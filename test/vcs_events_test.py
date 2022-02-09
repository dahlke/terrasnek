"""
Module for testing the Terraform Cloud API Endpoint: VCS Events.
"""

from .base import TestTFCBaseTestCase


class TestTFCVCSEvents(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: VCS Events.
    """

    _unittest_name = "vcsevents"
    _endpoint_being_tested = "vcs_events"


    def setUp(self):
        self._oauth_client = self._api.oauth_clients.create(\
            self._get_oauth_client_create_payload())["data"]
        self._oauth_client_id = self._oauth_client["id"]

    def tearDown(self):
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_vcs_events(self):
        """
        Test the VCS Events API endpoints.
        """
        # NOTE: Currently, this feature is in beta, and only supports GitLab.
        # Since all of the testing is done with GitHub, this function is
        # provided, but you can see below that the test is not yet very good.

        # List the VCS events
        start_page = 0
        page_size = 50
        # FIXME: Test filter / include parameters GitHub is supported.
        vcs_events = self._api.vcs_events.list(page=start_page, page_size=page_size)["data"]
        self.assertEqual(len(vcs_events), 0)
