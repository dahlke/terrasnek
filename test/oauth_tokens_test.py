"""
Module for testing the Terraform Cloud API Endpoint: OAuth Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCOAuthTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: OAuth Tokens.
    """

    _unittest_name = "oa-tokens"
    _endpoint_being_tested = "oauth_tokens"

    def setUp(self):
        self._oauth_client = self._api.oauth_clients.create(\
            self._get_oauth_client_create_payload())["data"]
        self._oauth_client_id = self._oauth_client["id"]

    def tearDown(self):
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_oauth_tokens(self):
        """
        Test the OAuth Tokens API endpoints.
        """

        # List all the tokens and make sure there is one associated to your client
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

        # Create an empty update payload (it requires a real Git SSH key), so publish
        # an update and verify the response type is what we expect
        update_payload = {
            "data": {
                "id": oauth_token_id,
                "type": "oauth-tokens",
                "attributes": {
                }
            }
        }
        updated_oauth_token = self._api.oauth_tokens.update(oauth_token_id, update_payload)["data"]
        self.assertEqual("oauth-tokens", updated_oauth_token["type"])

        # Delete the OAuth token and confirm it's no longer present
        self._api.oauth_tokens.destroy(oauth_token_id)
        oauth_tokens = self._api.oauth_tokens.list(
            self._oauth_client_id)["data"]

        found_token = False
        for oauth_token in oauth_tokens:
            if oauth_token_id == oauth_token["id"]:
                found_token = True
                break
        self.assertFalse(found_token)
