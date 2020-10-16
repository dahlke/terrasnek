"""
Module for testing the Terraform Cloud API Endpoint: Cost Estimates.
"""

import time

from .base import TestTFCBaseTestCase

from ._constants import \
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TFC_SAAS_HOSTNAME

class TestTFCCostEstimates(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Cost Estimates.
    """

    _unittest_name = "cst-est"
    _endpoint_being_tested = "cost_estimates"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        oauth_client_payload = self._get_oauth_client_create_payload()
        oauth_client = self._api.oauth_clients.create(oauth_client_payload)
        self._oauth_client_id = oauth_client["data"]["id"]
        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        _ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id, working_dir="aws")
        workspace = self._api.workspaces.create(_ws_payload)["data"]
        self._ws_id = workspace["id"]

        # Configure the required variables on the workspace
        variable_payloads = [
            self._get_variable_create_payload(
                "AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID, \
                self._ws_id, category="env", sensitive=True),
            self._get_variable_create_payload(
                "AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY, \
                self._ws_id, category="env", sensitive=True)
        ]
        for payload in variable_payloads:
            self._api.vars.create(payload)

        # Sleep for 1 second to give the WS time to create
        time.sleep(1)

        # Enable cost estimation if this is TFE
        if TFC_SAAS_HOSTNAME not in self._tfc_url:
            # Configure the AWS credentials for it at the admin level
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
            updated_admin_cost_est_settings = \
                self._api.admin_settings.update_cost_estimation(update_payload)["data"]
            self.assertTrue(updated_admin_cost_est_settings["attributes"]["enabled"])

        # Enable cost estimation on the org level
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

    def test_cost_estimates(self):
        """
        Test the Cost Estimates API endpoints.
        """

        # Create a run
        create_run_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_run_payload)["data"]
        run_id = run["id"]

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        created_run = self._created_run_timeout(run_id)

        # Get the Cost Estimate ID from the plan, and confirm that we can show it
        cost_estimate_id = created_run["relationships"]["cost-estimate"]["data"]["id"]
        cost_estimate = self._api.cost_estimates.show(cost_estimate_id)["data"]
        self.assertEqual("cost-estimates", cost_estimate["type"])
