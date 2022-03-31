"""
Module for testing the Terraform Cloud API Endpoint: State Version Outputs.
"""

import time

from .base import TestTFCBaseTestCase
from ._constants import PAGE_START, PAGE_SIZE


class TestTFCStateVersionOutputs(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: State Version Outputs.
    """

    _unittest_name = "state-ver-out"
    _endpoint_being_tested = "state_version_outputs"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        self._oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = self._oauth_client["data"]["id"]
        oauth_token_id = \
            self._oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        _ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id)
        self._ws = self._api.workspaces.create(_ws_payload)
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

        # Create an example config version for the unittest
        self._config_version = self._api.config_versions.create(
            self._ws_id, self._get_config_version_create_payload())["data"]
        self._config_version_upload_url = self._config_version["attributes"]["upload-url"]
        self._cv_id = self._config_version["id"]
        self._api.config_versions.upload(
            self._config_version_upload_tarball_path, self._config_version_upload_url)

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_state_version_outputs(self):
        """
        Test the State Version Outputs API endpoints.
        """

        # Create a sample state version
        self._api.workspaces.lock(self._ws_id, {"reason": "Unit testing."})
        _ = self._api.state_versions.create(self._ws_id, self._get_state_version_create_payload())["data"]
        self._api.workspaces.unlock(self._ws_id)

        # Get the state version ID, using list instead of extracting from the create
        # response to make the test shorter (less calls).
        test_filters = [
            {
                "keys": ["workspace", "name"],
                "value": self._ws_name
            },
            {
                "keys": ["organization", "name"],
                "value": self._test_org_name
            }
        ]
        state_versions = self._api.state_versions.list(\
            filters=test_filters, page=PAGE_START, page_size=PAGE_SIZE)["data"]
        state_version = state_versions[0]
        sv_id = state_version["id"]

        listed_state_version_outputs = self._api.state_version_outputs.list(sv_id, \
            page=PAGE_START, page_size=PAGE_SIZE)["data"]
        self.assertEqual(listed_state_version_outputs[0]["type"], "state-version-outputs")

        # Get the state version outputs ID, get the outputs, confirm they match the expected IDs
        shown_state_version = self._api.state_versions.show(sv_id)["data"]
        state_version_outputs = shown_state_version["relationships"]["outputs"]["data"]

        time.sleep(3)
        state_version_output_id = state_version_outputs[0]["id"]
        shown_state_version_output = self._api.state_version_outputs.show(
            state_version_output_id)["data"]
        self.assertEqual(state_version_output_id,
                         shown_state_version_output["id"])

        current_state_version_outputs = self._api.state_version_outputs.show_current_for_workspace(self._ws_id)["data"]
        self.assertEqual(current_state_version_outputs[0]["id"], state_version_output_id)
