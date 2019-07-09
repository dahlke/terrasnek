"""
Module for Terraform Enterprise API Endpoint: Admin Organizations.
"""

from .endpoint import TFEEndpoint

class TFEAdminOrganizations(TFEEndpoint):
    """
    The Organizations Admin API contains endpoints to help site administrators manage organizations.

    https://www.terraform.io/docs/enterprise/api/admin/organizations.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._orgs_base_url = f"{base_url}/admin/organizations"

    def destroy(self, organization_name):
        """
        DELETE /admin/organizations/:organization_name
        """
        url = f"{self._orgs_base_url}/{organization_name}"
        return self._destroy(url)

    def lst(self):
        """
        GET /admin/organizations

        This endpoint lists all organizations in the Terraform Enterprise installation.
        """
        return self._ls(self._orgs_base_url)

    def show(self, organization_name):
        """
        GET /admin/organizations/:organization_name
        """
        url = f"{self._orgs_base_url}/{organization_name}"
        return self._show(url)
