"""
Module for testing the Terraform Cloud API Endpoint: Admin Module Sharing.
"""

from .base import TestTFCBaseTestCase


class TestTFCAdminModuleSharing(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Module Sharing.
    """

    _unittest_name = "adm-mod"
    _endpoint_being_tested = "admin_module_sharing"

    def setUp(self):
        # Create a temp org to manipulate in the test
        created_org = self._api.orgs.create(self._get_org_create_payload())["data"]
        self._created_org_name = created_org["attributes"]["name"]
        self._created_org_id = created_org["id"]
        self._created_org_external_id = created_org["attributes"]["external-id"]

    def tearDown(self):
        self._api.orgs.destroy(self._created_org_name)

    def test_admin_module_sharing(self):
        """
        Test the Admin Module Sharing API endpoints.
        """

        # Change the email address for the org, confirm the change.
        update_org_payload = {
            "data": {
                "type": "module-partnerships",
                "attributes": {
                    "module-consuming-organization-ids": [
                        self._created_org_external_id
                    ]
                }
            }
        }

        module_partnerships = \
            self._api.admin_module_sharing.update(self._test_org_name, update_org_payload)["data"]

        found_partnership = False
        for partnership in module_partnerships:
            if partnership["attributes"]["consuming-organization-id"] == \
                    self._created_org_external_id:
                found_partnership = True
                break

        self.assertTrue(found_partnership)
