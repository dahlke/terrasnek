"""
Module for testing the Terraform Cloud API Endpoint: User Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCUserTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: User Tokens.
    """

    _unittest_name = "user-tok"
    _endpoint_being_tested = "user_tokens"

    def test_user_tokens(self):
        """
        Test the User Tokens API endpoints.
        """

        logged_in_user = self._api.account.show()["data"]
        logged_in_user_id = logged_in_user["id"]

        desc_to_update_to = self._unittest_random_name()
        create_payload = {
            "data": {
                "type": "authentication-tokens",
                "attributes": {
                    "description": desc_to_update_to
                }
            }
        }
        created_token = self._api.user_tokens.create(logged_in_user_id, create_payload)["data"]
        created_token_id = created_token["id"]

        tokens = self._api.user_tokens.list(logged_in_user_id)["data"]
        found_token = False
        for token in tokens:
            if token["id"] == created_token_id:
                found_token = True
                break
        self.assertTrue(found_token)

        self._api.user_tokens.destroy(created_token_id)

        tokens = self._api.user_tokens.list(logged_in_user_id)["data"]
        found_token = False
        for token in tokens:
            if token["id"] == created_token_id:
                found_token = True
                break
        self.assertFalse(found_token)
