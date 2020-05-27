"""
Module for Terraform Cloud API Endpoint: Admin Orgs.
"""

from .endpoint import TFCEndpoint

class TFCAdminOrgs(TFCEndpoint):
    """
    The Admin API is exclusive to Terraform Enterprise, and can only be used
    by the admins and operators who install and maintain their organization's
    Terraform Enterprise instance.

    The Orgs Admin API contains endpoints to help site administrators manage organizations.

    https://www.terraform.io/docs/cloud/api/admin/organizations.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/organizations"

    def required_entitlements(self):
        return []

    def destroy(self, org_name):
        """
        ``DELETE /admin/organizations/:name``
        """
        url = f"{self._endpoint_base_url}/{org_name}"
        return self._destroy(url)

    def list(self):
        """
        ``GET /admin/organizations``

        This endpoint lists all organizations in the Terraform Cloud installation.
        """
        return self._list(self._endpoint_base_url)

    def show(self, org_name):
        """
        ``GET /admin/organizations/:name``
        """
        url = f"{self._endpoint_base_url}/{org_name}"
        return self._show(url)
