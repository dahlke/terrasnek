"""
Module for testing the Terraform Cloud API Endpoint: Admin Terraform Versions.
"""

from .base import TestTFCBaseTestCase


class TestTFCAdminTerraformVersions(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Terraform Versions.
    """

    def test_admin_terraform_versions(self):
        """
        Test the Admin Terraform Versions API endpoints: created, show, updated,
        list, destroy.
        """
        # TODO: comments here
        all_tf_versions = self._api.admin_terraform_versions.list()["data"]
        self.assertTrue("terraform-versions", all_tf_versions[0]["type"])

        version_to_create = "0.1.300"
        create_payload = {
            "data": {
                "type": "terraform-versions",
                "attributes": {
                    "version": version_to_create,
                    "url": "https://releases.hashicorp.com/terraform/0.11.8/terraform_0.11.8_linux_amd64.zip",
                    "sha": "84ccfb8e13b5fce63051294f787885b76a1fedef6bdbecf51c5e586c9e20c9b7",
                    "official": False,
                    "enabled": True,
                    "beta": False
                }
            }
        }
        created_tf_version = self._api.admin_terraform_versions.create(create_payload)["data"]
        created_tf_version_id = created_tf_version["id"]
        self.assertEqual(version_to_create, created_tf_version["attributes"]["version"])

        beta_to_update_to = True
        update_payload = {
            "data": {
                "type": "terraform-versions",
                "attributes": {
                    "beta": beta_to_update_to
                }
            }
        }
        updated_tf_version = self._api.admin_terraform_versions.update(created_tf_version_id, update_payload)["data"]
        self.assertEqual(beta_to_update_to, updated_tf_version["attributes"]["beta"])

        shown_tf_version = self._api.admin_terraform_versions.show(created_tf_version_id)["data"]
        self.assertEqual(version_to_create, updated_tf_version["attributes"]["version"])

        self._api.admin_terraform_versions.destroy(created_tf_version_id)
        all_tf_versions = self._api.admin_terraform_versions.list()["data"]
        found_created_version = False
        for version in all_tf_versions:
            version_id = version["id"]
            if version_id == created_tf_version_id:
                found_created_version = True
                break
        self.assertFalse(found_created_version)