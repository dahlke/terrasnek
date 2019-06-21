import unittest
import os
from .base import TestTFEBaseTestCase

from tfepy.api import TFE


class TestTFEWorkspaces(TestTFEBaseTestCase):

    def test_workspaces_create(self):
        # TODO: How to manage VCS OAuth and create w/ VCS payload?
        ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 1)

        self._api.workspaces.destroy_by_name(ws["data"]["attributes"]["name"])
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 0)
    
    def test_destroy(self):
        # Create a workspace
        ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 1)

        # Destroy it with it's name
        ws_name = ws["data"]["attributes"]["name"]
        self._api.workspaces.destroy_by_name(ws_name)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 0)

        # Create another workspace
        ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 1)

        # Destroy it with it's ID
        ws_id = ws["data"]["id"]
        self._api.workspaces.destroy_by_id(ws_id)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 0)
    
    def test_workspaces_lock_unlock(self):
        # Create a workspace and make sure it's not locked
        ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        ws_id = ws["data"]["id"]
        self.assertFalse(ws["data"]["attributes"]["locked"])

        # Lock the workspace and confirm it's locked
        ws_locked = self._api.workspaces.lock(ws_id, {"reason": "Unit testing."})
        self.assertTrue(ws_locked["data"]["attributes"]["locked"])

        # Unlock the workspace and confirm it's unlocked
        ws_unlocked = self._api.workspaces.unlock(ws_id)
        self.assertFalse(ws_unlocked["data"]["attributes"]["locked"])

        # Relock the workspace and confirm it's locked
        ws_relocked = self._api.workspaces.lock(ws_id, {"reason": "Unit testing."})
        self.assertTrue(ws_locked["data"]["attributes"]["locked"])
        
        # Force an unlock and confirm its unlocked
        ws_forced = self._api.workspaces.force_unlock(ws_id)
        self.assertFalse(ws_forced["data"]["attributes"]["locked"])

        # Clean up the workspace
        self._api.workspaces.destroy_by_id(ws_id)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 0)
    
    def test_workspaces_show(self):
        # Create a workspace
        ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 1)

        # Get that workspace's ID, retrieve it's data and compare IDs
        ws_id = ws["data"]["id"]
        ws_shown_by_id = self._api.workspaces.show_by_id(ws_id)
        self.assertEqual(ws_id, ws_shown_by_id["data"]["id"])

        # Get that workspace's name, retrieve it's data and compare names
        ws_name = ws["data"]["attributes"]["name"]
        ws_shown_by_name = self._api.workspaces.show_by_name(ws_name)
        self.assertEqual(ws_name, ws_shown_by_name["data"]["attributes"]["name"])

        # Clean up the workspace
        self._api.workspaces.destroy_by_id(ws_id)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 0)

    def test_workspaces_update(self):
        # Create a workspace
        ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 1)

        # Get that workspace's ID, and update it's name
        ws_id = ws["data"]["id"]
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
        self.assertEqual(updated_name, ws_updated["data"]["attributes"]["name"])

        # Clean up the workspace
        self._api.workspaces.destroy_by_id(ws_id)
        workspaces = self._api.workspaces.ls()["data"]
        self.assertEqual(len(workspaces), 0)