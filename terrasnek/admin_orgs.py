"""
Module for Terraform Cloud API Endpoint: Admin Orgs.
"""

from .endpoint import TFCEndpoint

class TFCAdminOrgs(TFCEndpoint):
    """
    The Orgs Admin API contains endpoints to help site administrators manage organizations.

    https://www.terraform.io/docs/cloud/api/admin/organizations.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._orgs_base_url = f"{base_url}/admin/organizations"

    def destroy(self, org_name):
        """
        DELETE /admin/organizations/:org_name
        """
        url = f"{self._orgs_base_url}/{org_name}"
        return self._destroy(url)

    def list(self):
        """
        GET /admin/organizations

        This endpoint lists all organizations in the Terraform Cloud installation.
        """
        return self._list(self._orgs_base_url)

    def show(self, org_name):
        """
        GET /admin/organizations/:org_name
        """
        url = f"{self._orgs_base_url}/{org_name}"
        return self._show(url)
