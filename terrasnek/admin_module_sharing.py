"""
Module for Terraform Cloud API Endpoint: Admin Module Sharing.
"""

from .endpoint import TFCEndpoint

class TFCAdminModuleSharing(TFCEndpoint):
    """
    `Admin Module Sharing API Docs \
        <https://www.terraform.io/docs/cloud/api/admin/module-sharing.html#update-an-organization-39-s-module-consumers>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/admin/organizations"
        self._mod_consumers_api_v2_base_url = \
            f"{self._org_api_v2_base_url}/{org_name}/relationships/module-consumers"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return True

    def update(self, org_name, payload):
        """
        ``PATCH /admin/organizations/:name/module-consumers``

        `Admin Module Sharing API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/module-sharing.html#update-an-organization-39-s-module-consumers>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/admin/module-sharing.html#sample-payload>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}/module-consumers"
        return self._update(url, payload)
