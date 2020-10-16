"""
Module for testing the Terraform Cloud API Endpoint: Orgs.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrgs(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Orgs.
    """

    _unittest_name = "orgs"
    _endpoint_being_tested = "orgs"

    def test_orgs(self):
        """
        Test the Orgs API endpoints.
        """

        # Create an org, confirm it was created.
        created_org = self._api.orgs.create(self._get_org_create_payload())["data"]
        created_org_id = created_org["id"]
        created_org_name = created_org["attributes"]["name"]
        all_orgs = self._api.orgs.list()["data"]
        self.assertNotEqual(
            len(all_orgs), 0, msg="No organizations found for TFC token.")

        # List entitlements, confirm expected response
        ent = self._api.orgs.entitlements(self._test_org_name)["data"]
        self.assertEqual(ent["type"], "entitlement-sets")
        self.assertTrue(ent["attributes"]["state-storage"])

        # Show the org, confirm IDs match
        org = self._api.orgs.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)

        # Change the email address for the org, confirm the change.
        email_name = self._unittest_random_name()
        email_to_update_to = f"{email_name}@gmail.com"
        update_org_payload = {
            "data": {
                "type": "organizations",
                "attributes": {
                    "email": email_to_update_to
                }
            }
        }
        updated_org = self._api.orgs.update(
            self._test_org_name, update_org_payload)
        self.assertEqual(updated_org["data"]
                         ["attributes"]["email"], email_to_update_to)

        # Destroy the org, confirm it's gone
        self._api.orgs.destroy(created_org_name)
        all_orgs = self._api.orgs.list()["data"]
        found_org = False
        for org in all_orgs:
            if org["id"] == created_org_id:
                found_org = True
                break
        self.assertFalse(found_org)
