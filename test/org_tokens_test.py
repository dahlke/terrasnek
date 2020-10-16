"""
Module for testing the Terraform Cloud API Endpoint: Org Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrgTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Org Tokens.
    """

    _unittest_name = "org-tok"
    _endpoint_being_tested = "org_tokens"

    def setUp(self):
        # Create a temp org to manipulate in the test.
        created_org = self._api.orgs.create(self._get_org_create_payload())["data"]
        self._created_org_name = created_org["attributes"]["name"]
        self._created_org_id = created_org["id"]

    def tearDown(self):
        self._api.orgs.destroy(self._created_org_name)

    def test_org_tokens(self):
        """
        Test the Org Tokens API endpoints.
        """

        self._api.set_org(self._created_org_id)

        # Create the token, confirm it was created
        created_token = self._api.org_tokens.create()["data"]
        created_token_id = created_token["id"]
        self.assertIsNotNone(created_token_id)

        # Remove the token, confirm it the request worked (no response)
        # since we don't have a way to look for them otherwise.
        removed_token_resp = self._api.org_tokens.destroy()
        self.assertIsNone(removed_token_resp)
