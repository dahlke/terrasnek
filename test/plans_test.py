"""
Module for testing the Terraform Cloud API Endpoint: Plans.
"""

import time
import os

from .base import TestTFCBaseTestCase


class TestTFCPlans(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Plans.
    """

    _unittest_name = "plans"
    _endpoint_being_tested = "plans"

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

        # Sleep for 1 second to give the WS time to create
        time.sleep(1)

        # Start the run, store the run ID
        create_run_payload = self._get_run_create_payload(self._ws_id)
        self._run = self._api.runs.create(create_run_payload)["data"]
        self._run_id = self._run["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_plans(self):
        """
        Test the Plans API endpoints.
        """

        # Create a run and wait for the created run to complete it's plan
        created_run = self._api.runs.show(self._run_id)["data"]
        created_plan_id = created_run["relationships"]["plan"]["data"]["id"]

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        created_run = self._created_run_timeout(self._run_id)

        # Confirm the shown plan's ID matches the ID from the run
        plan = self._api.plans.show(created_plan_id)["data"]
        self.assertEqual(created_plan_id, plan["id"])

        if os.path.exists(self._plan_json_tarball_target_path):
            os.remove(self._plan_json_tarball_target_path)

        # Download the plan JSON by run ID, then assert the file exists, and remove it
        self._api.plans.download_json(self._plan_json_tarball_target_path, run_id=self._run_id)
        self.assertTrue(os.path.exists(self._plan_json_tarball_target_path))
        os.remove(self._plan_json_tarball_target_path)
        self.assertFalse(os.path.exists(self._plan_json_tarball_target_path))

        # Show the plan, assert that the Plan IDs match
        shown_plan = self._api.plans.show(created_plan_id)["data"]
        self.assertEqual(created_plan_id, shown_plan["id"])

        # Download the plan JSON by run ID, then assert the file exists, and remove it
        self._api.plans.download_json(self._plan_json_tarball_target_path, plan_id=plan["id"])
        self.assertTrue(os.path.exists(self._plan_json_tarball_target_path))
        os.remove(self._plan_json_tarball_target_path)
        self.assertFalse(os.path.exists(self._plan_json_tarball_target_path))
