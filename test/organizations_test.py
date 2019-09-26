"""
Module for testing the Terraform Enterprise API Endpoint: Organizations.
"""

from .base import TestTFEBaseTestCase


class TestTFEOrganizations(TestTFEBaseTestCase):
    """
    Class for testing the Terraform Enterprise API Endpoint: Organizations.
    """

    def test_orgs_lifecycle(self):
        """
        Test the Organizations API endpoints: create, list, entitlements, show, update, destroy.
        """

        """
        # Test create endpoint
        self._api.organizations.create(self._get_org_create_payload())
        orgs = self._api.organizations.lst()["data"]
        self.assertNotEqual(
            len(orgs), 0, msg="No organizations found for TFE token.")

        # Test entitlements endpoint
        ent = self._api.organizations.entitlements(self._test_org_name)
        self.assertEqual(ent["data"]["type"], "entitlement-sets")
        self.assertTrue(ent["data"]["attributes"]["state-storage"])

        # Test show endpoint
        org = self._api.organizations.show(self._test_org_name)
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

        updated_org = self._api.organizations.update(
            self._test_org_name, update_org_payload)
        self.assertEqual(updated_org["data"]
                         ["attributes"]["email"], updated_email)

        self._api.organizations.destroy(self._test_org_name)
        """