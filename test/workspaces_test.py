"""
Module for testing the Terraform Cloud API Endpoint: Workspaces.
"""

from .base import TestTFCBaseTestCase


class TestTFCWorkspaces(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Workspaces.
    """

    _unittest_name = "ws"

    def setUp(self):
        # Add an SSH Key to TFC
        create_payload = self._get_ssh_key_create_payload()
        created_key = self._api.ssh_keys.create(create_payload)["data"]
        self._created_key_id = created_key["id"]

    def tearDown(self):
        self._api.ssh_keys.destroy(self._created_key_id)

    def test_workspaces(self):
        """
        Test the Workspaces API endpoints: create, destroy, show, lock,
        unlock, update, assign_ssh_key, unassign_ssh_key.
        """

        # Get the number of existing workspaces, then create one and compare them
        num_workspaces_before_create = len(self._api.workspaces.list()["data"])
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload())["data"]
        ws_id = workspace["id"]
        # TODO: check for the workspace ID, not the length
        self.assertNotEqual(\
            num_workspaces_before_create, len(self._api.workspaces.list()["data"]))

        # Lock the workspace and confirm it's locked
        ws_locked = self._api.workspaces.lock(
            ws_id, {"reason": "Unit testing."})
        self.assertTrue(ws_locked["data"]["attributes"]["locked"])

        # Unlock the workspace and confirm it's unlocked
        ws_unlocked = self._api.workspaces.unlock(ws_id)
        self.assertFalse(ws_unlocked["data"]["attributes"]["locked"])

        # Relock the workspace and confirm it's locked
        ws_relocked = self._api.workspaces.lock(
            ws_id, {"reason": "Unit testing."})
        self.assertTrue(ws_relocked["data"]["attributes"]["locked"])

        # Force an unlock and confirm its unlocked
        ws_forced = self._api.workspaces.force_unlock(ws_id)
        self.assertFalse(ws_forced["data"]["attributes"]["locked"])

        # Update the workspace, check that the updates took effect
        updated_name = "unittest-update"
        update_payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name": updated_name
                }
            }
        }
        ws_updated = self._api.workspaces.update(ws_id, update_payload)["data"]
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
        self.assertTrue("ssh-key" in ws_shown_by_id["relationships"])

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
        self.assertTrue("ssh-key" not in ws_shown_by_id["relationships"])

        self._api.workspaces.destroy(
            workspace_name=updated_name)
        self.assertNotEqual(\
            num_workspaces_after_create, len(self._api.workspaces.list()["data"]))
