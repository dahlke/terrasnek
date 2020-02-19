"""
Module for testing the Terraform Cloud API Endpoint: Workspaces.
"""

from .base import TestTFCBaseTestCase


class TestTFCWorkspaces(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Workspaces.
    """

    def test_workspaces_create(self):
        """
        Test the Workspaces API endpoints: create.
        """

        # TODO: How to manage VCS OAuth and create w/ VCS payload?
        num_workspaces_before_create = len(self._api.workspaces.lst()["data"])
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("workspaces"))
        num_workspaces_after_create = len(self._api.workspaces.lst()["data"])
        self.assertNotEqual(num_workspaces_before_create,
                            num_workspaces_after_create)

        self._api.workspaces.destroy(
            workspace_name=workspace["data"]["attributes"]["name"])
        num_workspaces_after_destroy = len(self._api.workspaces.lst()["data"])
        self.assertNotEqual(num_workspaces_after_create,
                            num_workspaces_after_destroy)

    def test_destroy(self):
        """
        Test the Workspaces API endpoint: destroy.
        """

        # Create a workspace
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("workspaces"))
        num_workspaces_before = len(self._api.workspaces.lst()["data"])

        # Destroy it with it's name
        ws_name = workspace["data"]["attributes"]["name"]
        self._api.workspaces.destroy(workspace_name=ws_name)
        num_workspaces_after = len(self._api.workspaces.lst()["data"])
        self.assertNotEqual(num_workspaces_before, num_workspaces_after)

        # Create another workspace
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("workspaces"))

        # Destroy it with it's ID
        ws_id = workspace["data"]["id"]
        num_workspaces_before = len(self._api.workspaces.lst()["data"])
        self._api.workspaces.destroy(workspace_id=ws_id)
        num_workspaces_after = len(self._api.workspaces.lst()["data"])
        self.assertNotEqual(num_workspaces_before, num_workspaces_after)

    def test_workspaces_lock_unlock(self):
        """
        Test the Workspaces API endpoints: lock and unlock.
        """

        # Create a workspace and make sure it's not locked
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("workspaces"))
        ws_id = workspace["data"]["id"]

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

        # Clean up the workspace
        self._api.workspaces.destroy(workspace_id=ws_id)

    def test_workspaces_show(self):
        """
        Test the Workspaces API endpoint: show.
        """

        # Create a workspace
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("workspaces"))

        # Get that workspace's ID, retrieve it's data and compare IDs
        ws_id = workspace["data"]["id"]
        ws_shown_by_id = self._api.workspaces.show(workspace_id=ws_id)
        self.assertEqual(ws_id, ws_shown_by_id["data"]["id"])

        # Get that workspace's name, retrieve it's data and compare names
        ws_name = workspace["data"]["attributes"]["name"]
        ws_shown_by_name = self._api.workspaces.show(workspace_name=ws_name)
        self.assertEqual(
            ws_name, ws_shown_by_name["data"]["attributes"]["name"])

        # Clean up the workspace
        self._api.workspaces.destroy(workspace_id=ws_id)

    def test_workspaces_update(self):
        """
        Test the Workspaces API endpoint: update.
        """

        # Create a workspace
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("workspaces"))

        # Get that workspace's ID, and update it's name
        ws_id = workspace["data"]["id"]
        updated_name = "unittest-update"
        update_payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name": updated_name
                }
            }
        }
        ws_updated = self._api.workspaces.update(ws_id, update_payload)
        self.assertEqual(
            updated_name, ws_updated["data"]["attributes"]["name"])

        # Clean up the workspace
        self._api.workspaces.destroy(workspace_id=ws_id)
