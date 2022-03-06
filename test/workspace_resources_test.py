"""
Module for testing the Terraform Cloud API Endpoint: Workspace Resources.
"""

from .base import TestTFCBaseTestCase


class TestTFCWorkspaceResources(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Workspace Resources.
    """

    _unittest_name = "ws-rsrc"
    _endpoint_being_tested = "workspace_resources"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)

    def test_workspace_resources(self):
        """
        Test the Workspace Resources API endpoints.
        """

        listed_resources = self._api.workspace_resources.list(self._ws_id)["data"]
        self.assertEqual(len(listed_resources), 0)
