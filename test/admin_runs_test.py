"""
Module for testing the Terraform Cloud API Endpoint: Admin Runs.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCAdminRuns(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Runs.
    """

    _unittest_name = "adm-run"
    _endpoint_being_tested = "admin_runs"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        oauth_client = self._api.oauth_clients.create(\
            self._get_oauth_client_create_payload())["data"]
        self._oauth_client_id = oauth_client["id"]
        oauth_token_id = oauth_client["relationships"]["oauth-tokens"]["data"][0]["id"]

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
        run = self._api.runs.create(create_run_payload)["data"]
        self._run_id = run["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_admin_runs(self):
        """
        Test all the Admin Runs API endpoints.
        """

        # List all the runs confirm the one we created in the setup is there
        all_runs = self._api.admin_runs.list(\
            query=self._run_id, filters=[], page=0, page_size=50)["data"]
        found_run = False
        for run in all_runs:
            run_id = run["id"]
            if run_id == self._run_id:
                found_run = True
                break
        self.assertTrue(found_run)

        # Wait a second for to give the run some time to half plan
        self._logger.debug("Sleeping while plan half-executes...")
        time.sleep(1)
        self._logger.debug("Done sleeping.")

        # Force cancel the run and confirm that it has been cancelled
        self._api.admin_runs.force_cancel(self._run_id)
        status_timestamps = \
            self._api.runs.show(self._run_id)["data"]["attributes"]["status-timestamps"]
        while "force-canceled-at" not in status_timestamps:
            # Wait a second while we wait for the force cancel to go through
            time.sleep(1)
            status_timestamps = \
                self._api.runs.show(self._run_id)["data"]["attributes"]["status-timestamps"]
        self.assertIsNotNone(status_timestamps["force-canceled-at"])
