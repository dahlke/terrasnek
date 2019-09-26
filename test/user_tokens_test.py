"""
Module for testing the Terraform Enterprise API Endpoint: User Tokens.
"""

from .base import TestTFEBaseTestCase


class TestTFEUserTokens(TestTFEBaseTestCase):
    """
    Class for testing the Terraform Enterprise API Endpoint: User Tokens.
    """

    def test_user_token_lifecycle(self):
        """
        Test the User Token API endpoints: list, create, show, destroy.
        """

        # TODO: fix this once the User API is patched.
        # users = self._api.admin_users.lst(query=self._test_username)["data"]
        # self.assertNotEqual(len(users), 0)
        # user_id = users[0]['id']

        # created_token = \
        #   self._api.user_tokens.create(user_id, self._user_token_create_payload)["data"]
        # created_token_id = created_token["id"]
        # print("created", created_token)

        # shown_token = self._api.user_tokens.show(created_token_id)
        # print("shown", shown_token)

        # listed_tokens = self._api.user_tokens.lst(user_id)
        # print("listed", listed_tokens)

        # self._api.user_tokens.destroy(created_token_id)
        # print("destroyed")

        # listed_tokens = self._api.user_tokens.lst(user_id)
        # print("listed", listed_tokens)
