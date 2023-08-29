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
        orgs = self._api.orgs.list()["data"]
        self.assertNotEqual(
            len(orgs), 0, msg="No organizations found for TFC token.")

        # List entitlements, confirm expected response
        ent = self._api.orgs.entitlements(self._test_org_name)["data"]
        self.assertEqual(ent["type"], "entitlement-sets")
        self.assertTrue(ent["attributes"]["state-storage"])

        # List subscription details, confirm expected response
        if self._api.is_terraform_cloud():
            # This only works on TFC, so skip it if we're on TFE.
            sub = self._api.orgs.subscription(self._test_org_name)["data"]
            if "included" in sub:
                # If "included" is present, it's an active subscription
                self.assertEqual(sub["type"], "subscriptions")
                self.assertIn("identifier", sub["included"][0]["attributes"])
            else:
                # Otherwise, make sure it's a free tier subscription
                self.assertTrue(sub["attributes"]["is-public-free-tier"])

        # Show the org, confirm IDs match
        org = self._api.orgs.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)

        # NOTE: The module producers endpoint does not work on TFC.
        if not self._api.is_terraform_cloud():
            mod_producers = self._api.orgs.show_module_producers(self._test_org_name)
            # Check that we receive a valid module producers response
            self.assertIn("module-producers", mod_producers["links"]["self"])
            # And that the newly created org has no module producers
            self.assertEqual(len(mod_producers["data"]), 0)

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
        self.assertEqual(updated_org["data"] \
                         ["attributes"]["email"], email_to_update_to)

        all_orgs = self._api.orgs.list_all()["data"]
        self.assertNotEqual(
            len(all_orgs), 0, msg="No organizations found for TFC token.")

        # Destroy the org, confirm it's gone
        self._api.orgs.destroy(created_org_name)
        all_orgs = self._api.orgs.list()["data"]
        found_org = False
        for org in all_orgs:
            if org["id"] == created_org_id:
                found_org = True
                break
        self.assertFalse(found_org)
