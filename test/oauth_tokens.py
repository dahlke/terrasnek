import unittest
import os
from .base import TestTFEBaseTestCase

from terrasnek.api import TFE


class TestTFEOAuthTokens(TestTFEBaseTestCase):

    def test_oauth_tokens_lifecycle(self):
        # Create a test OAuth client
        self._api.oauth_clients.create(self._oauth_client_create_payload)
        oauth_clients = self._api.oauth_clients.lst()["data"]
        self.assertEqual(len(oauth_clients), 1)

        # Verify there is an associated token
        oauth_client_id = oauth_clients[0]["id"]
        oauth_tokens = self._api.oauth_tokens.lst(oauth_client_id)["data"]
        self.assertEqual(len(oauth_tokens), 1)

        parent_oauth_client_id = oauth_tokens[0]["relationships"]["oauth-client"]["data"]["id"]
        self.assertEqual(parent_oauth_client_id, oauth_client_id)

        # Look up the token by it's ID and make sure the results are as expected
        oauth_token_id = oauth_tokens[0]["id"]
        shown_oauth_token = self._api.oauth_tokens.show(oauth_token_id)
        self.assertEqual(oauth_token_id, shown_oauth_token["data"]["id"])

        # Destroy the test OAuth client
        self._api.oauth_clients.destroy(oauth_client_id)
        oauth_clients = self._api.oauth_clients.lst()["data"]
        self.assertEqual(len(oauth_clients), 0)
