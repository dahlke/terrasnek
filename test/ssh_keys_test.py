"""
Module for testing the Terraform Cloud API Endpoint: SSH Keys.
"""

from .base import TestTFCBaseTestCase


SSH_KEY_NAME_TO_UPDATE_TO = "foo"

class TestTFCSSHKeys(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: SSH Keys.
    """

    _unittest_name = "ssh-keys"
    _endpoint_being_tested = "ssh_keys"

    def test_ssh_keys(self):
        """
        Test the SSH Keys API endpoints.
        """

        all_ssh_keys = self._api.ssh_keys.list()["data"]
        self.assertEqual(len(all_ssh_keys), 0)

        # Add an SSH Key to TFC
        created_key = self._api.ssh_keys.create(self._get_ssh_key_create_payload())["data"]
        created_key_id = created_key["id"]

        # Check that we now have one key
        all_ssh_keys = self._api.ssh_keys.list()["data"]
        self.assertEqual(len(all_ssh_keys), 1)

        # Show the key we just created
        shown_key = self._api.ssh_keys.show(created_key_id)["data"]
        shown_key_id = shown_key["id"]
        self.assertEqual(shown_key_id, created_key_id)

        # Update the key we just showed
        update_payload = {
            "data": {
                "attributes": {
                    "name": SSH_KEY_NAME_TO_UPDATE_TO
                }
            }
        }
        updated_key = self._api.ssh_keys.update(created_key_id, update_payload)["data"]
        updated_key_name = updated_key["attributes"]["name"]
        self.assertEqual(SSH_KEY_NAME_TO_UPDATE_TO, updated_key_name)

        # Delete the key we just updated, confirm it's gone
        self._api.ssh_keys.destroy(created_key_id)
        all_ssh_keys = self._api.ssh_keys.list()["data"]
        self.assertEqual(len(all_ssh_keys), 0)
