"""
Module for testing the Terraform Cloud API Endpoint: Users.
"""

from .base import TestTFCBaseTestCase


class TestTFCUsers(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Users.
    """

    _unittest_name = "users"
    _endpoint_being_tested = "users"

    def test_users(self):
        """
        Test the Users API endpoints.
        """

        logged_in_user = self._api.account.show()["data"]
        logged_in_user_id = logged_in_user["id"]

        shown_user = self._api.users.show(logged_in_user_id)["data"]
        self.assertEqual(logged_in_user_id, shown_user["id"])
