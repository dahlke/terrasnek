"""
Module for testing the Terraform Cloud API Endpoint: Workspaces.
"""

from .base import TestTFCBaseTestCase
from ._constants import PAGE_START, PAGE_SIZE


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
            self._get_ws_no_vcs_create_payload())["data"]
        ws_id = workspace["id"]
        ws_name = workspace["attributes"]["name"]

        # List the workspaces, confirm we have the included values
        listed_ws_raw = self._api.workspaces.list(page=PAGE_START, page_size=PAGE_SIZE, include=["organization"])
        self.assertIn("included", listed_ws_raw)

        # Test the search parameter on listing workspaces
        search_payload = {
            "name": ws_name
        }
        search_listed_ws = \
            self._api.workspaces.list(page=PAGE_START, page_size=PAGE_SIZE, search=search_payload)["data"]
        self.assertTrue(len(search_listed_ws), 1)

        # Ensure searched workspace is in the returned list
        self.assertTrue(ws_name in [ws["attributes"]["name"] for ws in search_listed_ws])

        listed_ws = listed_ws_raw["data"]
        found_ws = False
        for workspace in listed_ws:
            if workspace["id"] == ws_id:
                found_ws = True
                break
        self.assertTrue(found_ws)

        # List all the workspaces, confirm we have the included values
        all_ws = self._api.workspaces.list_all(include=["organization"])
        self.assertIn("included", all_ws)

        # Test the search parameter on list all workspaces parameter
        search_listed_ws_all = self._api.workspaces.list_all(search=search_payload)["data"]
        self.assertTrue(len(search_listed_ws_all), 1)

        # Ensure searched workspace is in the returned list
        self.assertTrue(ws_name in [ws["attributes"]["name"] for ws in search_listed_ws_all])

        found_ws = False
        for workspace in all_ws["data"]:
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
        ws_shown_by_id_raw = self._api.workspaces.show(workspace_id=ws_id, include=["organization"])
        self.assertIn("included", ws_shown_by_id_raw)
        ws_shown_by_id = ws_shown_by_id_raw["data"]
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
        raw_ws_shown_by_id = self._api.workspaces.show(workspace_id=ws_id, include=["organization", "readme"])
        self.assertIn("included", raw_ws_shown_by_id)
        self.assertNotIn("ssh-key", raw_ws_shown_by_id["data"]["relationships"])

        # Add tags to the workspace
        ws_add_tags_payload = {
            "data": [
                {
                    "type": "tags",
                    "attributes": {
                        "name": "foo"
                    }
                },
                {
                    "type": "tags",
                    "attributes": {
                        "name": "bar"
                    }
                }
            ]
        }
        self._api.workspaces.add_tags(ws_id, ws_add_tags_payload)

        # Get the tags and confirm that two were added to the workspace
        added_ws_tags = self._api.workspaces.list_tags(ws_id)["data"]
        self.assertEqual(len(added_ws_tags), len(ws_add_tags_payload["data"]))

        # Also test the list all tags function
        all_tags = self._api.workspaces.list_all_tags(ws_id)["data"]
        self.assertEqual(len(all_tags), len(ws_add_tags_payload["data"]))

        ws_resources = self._api.workspaces.list_resources(ws_id)["data"]
        self.assertEqual(len(ws_resources), 0)

        all_ws_resources = self._api.workspaces.list_all_resources(ws_id)["data"]
        self.assertEqual(len(all_ws_resources), 0)

        # Remove one tag from the workspace
        ws_remove_tags_payload = {
            "data": [
                {
                    "type": "tags",
                    "id": added_ws_tags[0]["id"]
                }
            ]

        }
        self._api.workspaces.remove_tags(ws_id, ws_remove_tags_payload)

        # Get the tags and confirm the only tag left is the one we didn't remove.
        current_ws_tags = self._api.workspaces.list_tags(ws_id)["data"]
        self.assertEqual(current_ws_tags[0]["id"], added_ws_tags[-1]["id"])

        self._api.workspaces.destroy(workspace_name=updated_name)
        listed_ws_raw = self._api.workspaces.list(include=["organization"])
        listed_ws = listed_ws_raw["data"]
        found_ws = False
        for workspace in listed_ws:
            if workspace["id"] == ws_id:
                found_ws = True
                break

        self.assertFalse(found_ws)

    def test_workspaces_remote_state_consumers(self):
        """
        Test the Workspaces Remote State Consumers API endpoints.
        """

        # Create 3 workspaces, one to add a consumer to, one to update with.
        ws1_id = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]["id"]
        ws2_id = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]["id"]
        ws3_id = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]["id"]

        gotten_consumers = self._api.workspaces.get_remote_state_consumers(ws1_id)["data"]
        self.assertEqual(len(gotten_consumers), 0)

        # Add the second workspace as a consumer to the first workspace
        add_payload = {
            "data": [
                {
                    "id": ws2_id,
                    "type": "workspaces"
                }
            ]
        }
        self._api.workspaces.add_remote_state_consumers(ws1_id, add_payload)

        # Confirm the consumers
        gotten_consumers = self._api.workspaces.get_remote_state_consumers(ws1_id)["data"]
        self.assertIn(ws2_id, gotten_consumers[0]["relationships"]["remote-state-consumers"]["links"]["related"])

        # Update to add the third workspace as a consumer of the first workspace
        replace_delete_payload = {
            "data": [
                {
                    "id": ws3_id,
                    "type": "workspaces"
                }
            ]
        }
        self._api.workspaces.replace_remote_state_consumers(ws1_id, replace_delete_payload)

        # Confirm the consumers
        gotten_consumers = self._api.workspaces.get_remote_state_consumers(ws1_id)["data"]
        self.assertIn(ws3_id, gotten_consumers[0]["relationships"]["remote-state-consumers"]["links"]["related"])

        self._api.workspaces.delete_remote_state_consumers(ws1_id, replace_delete_payload)

        # Confirm the consumers
        gotten_consumers = self._api.workspaces.get_remote_state_consumers(ws1_id)["data"]
        self.assertEqual(len(gotten_consumers), 0)

        # Destroy all workspaces
        self._api.workspaces.destroy(workspace_id=ws1_id)
        self._api.workspaces.destroy(workspace_id=ws2_id)
        self._api.workspaces.destroy(workspace_id=ws3_id)

    def test_workspaces_safe_destroy(self):
        """
        Test the Workspaces API safe destroy endpoints.
        """

        # Create 3 workspaces, one to add a consumer to, one to update with.
        ws1_id = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]["id"]
        ws2_name = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]["attributes"]["name"]

        # Safe destroy the workspaces that should not have any resources under management
        self._api.workspaces.safe_destroy(workspace_id=ws1_id)
        self._api.workspaces.safe_destroy(workspace_name=ws2_name)

        # Confirm both of the workspaces with no resources were safe destroyed.
        listed_ws = self._api.workspaces.list()["data"]
        self.assertEqual(len(listed_ws), 0)
