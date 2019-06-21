import unittest
import os
from .base import TestTFEBaseTestCase

from tfepy.api import TFE


class TestTFEOAuthClients(TestTFEBaseTestCase):

    def test_oauth_clients_lifecycle(self):
        # Create a test OAuth client
        oauth_client = self._api.oauth_clients.create(self._oauth_client_create_payoad)
        oauth_clients = self._api.oauth_clients.ls()["data"]
        self.assertEqual(len(oauth_clients), 1)

        # Confirm we can show that OAuth client with it's ID
        oauth_client_id = oauth_clients[0]["id"]
        oauth_client = self._api.oauth_clients.show(oauth_client_id)["data"]
        self.assertEqual(oauth_client["id"], oauth_client_id)

        # Destroy the test OAuth client
        self._api.oauth_clients.destroy(oauth_client_id)
        oauth_clients = self._api.oauth_clients.ls()["data"]
        self.assertEqual(len(oauth_clients), 0)