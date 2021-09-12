"""
Module for testing the Terraform Cloud API Endpoint: Runs.
"""

import time

from terrasnek.exceptions import TFCHTTPConflict
from .base import TestTFCBaseTestCase
from ._constants import PAGE_START, PAGE_SIZE


class TestTFCRuns(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Runs.
    """

    _unittest_name = "runs"
    _endpoint_being_tested = "runs"

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

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_run_and_apply(self):
        """
        Test the Runs API endpoints with an apply.
        """
        # Create a run
        create_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_payload)["data"]
        run_id = run["id"]

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        created_run = self._created_run_timeout(run_id)

        self.assertEqual(created_run["relationships"]["workspace"]["data"]["id"],
                         create_payload["data"]["relationships"]["workspace"]["data"]["id"])
        self.assertTrue(created_run["attributes"]["actions"]["is-confirmable"], True)
        self.assertRaises(
            KeyError, lambda: created_run["attributes"]["status-timestamps"]["applying-at"])

        # List the runs, using the correct parameters, confirm it has been created
        # and we have our includes.
        some_runs_raw = self._api.runs.list(self._ws_id, page=PAGE_START, page_size=PAGE_SIZE, include=["plan"])
        self.assertIn("included", some_runs_raw)

        some_runs = some_runs_raw["data"]
        found_run = False
        for run in some_runs:
            if run["id"] == run_id:
                found_run = True
                break
        self.assertTrue(found_run)

        all_runs = self._api.runs.list_all(self._ws_id, include=["plan"])
        self.assertIn("included", all_runs)

        found_run = False
        for run in all_runs["data"]:
            if run["id"] == run_id:
                found_run = True
                break
        self.assertTrue(found_run)

        # Apply the plan
        apply_payload = {
            "comment": "foo"
        }
        self._api.runs.apply(run_id, apply_payload)

        # Wait for the plan to apply, then confirm the apply took place
        status_timestamps = self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        while "applying-at" not in status_timestamps:
            time.sleep(1)
            status_timestamps = \
                self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        self.assertIsNotNone(status_timestamps["applying-at"])

    def test_run_and_discard(self):
        """
        Test the Runs API endpoints for a discard.
        """

        # Create a run
        create_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_payload)["data"]
        run_id = run["id"]

        created_run = self._api.runs.show(run_id)["data"]
        self.assertRaises(
            KeyError, lambda: created_run["attributes"]["status-timestamps"]["discarded-at"])

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        created_run = self._created_run_timeout(run_id)

        # Discard the run
        discard_payload = {
            "comment": "foo"
        }
        self._api.runs.discard(run_id, discard_payload)
        status_timestamps = self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        while "discarded-at" not in status_timestamps:
            time.sleep(1)
            status_timestamps = \
                self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        self.assertIsNotNone(status_timestamps["discarded-at"])

    def test_run_and_cancel(self):
        """
        Test the Runs API endpoints for a normal cancel.
        """

        # Create a run
        create_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_payload)["data"]
        run_id = run["id"]

        # Show the created run, make sure it hasn't yet been cancelled
        created_run = self._api.runs.show(run_id)["data"]
        self.assertIsNone(created_run["attributes"]["canceled-at"])

        # Wait for it to plan
        self._logger.debug("Sleeping while plan half-executes...")
        time.sleep(1)
        self._logger.debug("Done sleeping.")

        # Cancel the run, confirm it has been cancelled
        cancel_payload = {
            "comment": "foo"
        }
        self._api.runs.cancel(run_id, cancel_payload)
        status_timestamps = self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        while "force-canceled-at" not in status_timestamps:
            time.sleep(1)
            status_timestamps = \
                self._api.runs.show(run_id)["data"]["attributes"]["status-timestamps"]
        self.assertIsNotNone(status_timestamps["force-canceled-at"])

    def test_run_and_force_cancel(self):
        """
        Test the Runs API endpoints for a force cancel.
        """

        # Create a run
        create_payload = self._get_run_create_payload(self._ws_id)
        run = self._api.runs.create(create_payload)["data"]
        run_id = run["id"]

        # Show the created run, make sure it hasn't yet been cancelled
        created_run = self._api.runs.show(run_id)["data"]
        self.assertIsNone(created_run["attributes"]["canceled-at"])

        # Wait for it to plan
        self._logger.debug("Sleeping while plan half-executes...")
        time.sleep(1)
        self._logger.debug("Done sleeping.")

        # Cancel the run first, it has to be cancelled before it can be force cancelled
        cancel_payload = {
            "comment": "foo"
        }
        self._api.runs.cancel(run_id, cancel_payload)

        # Cancel the run, confirm it has been cancelled
        force_cancel_payload = {
            "comment": "foo"
        }
        self.assertRaises(\
            TFCHTTPConflict, self._api.runs.force_cancel, run_id, force_cancel_payload)

        run_attrs = self._api.runs.show(run_id)["data"]["attributes"]
        while "force-cancel-available-at" not in run_attrs:
            shown_run = self._api.runs.show(run_id)["data"]
            run_attrs = shown_run["attributes"]
            time.sleep(1)
        self.assertIsNotNone(run_attrs["force-cancel-available-at"])
