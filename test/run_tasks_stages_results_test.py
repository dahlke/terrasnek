"""
Module for testing the Terraform Cloud API Endpoint: Run Tasks Stages and Results.
"""

from .base import TestTFCBaseTestCase


class TestTFCRunTaskStagesResults(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Run Tasks Stages Results.
    """

    _unittest_name = "run-tsr"
    _endpoint_being_tested = "run_tasks_stages_results"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_name)

    def test_run_tasks_stages_results(self):
        """
        Test the Run Tasks Stages and Results API endpoints.
        """
        # TODO: These will be fairly difficult to create valuable tests for.

