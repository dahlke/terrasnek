"""
Module for testing the Terraform Cloud API Endpoint: Policy Checks.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCPolicyChecks(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policy Checks.
    """

    _unittest_name = "pol-chk"
    _endpoint_being_tested = "policy_checks"

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

        # Add the policy set
        # Add a policy set to TFC
        pol_set_create_payload = self._get_policy_set_create_payload(oauth_token_id)
        created_policy_set = self._api.policy_sets.create(pol_set_create_payload)["data"]
        self._created_policy_set_id = created_policy_set["id"]

        # Attach the policy set to the workspace we created, confirm it's attached
        attach_to_workspace = {
            "data": [
                {
                    "id": self._ws_id, "type": "workspaces"
                },
            ]
        }
        self._api.policy_sets.attach_policy_set_to_workspaces(\
            self._created_policy_set_id, attach_to_workspace)

        # Wait a second to make sure the policy is attached before creating the run
        time.sleep(1)

        # Start the run, store the run ID
        create_run_payload = self._get_run_create_payload(self._ws_id)
        self._run = self._api.runs.create(create_run_payload)["data"]
        self._run_id = self._run["id"]


    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)
        self._api.policy_sets.destroy(self._created_policy_set_id)

    def test_policy_checks(self):
        """
        Test the Policy Checks API endpoints.
        """

        # Create a run and wait for the created run to complete it's plan
        created_run = self._api.runs.show(self._run_id)["data"]
        while created_run["attributes"]["status"] != "policy_override":
            self._logger.debug("Waiting for created run to get to policy override status...")
            created_run = self._api.runs.show(self._run_id)["data"]
            time.sleep(1)
        self._logger.debug("Plan successful.")

        run_id = created_run["id"]

        # List the policy checks, make sure we only have one and that it failed
        pol_checks = self._api.policy_checks.list(run_id)["data"]
        self.assertEqual(len(pol_checks), 1)
        self.assertFalse(pol_checks[0]["attributes"]["result"]["result"])

        # Override the policy check that soft failed, confirm we can continue
        self._api.policy_checks.override(pol_checks[0]["id"])

        created_run = self._api.runs.show(self._run_id)["data"]
        self.assertTrue(created_run["attributes"]["actions"]["is-confirmable"])
