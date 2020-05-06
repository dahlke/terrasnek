"""
Module for testing the Terraform Cloud API Endpoint: Admin Orgs.
"""

from .base import TestTFCBaseTestCase


class TestTFCAdminOrgs(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Orgs
    """

    def setUp(self):
        org_create_payload = self._get_org_create_payload()
        self._created_org = self._api.orgs.create(org_create_payload)
        self._created_org_name = org_create_payload["data"]["attributes"]["name"]
        self._created_org_id = self._created_org["data"]["id"]

    def test_admin_orgs(self):
        """
        Test the Admin Orgs API endpoints: list, show, destroy.
        """
        all_orgs = self._api.admin_orgs.list()["data"]
        found_created_org = False
        for org in all_orgs:
            org_id = org["id"]
            if org_id == self._created_org_id:
                found_created_org = True
                break
        self.assertTrue(found_created_org)

        shown_org = self._api.admin_orgs.show(self._created_org_name)["data"]
        self.assertTrue(self._created_org_id, shown_org["id"])

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