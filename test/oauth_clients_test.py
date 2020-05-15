"""
Module for testing the Terraform Cloud API Endpoint: OAuth Clients.
"""

from .base import TestTFCBaseTestCase


class TestTFCOAuthClients(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: OAuth Clients.
    """

    _unittest_name = "oa-clients"
    _endpoint_being_tested = "oauth_clients"

    def test_oauth_clients(self):
        """
        Test the OAuth Clients API endpoints: ``list``, ``create``, ``show``, ``destroy``.
        """

        # Create a test OAuth client
        oauth_clients = self._api.oauth_clients.list()["data"]
        num_clients_before_add = len(oauth_clients)
        oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())

        # List the OAuth clients and confirm there is one.
        oauth_clients = self._api.oauth_clients.list()["data"]
        num_clients_after_add = len(oauth_clients)
        self.assertNotEqual(num_clients_after_add, num_clients_before_add)

        # Confirm we can show that OAuth client with it's ID and it matches the created
        oauth_client_id = oauth_clients[0]["id"]
        oauth_client = self._api.oauth_clients.show(oauth_client_id)["data"]
        self.assertEqual(oauth_client["id"], oauth_client_id)

        # Destroy the test OAuth client and confirm there are none left
        self._api.oauth_clients.destroy(oauth_client_id)
        oauth_clients = self._api.oauth_clients.list()["data"]
        num_clients_after_delete = len(oauth_clients)
        self.assertNotEqual(num_clients_after_add, num_clients_after_delete)
