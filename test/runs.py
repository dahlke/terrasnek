
import unittest
import os
import time
from .base import TestTFEBaseTestCase

from tfepy.api import TFE

RUN_SLEEP_TIME = 30

class TestTFERuns(TestTFEBaseTestCase):

    @classmethod
    def setUpClass(self):
        super(TestTFERuns, self).setUpClass()
        self._oauth_client = self._api.oauth_clients.create(self._oauth_client_create_payload)
        self._oauth_client_id = self._oauth_client["data"]["id"]

        self._oauth_token_id = self._oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        _ws_create_with_vcs_payload = self._get_create_ws_with_vcs_payload(self._oauth_token_id)

        self._ws = self._api.workspaces.create(_ws_create_with_vcs_payload)
        self._ws_id = self._ws["data"]["id"]

        self._config_version = self._api.config_versions.create(self._ws_id, self._config_version_create_payload)["data"]
        self._config_version_upload_url = self._config_version["attributes"]["upload-url"]
        self._cv_id = self._config_version["id"]
        self._api.config_versions.upload(self._config_version_upload_tarball_path, self._cv_id)

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
        print("Sleeping while plan executes...")
        time.sleep(30)
        print("Done sleeping.")

        created_run = self._api.runs.show(run_id)["data"]
        self.assertEqual(created_run["relationships"]["workspace"]["data"]["id"], create_run_payload["data"]["relationships"]["workspace"]["data"]["id"])
        self.assertEqual(created_run["attributes"]["actions"]["is-confirmable"], True)
        self.assertRaises(KeyError, lambda: created_run["attributes"]["status-timestamps"]["applying-at"])

        # Apply the plan
        self._api.runs.apply(run_id)
        print("Sleeping while plan applies...")
        time.sleep(10)
        print("Done sleeping.")
        applied_run = self._api.runs.show(run_id)["data"]
        self.assertNotEqual(applied_run["attributes"]["status-timestamps"]["applying-at"], None)

    def test_run_and_discard(self):
        # Create a run
        create_run_payload = self._get_create_run_payload(self._ws_id)
        run = self._api.runs.create(create_run_payload)["data"]
        run_id = run["id"]
        created_run = self._api.runs.show(run_id)["data"]
        self.assertRaises(KeyError, lambda: created_run["attributes"]["status-timestamps"]["discarded-at"])

        # Wait for it to plan
        print("Sleeping while plan executes...")
        time.sleep(30)
        print("Done sleeping.")

        # Discard the run
        self._api.runs.discard(run_id)
        print("Sleeping while run discards...")
        time.sleep(RUN_SLEEP_TIME)
        print("Done sleeping.")

        discarded_run = self._api.runs.show(run_id)["data"]
        self.assertNotEqual(discarded_run["attributes"]["status-timestamps"]["discarded-at"], None)
