"""
Module for testing the Terraform Cloud API Endpoint: Admin Terraform Versions.
"""

from .base import TestTFCBaseTestCase

TF_RELEASE_URL = "https://releases.hashicorp.com/terraform/0.11.8/terraform_0.11.8_linux_amd64.zip"
TF_RELEASE_SHA = "84ccfb8e13b5fce63051294f787885b76a1fedef6bdbecf51c5e586c9e20c9b7"

class TestTFCAdminTerraformVersions(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Terraform Versions.
    """

    _unittest_name = "tf-ver"
    _endpoint_being_tested = "admin_terraform_versions"

    def test_admin_terraform_versions(self):
        """
        Test the Admin Terraform Versions API endpoints.
        """

        # List all the TF versions, verify the response type
        all_tf_versions = self._api.admin_terraform_versions.list()["data"]
        self.assertEqual("terraform-versions", all_tf_versions[0]["type"])

        # Create a fake version and confirm it was created correctly
        version_to_create = "0.1.300"
        create_payload = {
            "data": {
                "type": "terraform-versions",
                "attributes": {
                    "version": version_to_create,
                    "url": TF_RELEASE_URL,
                    "sha": TF_RELEASE_SHA,
                    "official": False,
                    "enabled": True,
                    "beta": False
                }
            }
        }
        created_tf_version = self._api.admin_terraform_versions.create(create_payload)["data"]
        created_tf_version_id = created_tf_version["id"]
        self.assertEqual(version_to_create, created_tf_version["attributes"]["version"])

        # Update the newly created version to be a beta version, confirm the change
        beta_to_update_to = True
        update_payload = {
            "data": {
                "type": "terraform-versions",
                "attributes": {
                    "beta": beta_to_update_to
                }
            }
        }
        updated_tf_version = \
            self._api.admin_terraform_versions.update(created_tf_version_id, update_payload)["data"]
        self.assertEqual(beta_to_update_to, updated_tf_version["attributes"]["beta"])

        # Show the TF version, confirm the version number
        shown_tf_version = self._api.admin_terraform_versions.show(created_tf_version_id)["data"]
        self.assertEqual(version_to_create, shown_tf_version["attributes"]["version"])

        # Destroy the TF version, confirm it's gone
        self._api.admin_terraform_versions.destroy(created_tf_version_id)
        all_tf_versions = self._api.admin_terraform_versions.list()["data"]
        found_created_version = False
        for version in all_tf_versions:
            version_id = version["id"]
            if version_id == created_tf_version_id:
                found_created_version = True
                break
        self.assertFalse(found_created_version)
