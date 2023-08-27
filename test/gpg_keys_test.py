"""
Module for testing the Terraform Cloud API Endpoint: GPG Keys.
"""

from terrasnek.exceptions import TFCHTTPUnprocessableEntity
from .base import TestTFCBaseTestCase


class TestTFCGPGKeys(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: GPG Keys.
    """

    _unittest_name = "gpgk"
    _endpoint_being_tested = "gpg_keys"

    def test_gpg_keys(self):
        """
        Test the GPG Keys API endpoints.
        """

        # List the GPG keys
        gpg_keys = self._api.gpg_keys.list()["data"]
        self.assertEqual(0, len(gpg_keys))

        gpg_key_contents = None

        with open("./test/testdata/test_gpg.key", "r") as f:
            gpg_key_contents = f.read()

        # Create a GPG key
        create_payload = {
            "data": {
                "type": "gpg-keys",
                "attributes": {
                "namespace": self._test_org_name,
                "ascii-armor": gpg_key_contents
                }
            }
        }
        created_key = self._api.gpg_keys.create(payload=create_payload)["data"]
        self.assertEqual(created_key["type"], "gpg-keys")

        # Update the GPG key
        # NOTE: no test for this as I do not want to move GPG keys around namespaces, which is
        # all this supports right now

        all_gpg_keys = self._api.gpg_keys.list_all()["data"]
        self.assertEqual(1, len(all_gpg_keys))

        # Delete the GPG key
        self._api.gpg_keys.destroy(created_key["attributes"]["key-id"])

        # Confirm the GPG key has been deleted
        gpg_keys = self._api.gpg_keys.list()["data"]
        self.assertEqual(0, len(gpg_keys))

