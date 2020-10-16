"""
Module for testing the Terraform Cloud API Endpoint: Config Versions.
"""

from .base import TestTFCBaseTestCase


class TestTFCConfigVersions(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Config Versions.
    """

    _unittest_name = "cnf-ver"
    _endpoint_being_tested = "config_versions"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_without_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)

    def test_config_versions(self):
        """
        Test the Config Versions API endpoints.
        """

        # Create a new config version
        config_version = self._api.config_versions.create(
            self._ws_id, self._get_config_version_create_payload())["data"]
        cv_id = config_version["id"]

        # List all of the config versions for the workspace
        all_config_versions = self._api.config_versions.list(self._ws_id)["data"]

        # Confirm we found the newly created config version
        found_conf_ver = False
        for conf_ver in all_config_versions:
            if cv_id == conf_ver["id"]:
                found_conf_ver = True
                break
        self.assertTrue(found_conf_ver)

        # Confirm the config version status is "pending" or "uploaded" as well
        uploaded_or_pending = \
            all_config_versions[0]["attributes"]["status"] in ["pending", "uploaded"]
        self.assertTrue(uploaded_or_pending)

        # Test the show method on that same config version ID
        shown_config_version = self._api.config_versions.show(cv_id)["data"]

        # Confirm the results match the same ID we looked up
        self.assertEqual(shown_config_version["id"], cv_id)

        # Upload the .tf code and confirm it's been uploaded
        upload_url = shown_config_version["attributes"]["upload-url"]
        self._api.config_versions.upload(
            self._config_version_upload_tarball_path, upload_url)

        config_versions = self._api.config_versions.list(self._ws_id)["data"]
        uploaded_or_pending = \
            config_versions[0]["attributes"]["status"] in ["pending", "uploaded"]
        self.assertTrue(uploaded_or_pending)
