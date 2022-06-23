"""
Module for testing the Terraform Cloud API Endpoint: Admin Workspaces.
"""

from .base import TestTFCBaseTestCase
from ._constants import PAGE_START, PAGE_SIZE


class TestTFCAdminWorkspaces(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Workspaces.
    """

    _unittest_name = "adm-ws"
    _endpoint_being_tested = "admin_workspaces"

    def setUp(self):
        # Create a sample workspace to manipulate in the test.
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]
        self._created_ws_id = self._ws["id"]
        self._created_ws_name = self._ws["attributes"]["name"]

    def test_admin_workspaces(self):
        """
        Test the Admin Workspaces API endpoints.
        """

        search_payload = {
            "name": self._created_ws_name
        }
        # List all the workspaces, confirm the one we created in the setup exists
        all_ws_raw = self._api.admin_workspaces.list(\
            search=search_payload, filters=None, page=PAGE_START, page_size=PAGE_SIZE, \
                sort="name", include=["organization"])
        self.assertIn("included", all_ws_raw)

        all_ws = all_ws_raw["data"]
        found_ws = False
        for workspace in all_ws:
            ws_id = workspace["id"]
            if ws_id == self._created_ws_id:
                found_ws = True
                break
        self.assertTrue(found_ws)

        # Show the workspace by the ID, confirm we get the expected ID back
        shown_ws = self._api.admin_workspaces.show(self._created_ws_id)["data"]
        self.assertEqual(self._created_ws_id, shown_ws["id"])

        # Destroy the workspace that we created, verify it's gone
        self._api.admin_workspaces.destroy(self._created_ws_id)
        all_ws = self._api.admin_workspaces.list()["data"]
        found_ws = False
        for workspace in all_ws:
            ws_id = workspace["id"]
            if ws_id == self._created_ws_id:
                found_ws = True
                break
        self.assertFalse(found_ws)
