"""
Module for testing the Terraform Cloud API Endpoint: OAuth Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCOAuthTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: OAuth Tokens.
    """

    def setUp(self):
        unittest_name = "oauth-tokens"
        oauth_client_payload = self._get_oauth_client_create_payload(
            unittest_name)
        self._oauth_client = self._api.oauth_clients.create(oauth_client_payload)[
            "data"]
        self._oauth_client_id = self._oauth_client["id"]

    def tearDown(self):
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_oauth_tokens_endpoints(self):
        """
        Test the OAuth Tokens API endpoints: list, show.
        """

        # List all the tokens and make sure there is one associate to your client
        oauth_tokens = self._api.oauth_tokens.list(
            self._oauth_client_id)["data"]
        self.assertEqual(len(oauth_tokens), 1)

        # Make sure the OAuth client parent is as expected
        parent_oauth_client_id = oauth_tokens[0]["relationships"]["oauth-client"]["data"]["id"]
        self.assertEqual(parent_oauth_client_id, self._oauth_client_id)

        # Look up the token by it's ID and make sure the results are as expected
        oauth_token_id = oauth_tokens[0]["id"]
        shown_oauth_token = self._api.oauth_tokens.show(oauth_token_id)
        self.assertEqual(oauth_token_id, shown_oauth_token["data"]["id"])
