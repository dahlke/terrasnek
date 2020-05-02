"""
Module for testing the Terraform Cloud API Endpoint: Runs.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCRuns(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Runs.
    """

    def setUp(self):
        # Create an OAuth client for the test and extract it's ID
        unittest_name = "runs"
        oauth_client_payload = self._get_oauth_client_create_payload(
            unittest_name)
        oauth_client = self._api.oauth_clients.create(oauth_client_payload)
        self._oauth_client_id = oauth_client["data"]["id"]

        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        _ws_payload = self._get_ws_with_vcs_create_payload(
            unittest_name, oauth_token_id)
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

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_run_and_apply(self):
        """
        Test the Runs API endpoints: create, show, apply.
        """

        # Create a run
        create_run_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_run_payload)["data"]
        run_id = run["id"]

        # Wait for it to plan
        created_run = self._api.runs.show(run_id)["data"]
        while not created_run["attributes"]["actions"]["is-confirmable"]:
            self._logger.debug("Waiting on plan to execute...")
            time.sleep(1)
            created_run = self._api.runs.show(run_id)["data"]
        self._logger.debug("Plan successful.")

        self.assertEqual(created_run["relationships"]["workspace"]["data"]["id"],
                         create_run_payload["data"]["relationships"]["workspace"]["data"]["id"])
        self.assertEqual(created_run["attributes"]
                         ["actions"]["is-confirmable"], True)
        self.assertRaises(
            KeyError, lambda: created_run["attributes"]["status-timestamps"]["applying-at"])

        # List the runs, using the correct parameters
        all_runs = self._api.runs.list(self._ws_id, page=0, page_size=50)["data"]
        self.assertEqual(len(all_runs), 1)

        # Apply the plan
        self._api.runs.apply(run_id)

        status_timestamps = self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        while "applying-at" not in status_timestamps:
            time.sleep(1)
            status_timestamps = \
                self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        self.assertNotEqual(status_timestamps["applying-at"], None)

    def test_run_and_discard(self):
        """
        Test the Runs API endpoint: discard.
        """

        # Create a run
        create_run_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_run_payload)["data"]
        run_id = run["id"]

        created_run = self._api.runs.show(run_id)["data"]
        self.assertRaises(
            KeyError, lambda: created_run["attributes"]["status-timestamps"]["discarded-at"])

        while not created_run["attributes"]["actions"]["is-confirmable"]:
            self._logger.debug("Waiting on plan to execute...")
            time.sleep(1)
            created_run = self._api.runs.show(run_id)["data"]
        self._logger.debug("Plan successful.")

        # Discard the run
        self._api.runs.discard(run_id)
        status_timestamps = self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        while "discarded-at" not in status_timestamps:
            time.sleep(1)
            status_timestamps = \
                self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        self.assertNotEqual(status_timestamps["discarded-at"], None)

    def test_run_and_cancel(self):
        """
        Test the Runs API endpoint: cancel.
        """

        # Create a run
        create_run_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_run_payload)["data"]
        run_id = run["id"]

        created_run = self._api.runs.show(run_id)["data"]
        self.assertEqual(created_run["attributes"]["canceled-at"], None)

        # Wait for it to plan
        self._logger.debug("Sleeping while plan half-executes...")
        time.sleep(1)
        self._logger.debug("Done sleeping.")

        # Cancel the run
        self._api.runs.cancel(run_id)
        status_timestamps = self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        while "force-canceled-at" not in status_timestamps:
            time.sleep(1)
            status_timestamps = \
                self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        self.assertNotEqual(status_timestamps["force-canceled-at"], None)
