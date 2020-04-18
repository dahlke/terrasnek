"""
Module for testing the Terraform Cloud API Endpoint: Organization Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrganizationMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Organization Tokens.
    """

    def setUp(self):
        # TODO: figure out how to make these not spammy or burdensome
        org_create_payload = self._get_org_create_payload()
        self._created_org = self._api.organizations.create(org_create_payload)
        self._created_org_name = org_create_payload["data"]["attributes"]["name"]
        self._created_org_id = self._created_org["data"]["id"]

    def tearDown(self):
        self._api.organizations.destroy(self._created_org_name)

    def test_org_tokens_lifecycle(self):
        """
        Test the Organization Tokens API endpoints: create, destroy.
        """
        self._api.set_organization(self._created_org_id)

        # Create the token
        created_token_resp = self._api.organization_tokens.create()
        created_token_id = created_token_resp["data"]["id"]
        self.assertNotEqual(created_token_id, None)

        # Remove the token
        removed_token_resp = self._api.organization_tokens.destroy()
        self.assertEqual(removed_token_resp, None)