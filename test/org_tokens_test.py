"""
Module for testing the Terraform Cloud API Endpoint: Org Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrgTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Org Tokens.
    """

    _unittest_name = "org-tok"

    def setUp(self):
        # Create a temp org to manipulate in the test.
        org_create_payload = self._get_org_create_payload()
        self._created_org = self._api.orgs.create(org_create_payload)
        self._created_org_name = org_create_payload["data"]["attributes"]["name"]
        self._created_org_id = self._created_org["data"]["id"]

    def tearDown(self):
        self._api.orgs.destroy(self._created_org_name)

    def test_org_tokens(self):
        """
        Test the Org Tokens API endpoints: ``create``, ``destroy``.
        """
        self._api.set_org(self._created_org_id)

        # Create the token, confirm it was created
        created_token_resp = self._api.org_tokens.create()
        created_token_id = created_token_resp["data"]["id"]
        self.assertNotEqual(created_token_id, None)

        # Remove the token, confirm it was removed
        removed_token_resp = self._api.org_tokens.destroy()
        self.assertEqual(removed_token_resp, None)
