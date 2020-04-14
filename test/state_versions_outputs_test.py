"""
Module for testing the Terraform Cloud API Endpoint: State Version Outputs.
"""

from .base import TestTFCBaseTestCase


class TestTFCStateVersionOutputs(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: State Version Outputs.
    """

    def setUp(self):
        unittest_name = "state-version-outputs"
        oauth_client_payload = self._get_oauth_client_create_payload(
            unittest_name)
        self._oauth_client = self._api.oauth_clients.create(
            oauth_client_payload)
        self._oauth_client_id = self._oauth_client["data"]["id"]

        self._oauth_token_id = \
            self._oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        _ws_create_with_vcs_payload = self._get_ws_with_vcs_create_payload(
            "state-version-outputs",
            self._oauth_token_id)

        self._ws = self._api.workspaces.create(_ws_create_with_vcs_payload)
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

        self._config_version = self._api.config_versions.create(
            self._ws_id, self._get_config_version_create_payload())["data"]
        self._config_version_upload_url = self._config_version["attributes"]["upload-url"]
        self._cv_id = self._config_version["id"]
        self._api.config_versions.upload(
            self._config_version_upload_tarball_path, self._cv_id)

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_run_and_apply(self):
        """
        Test the State Version API endpoints: list, create, show.
        """

        state_versions = self._api.state_versions.lst(self._ws_name)["data"]
        self._api.workspaces.lock(self._ws_id, {"reason": "Unit testing."})

        create_state_version_payload = self._get_state_version_create_payload()
        self._api.state_versions.create(
            self._ws_id, create_state_version_payload)
        self._api.workspaces.unlock(self._ws_id)

        state_versions = self._api.state_versions.lst(self._ws_name)["data"]

        state_version = state_versions[0]
        sv_id = state_version["id"]

        shown_state_version = self._api.state_versions.show(sv_id)["data"]
        state_version_outputs = shown_state_version["relationships"]["outputs"]["data"]
        state_version_output_id = state_version_outputs[0]["id"]
        shown_state_version_output = self._api.state_version_outputs.show(
            state_version_output_id)["data"]
        self.assertEqual(state_version_output_id,
                         shown_state_version_output["id"])
