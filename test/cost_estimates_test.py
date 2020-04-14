"""
Module for testing the Terraform Cloud API Endpoint: Cost Estimates.
"""

import time

from .base import TestTFCBaseTestCase

from ._constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class TestTFCCostEstimates(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Cost Estimates.
    """

    def setUp(self):
        # Create an OAuth client for the test and extract it's ID
        unittest_name = "cost-est"
        oauth_client_payload = self._get_oauth_client_create_payload(
            unittest_name)
        oauth_client = self._api.oauth_clients.create(oauth_client_payload)
        self._oauth_client_id = oauth_client["data"]["id"]

        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        _ws_payload = self._get_ws_with_vcs_create_payload(
            unittest_name, oauth_token_id, working_dir="aws")
        workspace = self._api.workspaces.create(_ws_payload)["data"]
        self._ws_id = workspace["id"]

        variable_payloads = [
            self._get_variable_create_payload(
                "AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID, self._ws_id, category="env", sensitive=True),
            self._get_variable_create_payload(
                "AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY, self._ws_id, category="env", sensitive=True)
        ]
        for payload in variable_payloads:
            self._api.variables.create(payload)

        update_payload = {
            "data": {
                "attributes": {
                    "enabled": True,
                    "aws-enabled": True,
                    "aws-access-key-id": AWS_ACCESS_KEY_ID,
                    "aws-secret-key": AWS_SECRET_ACCESS_KEY
                }
            }
        }
        self._api.admin_settings.update_cost_estimation(update_payload)["data"]

        update_payload = {
            "data": {
                "attributes": {
                    "cost-estimation-enabled": True
                }
            }
        }
        self._api.orgs.update(self._test_org_name, update_payload)

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_show(self):
        """
        Test the Cost Estimates API endpoints: show.
        """
        # Wait a second for the workspace to create, otherwise we could get an
        # invalid run parameters error.
        time.sleep(1)

        # Create a run
        create_run_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_run_payload)["data"]
        run_id = run["id"]

        # Wait for it to plan
        planned_run = self._api.runs.show(run_id)["data"]
        while not planned_run["attributes"]["actions"]["is-confirmable"]:
            self._logger.debug("Waiting on plan to execute...")
            time.sleep(1)
            planned_run = self._api.runs.show(run_id)["data"]
        self._logger.debug("Plan successful.")

        # Get the Cost Estimate ID from the plan, and confirm that we can show it
        cost_estimate_id = planned_run["relationships"]["cost-estimate"]["data"]["id"]
        cost_estimate = self._api.cost_estimates.show(cost_estimate_id)["data"]
        self.assertEqual("cost-estimates", cost_estimate["type"])