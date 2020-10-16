"""
Module for testing the Terraform Cloud API Endpoint: Admin Orgs.
"""

from .base import TestTFCBaseTestCase


class TestTFCAdminOrgs(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Orgs.
    """

    _unittest_name = "adm-org"
    _endpoint_being_tested = "admin_orgs"

    def setUp(self):
        # Create a temp org to manipulate in the test
        created_org = self._api.orgs.create(self._get_org_create_payload())["data"]
        self._created_org_name = created_org["attributes"]["name"]
        self._created_org_id = created_org["id"]

    def test_admin_orgs(self):
        """
        Test the Admin Orgs API endpoints.
        """

        # List all the orgs, confirm the created one is present
        all_orgs = self._api.admin_orgs.list()["data"]
        found_created_org = False
        for org in all_orgs:
            org_id = org["id"]
            if org_id == self._created_org_id:
                found_created_org = True
                break
        self.assertTrue(found_created_org)

        # Show the created org, confirm it matches the created org's ID
        shown_org = self._api.admin_orgs.show(self._created_org_name)["data"]
        self.assertEqual(self._created_org_id, shown_org["id"])

        # Destroy the org that we created, verify it's gone.
        self._api.admin_orgs.destroy(self._created_org_name)
        all_orgs = self._api.admin_orgs.list()["data"]
        found_created_org = False
        for org in all_orgs:
            org_id = org["id"]
            if org_id == self._created_org_id:
                found_created_org = True
                break
        self.assertFalse(found_created_org)
