"""
Module for testing the Terraform Cloud API Endpoint: Applies.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCApplies(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Applies.
    """

    def setUp(self):
        unittest_name = "applies"
        # Create an OAuth client for the test and extract it's ID
        oauth_client_payload = self._get_oauth_client_create_payload(unittest_name)
        oauth_client = self._api.oauth_clients.create(oauth_client_payload)
        self._oauth_client_id = oauth_client["data"]["id"]

        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        ws_payload = self._get_ws_with_vcs_create_payload(unittest_name, oauth_token_id)
        workspace = self._api.workspaces.create(ws_payload)["data"]
        self._ws_id = workspace["id"]

        variable_payloads = [
            self._get_variable_create_payload(
                "email", self._test_email, self._ws_id),
            self._get_variable_create_payload(
                "org_name", "terrasnek_unittest", self._ws_id),
            self._get_variable_create_payload(
                "TFE_TOKEN", self._test_api_token, self._ws_id, category="env", sensitive=True)
        ]
        for payload in variable_payloads:
            self._api.variables.create(payload)

        create_run_payload = self._get_run_create_payload(self._ws_id)
        self._run = self._api.runs.create(create_run_payload)["data"]
        self._run_id = self._run["id"]


    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_apply(self):
        """
        Test the Applies API endpoint: show.
        """

        # Create a run and wait for the created run to complete it's plan
        created_run = self._api.runs.show(self._run_id)["data"]
        while not created_run["attributes"]["actions"]["is-confirmable"]:
            self._logger.debug("Waiting on plan to execute...")
            created_run = self._api.runs.show(self._run_id)["data"]
            self._logger.debug("Waiting for created run to finish planning...")
            time.sleep(1)
        self._logger.debug("Plan successful.")

        # Apply the plan
        self._api.runs.apply(self._run_id)
        applied_run = self._api.runs.show(self._run_id)["data"]

        self._logger.debug("Waiting for apply to kick off...")
        while applied_run["attributes"]["status-timestamps"]["applying-at"] is None:
            applied_run = self._api.runs.show(self._run_id)["data"]
            time.sleep(1)
        self._logger.debug("Apply kicked off.")
        self.assertNotEqual(
            applied_run["attributes"]["status-timestamps"]["applying-at"], None)

        apply_id = applied_run["relationships"]["apply"]["data"]["id"]
        shown_apply = self._api.applies.show(apply_id)["data"]
        shown_apply_id = shown_apply["id"]
        self.assertEqual(apply_id, shown_apply_id)
