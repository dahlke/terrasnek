"""
Module for testing the Terraform Cloud API Endpoint: Admin Orgs.
"""

from .base import TestTFCBaseTestCase
from ._constants import PAGE_START, PAGE_SIZE


class TestTFCAdminOrgs(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Orgs.
    """

    _unittest_name = "adm-org"
    _endpoint_being_tested = "admin_orgs"

    def test_admin_orgs(self):
        """
        Test the Admin Orgs API endpoints.
        """
        # Create a temp org to manipulate in the test
        created_org = self._api.orgs.create(self._get_org_create_payload())["data"]
        created_org_name = created_org["attributes"]["name"]
        created_org_id = created_org["id"]

        # List all the orgs, confirm the created one is present. Confirm related resources
        # are return.
        all_orgs_raw = self._api.admin_orgs.list(include=["owners"])
        self.assertIn("included", all_orgs_raw)

        all_orgs = all_orgs_raw["data"]
        found_created_org = False
        for org in all_orgs:
            org_id = org["id"]
            if org_id == created_org_id:
                found_created_org = True
                break
        self.assertTrue(found_created_org)

        # Change the email address for the org, confirm the change.
        update_org_payload = {
            "data": {
                "type": "organizations",
                "attributes": {
                    "global-module-sharing": True
                }
            }
        }
        updated_org = self._api.admin_orgs.update(self._test_org_name, update_org_payload)["data"]
        self.assertTrue(updated_org["attributes"]["global-module-sharing"])

        # Show the created org, confirm it matches the created org's ID, confirm related
        # resources are returned
        shown_org_raw = self._api.admin_orgs.show(created_org_name, include=["owners"])
        self.assertIn("included", all_orgs_raw)

        shown_org = shown_org_raw["data"]
        self.assertEqual(created_org_id, shown_org["id"])

        mod_consumers = self._api.admin_orgs.list_org_module_consumers(\
            self._test_org_name, page=PAGE_START, page_size=PAGE_SIZE)["data"]
        self.assertEqual(len(mod_consumers), 0)

        mod_consumer_update_payload = {
            "data": [
                {
                    "id": created_org_name,
                    "type": "organizations"
                }
            ]
        }
        self._api.admin_orgs.update_org_module_consumers(\
            self._test_org_name, mod_consumer_update_payload)

        mod_consumers = self._api.admin_orgs.list_org_module_consumers(self._test_org_name)["data"]
        self.assertEqual(mod_consumers[0]["id"], created_org_name)

        # Destroy the org that we created, verify it's gone.
        self._api.admin_orgs.destroy(created_org_name)
        all_orgs = self._api.admin_orgs.list()["data"]
        found_created_org = False
        for org in all_orgs:
            org_id = org["id"]
            if org_id == created_org_id:
                found_created_org = True
                break
        self.assertFalse(found_created_org)
