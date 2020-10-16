"""
Module for testing the Terraform Cloud API Endpoint: State Versions.
"""

from .base import TestTFCBaseTestCase


class TestTFCStateVersions(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: State Versions.
    """

    _unittest_name = "state-ver"
    _endpoint_being_tested = "state_versions"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        self._oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = self._oauth_client["data"]["id"]
        oauth_token_id = \
            self._oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        _ws_create_with_vcs_payload = self._get_ws_with_vcs_create_payload(oauth_token_id)
        self._ws = self._api.workspaces.create(_ws_create_with_vcs_payload)
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

    def test_state_versions(self):
        """
        Test the State Version API endpoints.
        """

        # List the existing state versions, confirm there are none.
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
            filters=test_filters, page=0, page_size=50)["data"]
        self.assertEqual(len(state_versions), 0)
        self._api.workspaces.lock(self._ws_id, {"reason": "Unit testing."})

        # Create a state version, confirm we now have one
        self._api.state_versions.create(
            self._ws_id, self._get_state_version_create_payload())
        self._api.workspaces.unlock(self._ws_id)
        state_versions = self._api.state_versions.list(filters=test_filters)["data"]
        self.assertNotEqual(len(state_versions), 0)

        # Get the most current state version, confirm it matches the one we created
        state_version = state_versions[0]
        sv_id = state_version["id"]
        current_state_version = self._api.state_versions.get_current(self._ws_id)[
            "data"]
        self.assertEqual(sv_id, current_state_version["id"])

        # Show the state version by ID, confirm that they match
        shown_state_version = self._api.state_versions.show(sv_id)["data"]
        self.assertEqual(sv_id, shown_state_version["id"])
