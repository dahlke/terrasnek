"""
Module for testing the Terraform Cloud API Endpoint: Workspaces.
"""

from .base import TestTFCBaseTestCase


class TestTFCWorkspaces(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Workspaces.
    """

    _unittest_name = "ws"
    _endpoint_being_tested = "workspaces"

    def setUp(self):
        # Add an SSH Key to TFC
        created_key = self._api.ssh_keys.create(self._get_ssh_key_create_payload())["data"]
        self._created_key_id = created_key["id"]

    def tearDown(self):
        self._api.ssh_keys.destroy(self._created_key_id)

    def test_workspaces(self):
        """
        Test the Workspaces API endpoints.
        """

        # Get the number of existing workspaces, then create one and compare them
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload())["data"]
        ws_id = workspace["id"]
        all_ws = self._api.workspaces.list(page=0, page_size=50)["data"]
        found_ws = False
        for workspace in all_ws:
            if workspace["id"] == ws_id:
                found_ws = True
                break
        self.assertTrue(found_ws)

        # Lock the workspace and confirm it's locked
        ws_locked = self._api.workspaces.lock(
            ws_id, {"reason": "Unit testing."})["data"]
        self.assertTrue(ws_locked["attributes"]["locked"])

        # Unlock the workspace and confirm it's unlocked
        ws_unlocked = self._api.workspaces.unlock(ws_id)
        self.assertFalse(ws_unlocked["data"]["attributes"]["locked"])

        # Relock the workspace and confirm it's locked
        ws_relocked = self._api.workspaces.lock(
            ws_id, {"reason": "Unit testing."})["data"]
        self.assertTrue(ws_relocked["attributes"]["locked"])

        # Force an unlock and confirm its unlocked
        ws_forced = self._api.workspaces.force_unlock(ws_id)["data"]
        self.assertFalse(ws_forced["attributes"]["locked"])

        # Update the workspace, check that the updates took effect
        updated_name = self._unittest_random_name()
        update_payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name": updated_name
                }
            }
        }
        ws_updated = self._api.workspaces.update(update_payload, workspace_id=ws_id)["data"]
        self.assertEqual(
            updated_name, ws_updated["attributes"]["name"])

        # Assign an SSH key and confirm it's added
        assign_payload = {
            "data": {
                "attributes": {
                    "id": self._created_key_id
                },
                "type": "workspaces"
            }
        }
        self._api.workspaces.assign_ssh_key(ws_id, assign_payload)

        # Show by ID, and make sure we get the right payload back. Also check for the
        # the newly assigned SSH key
        ws_shown_by_id = self._api.workspaces.show(workspace_id=ws_id)["data"]
        self.assertEqual(ws_id, ws_shown_by_id["id"])
        self.assertIn("ssh-key", ws_shown_by_id["relationships"])

        # Unassign the SSH key and confirm it's removed
        unassign_payload = {
            "data": {
                "attributes": {
                    "id": None
                },
                "type": "workspaces"
            }
        }
        self._api.workspaces.unassign_ssh_key(ws_id, unassign_payload)
        ws_shown_by_id = self._api.workspaces.show(workspace_id=ws_id)["data"]
        self.assertNotIn("ssh-key", ws_shown_by_id["relationships"])

        self._api.workspaces.destroy(
            workspace_name=updated_name)
        all_ws = self._api.workspaces.list()["data"]
        found_ws = False
        for workspace in all_ws:
            if workspace["id"] == ws_id:
                found_ws = True
                break

        self.assertFalse(found_ws)
