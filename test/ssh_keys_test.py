"""
Module for testing the Terraform Cloud API Endpoint: SSH Keys.
"""

from .base import TestTFCBaseTestCase


class TestTFCSSHKeys(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: SSH Keys.
    """

    def test_ssh_keys_lifecycle(self):
        """
        Test the SSH Keys API endpoints: create, list, show,
        update, destroy.
        """

        ssh_keys_resp = self._api.ssh_keys.list()
        ssh_keys = ssh_keys_resp["data"]
        self.assertEqual(len(ssh_keys), 0)

        # Add an SSH Key to TFC
        create_payload = self._get_ssh_key_create_payload()
        create_resp = self._api.ssh_keys.create(create_payload)
        created_key = create_resp["data"]
        created_key_id = created_key["id"]

        # Check that we now have one key
        ssh_keys_resp = self._api.ssh_keys.list()
        ssh_keys = ssh_keys_resp["data"]
        self.assertEqual(len(ssh_keys), 1)

        # Show the key we just created
        shown_resp = self._api.ssh_keys.show(created_key_id)
        shown_key = shown_resp["data"]
        shown_key_id = shown_key["id"]
        self.assertEqual(shown_key_id, created_key_id)

        # Update the key we just showed
        name_to_update_to = "foo"
        update_payload = {
            "data": {
                "attributes": {
                    "name": name_to_update_to
                }
            }
        }
        update_resp = self._api.ssh_keys.update(created_key_id, update_payload)
        updated_key = update_resp["data"]
        updated_key_name = updated_key["attributes"]["name"]
        self.assertEqual(name_to_update_to, updated_key_name)

        # Delete the key we just updated
        self._api.ssh_keys.destroy(created_key_id)

        # Check that we now have zero keys again
        ssh_keys_resp = self._api.ssh_keys.list()
        ssh_keys = ssh_keys_resp["data"]
        self.assertEqual(len(ssh_keys), 0)
