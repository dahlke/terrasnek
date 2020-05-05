"""
Module for testing the Terraform Cloud API Endpoint: Orgs.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrgs(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Orgs.
    """

    def test_orgs_lifecycle(self):
        """
        Test the Orgs API endpoints: create, list, entitlements, show, update, destroy.
        """
        # Test create endpoint
        created_org = self._api.orgs.create(self._get_org_create_payload())["data"]
        created_org_name = created_org["attributes"]["name"]
        orgs = self._api.orgs.list()["data"]
        self.assertNotEqual(
            len(orgs), 0, msg="No organizations found for TFC token.")

        # Test entitlements endpoint
        ent = self._api.orgs.entitlements(self._test_org_name)["data"]
        self.assertEqual(ent["type"], "entitlement-sets")
        self.assertTrue(ent["attributes"]["state-storage"])

        # Test show endpoint
        org = self._api.orgs.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)

        # Test update endpoint
        updated_email = "neil+terrasnek-unittest@hashicorp.com"
        update_org_payload = {
            "data": {
                "type": "organizations",
                "attributes": {
                    "email": updated_email
                }
            }
        }

        updated_org = self._api.orgs.update(
            self._test_org_name, update_org_payload)
        self.assertEqual(updated_org["data"]
                         ["attributes"]["email"], updated_email)

        self._api.orgs.destroy(created_org_name)
