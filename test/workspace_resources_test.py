"""
Module for testing the Terraform Cloud API Endpoint: Workspace Variables.
"""

from .base import TestTFCBaseTestCase


class TestTFCWorkspaceVars(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Workspace Variables.
    """

    _unittest_name = "ws-vars"
    _endpoint_being_tested = "workspace_vars"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(
            workspace_name=self._ws_name)

    def test_workspace_variables(self):
        """
        Test the Workspace Variables API endpoints.
        """

        listed_resources = self._api.workspace_resources.list(self._ws_id)["data"]
        print(listed_resources)
