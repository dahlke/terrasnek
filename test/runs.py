
import unittest
import os
import time
from .base import TestTFEBaseTestCase

from terrasnek.api import TFE

class TestTFERuns(TestTFEBaseTestCase):

    @classmethod
    def setUpClass(self):
        super(TestTFERuns, self).setUpClass()
        self._oauth_client = self._api.oauth_clients.create(
            self._oauth_client_create_payload)
        self._oauth_client_id = self._oauth_client["data"]["id"]

        self._oauth_token_id = self._oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        _ws_create_with_vcs_payload = self._get_create_ws_with_vcs_payload(
            self._oauth_token_id)

        self._ws = self._api.workspaces.create(_ws_create_with_vcs_payload)
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

        self._config_version = self._api.config_versions.create(
            self._ws_id, self._config_version_create_payload)["data"]
        self._config_version_upload_url = self._config_version["attributes"]["upload-url"]
        self._cv_id = self._config_version["id"]
        self._api.config_versions.upload(
            self._config_version_upload_tarball_path, self._cv_id)

    @classmethod
    def tearDownClass(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_run_and_apply(self):
        # Create a run
        create_run_payload = self._get_create_run_payload(self._ws_id)
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

        # Apply the plan
        self._api.runs.apply(run_id)
        self._logger.debug("Sleeping while plan applies...")
        time.sleep(10)
        self._logger.debug("Done sleeping.")
        applied_run = self._api.runs.show(run_id)["data"]
        self.assertNotEqual(
            applied_run["attributes"]["status-timestamps"]["applying-at"], None)

        # Test the Plan/Apply endpoints with this run
        plan_id = applied_run["relationships"]["plan"]["data"]["id"]
        plan = self._api.plans.show(plan_id)["data"]
        self.assertEqual(plan_id, plan["id"])

        apply_id = applied_run["relationships"]["apply"]["data"]["id"]
        apply = self._api.applies.show(apply_id)["data"]
        self.assertEqual(apply_id, apply["id"])

        # Test the Plan Exports endpoint with this run
        plan_export = self._api.plan_exports.create(
            self._get_create_plan_export_payload(plan_id))["data"]
        self.assertEqual(
            plan_id, plan_export["relationships"]["plan"]["data"]["id"])

        # Verify that we get the right plan export back if we look it up by ID
        plan_export_id = plan_export["id"]
        shown_plan_export = self._api.plan_exports.show(plan_export_id)["data"]
        self.assertEqual(plan_export_id, shown_plan_export["id"])

        # If the download path already exists, clear it out, then download the plan
        # export, and verify it gets downloaded
        if os.path.exists(self._plan_export_tarball_target_path):
            os.remove(self._plan_export_tarball_target_path)
        self._api.plan_exports.download(
            plan_export_id, target_path=self._plan_export_tarball_target_path)
        self.assertTrue(os.path.exists(self._plan_export_tarball_target_path))
        os.remove(self._plan_export_tarball_target_path)

        # Destroy the plan export and make sure we can't fetch it any more
        self._api.plan_exports.destroy(plan_export_id)
        deleted_plan_export = self._api.plan_exports.show(plan_export_id)
        self.assertEqual(deleted_plan_export, None)

    def test_run_and_discard(self):
        # Create a run
        create_run_payload = self._get_create_run_payload(self._ws_id)
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
        self._logger.debug("Sleeping while run discards...")
        time.sleep(3)
        self._logger.debug("Done sleeping.")

        discarded_run = self._api.runs.show(run_id)["data"]
        self.assertNotEqual(
            discarded_run["attributes"]["status-timestamps"]["discarded-at"], None)

    def test_run_and_cancel(self):
        # Create a run
        create_run_payload = self._get_create_run_payload(self._ws_id)
        run = self._api.runs.create(create_run_payload)["data"]
        run_id = run["id"]

        created_run = self._api.runs.show(run_id)["data"]
        self.assertEqual(created_run["attributes"]["canceled-at"], None)

        # Wait for it to plan
        self._logger.debug("Sleeping while plan half-executes...")
        time.sleep(3)
        self._logger.debug("Done sleeping.")

        # Discard the run
        self._api.runs.cancel(run_id)
        self._logger.debug("Sleeping while run cancels...")
        time.sleep(10)
        self._logger.debug("Done sleeping.")

        cancelled_run = self._api.runs.show(run_id)["data"]
        self.assertNotEqual(cancelled_run["attributes"]["canceled-at"], None)

    def test_run_with_created_state_version(self):
        pass
