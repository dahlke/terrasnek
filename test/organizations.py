import unittest
import os
from .base import TestTFEBaseTestCase

from tfepy.api import TFE

class TestTFEOrganizations(TestTFEBaseTestCase):

    def test_orgs_ls(self):
        self._api.organizations.create(self._org_create_payload)
        orgs = self._api.organizations.ls()["data"]
        self.assertNotEqual(len(orgs), 0, msg="No organizations found for TFE token.")
        self._api.organizations.destroy(self._test_org_name)

    def test_orgs_show(self):
        self._api.organizations.create(self._org_create_payload)
        org = self._api.organizations.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)
        self._api.organizations.destroy(self._test_org_name)
    
    def test_orgs_create(self):
        new_org = self._api.organizations.create(self._org_create_payload)
        self._api.organizations.destroy(self._test_org_name)
        self.assertEqual(new_org["data"]["id"], self._test_org_name)

    def test_orgs_update(self):
        updated_email = "neil+pytfe-unittest@hashicorp.com"
        new_org = self._api.organizations.create(self._org_create_payload)
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
        self._api.organizations.create(self._org_create_payload)
        org = self._api.organizations.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)

        self._api.organizations.destroy(self._test_org_name)
        org = self._api.organizations.show(self._test_org_name)
        self.assertEqual(org, None)

    def test_orgs_entitlements(self):
        self._api.organizations.create(self._org_create_payload)
        ent = self._api.organizations.entitlements(self._test_org_name)
        self._api.organizations.destroy(self._test_org_name)
        self.assertEqual(ent["data"]["type"], "entitlement-sets")
        self.assertTrue(ent["data"]["attributes"]["state-storage"])

    def test_orgs_admin(self):
        # Need to use the non-admin to create for some reason
        self._api.organizations.create(self._org_create_payload)

        orgs = self._api.admin_organizations.ls()["data"]
        self.assertNotEqual(len(orgs), 0, msg="No organizations found for TFE token.")

        org = self._api.admin_organizations.show(self._test_org_name)
        self.assertEqual(org["data"]["id"], self._test_org_name)

        self._api.admin_organizations.destroy(self._test_org_name)