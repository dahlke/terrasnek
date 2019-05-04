import unittest
import os

from tfepy.api import TFE

TOKEN = os.getenv("TFE_TOKEN", None)

class TestTFEOrganzations(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._api = TFE(TOKEN)
        self._test_email = "neil@hashicorp.com"
        self._test_org_name = "pytfe-unittest"
        self._create_payload = {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": self._test_org_name,
                    "email": self._test_email
                }
            }
        }

    def test_orgs_ls(self):
        self._api.organizations.create(self._create_payload)
        orgs = self._api.organizations.ls()["data"]
        self._api.organizations.destroy(self._test_org_name)
        self.assertNotEqual(len(orgs), 0, msg="No organizations found for TFE token.")

    def test_orgs_show(self):
        self._api.organizations.create(self._create_payload)
        org = self._api.organizations.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)
        self._api.organizations.destroy(self._test_org_name)
    
    def test_orgs_create(self):
        new_org = self._api.organizations.create(self._create_payload)
        self._api.organizations.destroy(self._test_org_name)
        self.assertEqual(new_org["data"]["id"], self._test_org_name)

    def test_orgs_update(self):
        updated_email = "neil+pytfe-unittest@hashicorp.com"
        new_org = self._api.organizations.create(self._create_payload)
        self.assertEqual(new_org["data"]["attributes"]["email"], self._test_email)

        update_payload = {
            "data": {
                "type": "organizations",
                "attributes": {
                    "email": updated_email
                }
            }
        }
        updated_org = self._api.organizations.update(self._test_org_name, update_payload)
        self._api.organizations.destroy(self._test_org_name)
        self.assertEqual(updated_org["data"]["attributes"]["email"], updated_email)

    def test_orgs_destroy(self):
        self._api.organizations.create(self._create_payload)
        org = self._api.organizations.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)

        self._api.organizations.destroy(self._test_org_name)
        org = self._api.organizations.show(self._test_org_name)
        self.assertEqual(org, None)

    def test_orgs_entitlements(self):
        self._api.organizations.create(self._create_payload)
        ent = self._api.organizations.entitlements(self._test_org_name)
        self._api.organizations.destroy(self._test_org_name)
        self.assertEqual(ent["data"]["type"], "entitlement-sets")
        self.assertTrue(ent["data"]["attributes"]["state-storage"])
