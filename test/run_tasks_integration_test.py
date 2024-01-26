"""
Module for testing the Terraform Cloud API Endpoint: Run Tasks Integration.
"""

from .base import TestTFCBaseTestCase


class TestTFCRunTaskIntegration(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Run Tasks Integration.
    """

    _unittest_name = "run-tint"
    _endpoint_being_tested = "run_tasks_integration"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_name)

    def test_run_tasks_integration(self):
        """
        Test the Run Tasks Integration API endpoints.
        """
        # TODO: These will be fairly difficult to create valuable tests for.
