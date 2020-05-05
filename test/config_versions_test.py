"""
Module for testing the Terraform Cloud API Endpoint: Config Versions.
"""

from .base import TestTFCBaseTestCase


class TestTFCConfigVersions(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Config Versions.
    """

    def setUp(self):
        self._ws = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("config-versions"))
        self._ws_id = self._ws["data"]["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)

    def test_config_version_lifecycle(self):
        """
        Test the Config Version API endpoints: create, list, show, upload.
        """

        # Create a new config version
        config_version = self._api.config_versions.create(
            self._ws_id, self._get_config_version_create_payload())["data"]

        # List all of the config versions for the workspace
        config_versions = self._api.config_versions.list(self._ws_id)["data"]
        cv_id = config_version["id"]

        # Confirm there is only one config version (the one we uploaded)
        self.assertEqual(len(config_versions), 1)
        # Confirm the first listed config version matches the ID of the one we created
        self.assertEqual(config_versions[0]["id"], cv_id)

        # Confirm it's status is "pending" as well
        self.assertEqual(config_versions[0]["attributes"]["status"], "pending")

        # Test the show method on that same config version ID
        shown_config_version = self._api.config_versions.show(cv_id)["data"]

        # Confirm the results match the same ID we looked up
        self.assertEqual(shown_config_version["id"], cv_id)

        # Upload the .tf code and confirm it's been uploaded
        self._api.config_versions.upload(
            self._config_version_upload_tarball_path, cv_id)

        config_versions = self._api.config_versions.list(self._ws_id)["data"]
        self.assertEqual(config_versions[0]
                         ["attributes"]["status"], "uploaded")

        # TODO: test force_cancel / force_execute once Policy endpoints are implemented
