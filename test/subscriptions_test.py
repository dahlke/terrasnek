"""
Module for testing the Terraform Cloud API Endpoint: Subscriptions.
"""

from .base import TestTFCBaseTestCase


class TestTFCSubscriptions(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Subscriptions.
    """

    _unittest_name = "subsc"
    _endpoint_being_tested = "subscriptions"

    def test_subscriptions(self):
        """
        Test the Subscriptions API endpoints.
        """
        subs = self._api.subscriptions.show()["data"]
        sub_id = subs["id"]
        self.assertEqual(subs["type"], "subscriptions")

        sub = self._api.subscriptions.show_by_id(sub_id)["data"]
        self.assertEqual(sub["id"], sub_id)
