"""
Module for testjkg the Terraform Cloud API Endpoint: State Versions.
"""

from .base import TestTFCBaseTestCase
from ._constants import PAGE_START, PAGE_SIZE


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
            filters=test_filters, page=PAGE_START, page_size=PAGE_SIZE)["data"]
        self.assertEqual(len(state_versions), 0)
        self._api.workspaces.lock(self._ws_id, {"reason": "Unit testing."})

        # Create a state version, confirm we now have one
        self._api.state_versions.create(
            self._ws_id, self._get_state_version_create_payload())
        self._api.workspaces.unlock(self._ws_id)

        state_versions_raw, _ = self._state_versions_includes_timeout(filters=test_filters, include=["outputs"])
        self.assertIn("included", state_versions_raw)

        state_versions = state_versions_raw["data"]
        self.assertNotEqual(len(state_versions), 0)

        all_state_versions_raw, _ = self._state_versions_includes_timeout(\
            filters=test_filters, include=["outputs"], list_all=True)
        self.assertIn("included", all_state_versions_raw)
        self.assertNotEqual(len(all_state_versions_raw["data"]), 0)

        # Get the most current state version, confirm it matches the one we created
        state_version = state_versions[0]
        sv_id = state_version["id"]

        # List the state version outputs
        sv_outputs = self._api.state_versions.list_outputs(sv_id)["data"]
        self.assertEqual(sv_outputs[0]["attributes"]["name"], "org_id")

        # Check the raw state version has the includes
        current_state_version_raw = \
            self._api.state_versions.get_current(self._ws_id, include=["outputs"])
        self.assertIn("included", current_state_version_raw)

        current_state_version = current_state_version_raw["data"]
        current_sv_id = current_state_version["id"]
        self.assertEqual(sv_id, current_sv_id)

        # TODO: these are only available on the TFE API, so we can't test them yet
        # marked = self._api.state_versions.mark_for_garbage_collection(current_sv_id)["data"]
        # unmarked = self._api.state_versions.restore_marked_for_garbage_collection(current_sv_id)["data"]
        # permanently_deleted = self._api.state_versions.permanently_delete_config_version(current_sv_id)["data"]

        shown_state_version_raw = self._api.state_versions.show(sv_id, include=["outputs"])
        # Confirm we have the related resources
        shown_state_version = shown_state_version_raw["data"]
        # Confirm the shown state version ID matches the input ID
        self.assertEqual(sv_id, shown_state_version["id"])

        # Test the Rollback functionality
        rollback_payload = {
            "data": {
                "type": "state-versions",
                "relationships": {
                    "rollback-state-version": {
                        "data": {
                            "type": "state-versions",
                            "id": sv_id
                        }
                    }
                }
            }
        }

        self._api.workspaces.lock(self._ws_id, {"reason": "Unit testing."})
        rolled_back_state_version = \
            self._api.state_versions.rollback(self._ws_id, rollback_payload)["data"]
        self._api.workspaces.unlock(self._ws_id)
        rolled_back_state_version_id = \
            rolled_back_state_version["relationships"]["rollback-state-version"]["data"]["id"]
        self.assertEqual(sv_id, rolled_back_state_version_id)
