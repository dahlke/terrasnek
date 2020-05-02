"""
Module for testing the Terraform Cloud API Endpoint: Plans.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCPlans(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Plans.
    """


    def setUp(self):
        # Create an OAuth client for the test and extract it's ID
        unittest_name = "plans"
        oauth_client_payload = self._get_oauth_client_create_payload(unittest_name)
        oauth_client = self._api.oauth_clients.create(oauth_client_payload)
        self._oauth_client_id = oauth_client["data"]["id"]

        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        _ws_payload = self._get_ws_with_vcs_create_payload("plans", oauth_token_id)
        workspace = self._api.workspaces.create(_ws_payload)["data"]
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

    def test_plan(self):
        """
        Test the Plans API endpoint: show.
        """

        # Create a run and wait for the created run to complete it's plan
        created_run = self._api.runs.show(self._run_id)["data"]
        created_plan_id = created_run["relationships"]["plan"]["data"]["id"]

        while not created_run["attributes"]["actions"]["is-confirmable"]:
            self._logger.debug("Waiting on plan to execute...")
            created_run = self._api.runs.show(self._run_id)["data"]
            self._logger.debug("Waiting for created run to finish planning...")
            time.sleep(1)
        self._logger.debug("Plan successful.")

        plan = self._api.plans.show(created_plan_id)["data"]
        self.assertEqual(created_plan_id, plan["id"])
