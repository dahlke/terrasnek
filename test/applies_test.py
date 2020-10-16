"""
Module for testing the Terraform Cloud API Endpoint: Applies.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCApplies(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Applies.
    """

    _unittest_name = "applies"
    _endpoint_being_tested = "applies"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = oauth_client["data"]["id"]
        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id)
        workspace = self._api.workspaces.create(ws_payload)["data"]
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

    def test_apply(self):
        """
        Test the Applies API endpoints.
        """

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        self._created_run_timeout(self._run_id)

        # Apply the plan
        apply_payload = {
            "comment": "foo"
        }
        self._api.runs.apply(self._run_id, apply_payload)
        applied_run = self._api.runs.show(self._run_id)["data"]

        self._logger.debug("Waiting for apply to kick off...")
        while "applying-at" not in applied_run["attributes"]["status-timestamps"]:
            applied_run = self._api.runs.show(self._run_id)["data"]
            time.sleep(1)
        self._logger.debug("Apply kicked off.")
        self.assertIsNotNone(applied_run["attributes"]["status-timestamps"]["applying-at"])

        # Show the apply, confirm it returns the same value as the run attributes
        apply_id = applied_run["relationships"]["apply"]["data"]["id"]
        shown_apply = self._api.applies.show(apply_id)["data"]
        shown_apply_id = shown_apply["id"]
        self.assertEqual(apply_id, shown_apply_id)
