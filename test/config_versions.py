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

    @classmethod
    def tearDownClass(self):
        self._api.workspaces.destroy(workspace_name=self._ws["data"]["attributes"]["name"])

    def test_config_version_lifecycle(self):
        ws_id = self._ws["data"]["id"]

        # Create a new config version and confirm it's creation
        config_version = self._api.config_versions.create(ws_id, self._config_version_create_payload)["data"]
        config_versions = self._api.config_versions.ls(ws_id)["data"]
        cv_id = config_version["id"]
        self.assertEqual(len(config_versions), 1)
        self.assertEqual(config_versions[0]["id"], cv_id)

        shown_config_version = self._api.config_versions.show(cv_id)["data"]
        self.assertEqual(shown_config_version["id"], cv_id)
