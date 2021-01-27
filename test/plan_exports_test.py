"""
Module for testing the Terraform Cloud API Endpoint: Plan Exports.
"""

import time
import os

from terrasnek.exceptions import TFCHTTPNotFound
from .base import TestTFCBaseTestCase


class TestTFCPlanExports(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Plan Exports.
    """

    _unittest_name = "plan-exp"
    _endpoint_being_tested = "plan_exports"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = oauth_client["data"]["id"]
        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        _ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id)
        workspace = self._api.workspaces.create(_ws_payload)["data"]
        self._ws_id = workspace["id"]

        # Configure the required variables on the workspace
        variable_payloads = [
            self._get_variable_create_payload(
                "email", self._test_email, self._ws_id),
            self._get_variable_create_payload(
                "org_name", self._test_org_name, self._ws_id),
            self._get_variable_create_payload(
                "TFE_TOKEN", self._test_api_token, self._ws_id, category="env", sensitive=True)
        ]
        for payload in variable_payloads:
            self._api.vars.create(payload)

        # Sleep for 3 seconds to give the WS time to create, takes a bit longer
        # on small TFE instances.
        time.sleep(3)

        # Start the run, store the run ID
        create_run_payload = self._get_run_create_payload(self._ws_id)
        self._run = self._api.runs.create(create_run_payload)["data"]
        self._run_id = self._run["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_plan_exports(self):
        """
        Test the Plan Exports API endpoints.
        """

        # Create a run and wait for the created run to complete it's plan
        created_run = self._api.runs.show(self._run_id)["data"]
        created_plan_id = created_run["relationships"]["plan"]["data"]["id"]

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        created_run = self._created_run_timeout(self._run_id)

        # Export the plan, confirm the plan_id matches that in the exported plan
        create_plan_export_payload = {
            "data": {
                "type": "plan-exports",
                "attributes": {
                    "data-type": "sentinel-mock-bundle-v0"
                },
                "relationships": {
                    "plan": {
                        "data": {
                            "id": created_plan_id,
                            "type": "plans"
                        }
                    }
                }
            }
        }
        plan_export = self._api.plan_exports.create(create_plan_export_payload)["data"]
        self.assertEqual(
            created_plan_id, plan_export["relationships"]["plan"]["data"]["id"])

        # Verify that we get the right plan export back if we look it up by ID
        plan_export_id = plan_export["id"]
        shown_plan_export = self._api.plan_exports.show(plan_export_id)["data"]
        self.assertEqual(plan_export_id, shown_plan_export["id"])

        # If the download path already exists, clear it out, then download the plan
        # export, and verify it gets downloaded
        if os.path.exists(self._plan_export_tarball_target_path):
            os.remove(self._plan_export_tarball_target_path)
        self._api.plan_exports.download(
            plan_export_id, self._plan_export_tarball_target_path)
        self.assertTrue(os.path.exists(self._plan_export_tarball_target_path))
        os.remove(self._plan_export_tarball_target_path)

        # Destroy the plan export and confirm it's gone.
        self._api.plan_exports.destroy(plan_export_id)
        self.assertRaises(TFCHTTPNotFound, self._api.plan_exports.show, plan_export_id)
