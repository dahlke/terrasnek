"""
Module for testing the Terraform Cloud API Endpoint: Admin Workspaces.
"""

from .base import TestTFCBaseTestCase


class TestTFCAdminWorkspaces(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Workspaces.
    """

    def setUp(self):
        self._ws = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("admin-ws"))["data"]
        self._created_ws_id = self._ws["id"]

    def test_admin_workspaces(self):
        """
        Test the Admin Workspaces API endpoints: list, show, destroy.
        """
        # TODO: test the parameters
        all_ws = self._api.admin_workspaces.list()["data"]

        found_ws = False
        for ws in all_ws:
            ws_id = ws["id"]
            if ws_id == self._created_ws_id:
                found_ws = True
                break
        self.assertTrue(found_ws)

        shown_ws = self._api.admin_workspaces.show(self._created_ws_id)["data"]
        self.assertTrue(self._created_ws_id, shown_ws["id"])

        # Destroy the ws that we created, verify it's gone.
        self._api.admin_workspaces.destroy(self._created_ws_id)
        all_ws = self._api.admin_workspaces.list()["data"]
        found_ws = False
        for ws in all_ws:
            ws_id = ws["id"]
            if ws_id == self._created_ws_id:
                found_ws = True
                break
        self.assertFalse(found_ws)