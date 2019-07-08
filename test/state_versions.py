import unittest
import os
import time
from .base import TestTFEBaseTestCase

from tfepy.api import TFE

class TestTFEStateVersions(TestTFEBaseTestCase):

    @classmethod
    def setUpClass(self):
        super(TestTFEStateVersions, self).setUpClass()
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
        # TODO: ensure oauth_client destruction

    def test_run_and_apply(self):
        state_versions = self._api.state_versions.ls(self._ws_name)["data"]
        self.assertEqual(len(state_versions), 0)
        self._api.workspaces.lock(self._ws_id, {"reason": "Unit testing."})

        create_state_version_payload = self._get_create_state_version_payload()
        self._api.state_versions.create(self._ws_id, create_state_version_payload)
        self._api.workspaces.unlock(self._ws_id)

        state_versions = self._api.state_versions.ls(self._ws_name)["data"]
        self.assertNotEqual(len(state_versions), 0)

        state_version = state_versions[0]
        sv_id = state_version["id"]
        current_state_version = self._api.state_versions.get_current(self._ws_id)[
            "data"]
        self.assertEqual(sv_id, current_state_version["id"])

        shown_state_version = self._api.state_versions.show(sv_id)["data"]
        self.assertEqual(sv_id, shown_state_version["id"])

        state_version_outputs = shown_state_version["relationships"]["outputs"]["data"]
        self.assertEqual(len(state_version_outputs), 3)

        state_version_output_id = state_version_outputs[0]["id"]
        shown_state_version_output = self._api.state_version_outputs.show(state_version_output_id)["data"]
        self.assertEqual(state_version_output_id, shown_state_version_output["id"])