import unittest
import os
from .base import TestTFEBaseTestCase

from tfepy.api import TFE


class TestTFEConfigVersions(TestTFEBaseTestCase):

    @classmethod
    def setUpClass(self):
        super(TestTFEConfigVersions, self).setUpClass()
        # TODO: How to manage VCS OAuth and create w/ VCS payload?
        self._ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        self._ws_id = self._ws["data"]["id"]

    @classmethod
    def tearDownClass(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)

    def test_config_version_lifecycle(self):
        # Create a new config version and confirm it's creation, and it's pending state
        config_version = self._api.config_versions.create(self._ws_id, self._config_version_create_payload)["data"]
        config_versions = self._api.config_versions.ls(self._ws_id)["data"]
        cv_id = config_version["id"]
        self.assertEqual(len(config_versions), 1)
        self.assertEqual(config_versions[0]["id"], cv_id)
        self.assertEqual(config_versions[0]["attributes"]["status"], "pending")

        shown_config_version = self._api.config_versions.show(cv_id)["data"]
        self.assertEqual(shown_config_version["id"], cv_id)
        
        # Upload the .tf code and confirm it's been uploaded
        self._api.config_versions.upload(self._config_version_upload_tarball_path, cv_id)
        config_versions = self._api.config_versions.ls(self._ws_id)["data"]
        self.assertEqual(config_versions[0]["attributes"]["status"], "uploaded")
    
    # TODO: test force_cancel / force_execute once policy endpoints are implemented