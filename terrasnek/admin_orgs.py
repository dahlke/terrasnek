"""
Module for Terraform Cloud API Endpoint: Admin Orgs.
"""

from .endpoint import TFCEndpoint

class TFCAdminOrgs(TFCEndpoint):
    """
    `Admin Orgs API Docs \
        <https://www.terraform.io/docs/cloud/api/admin/organizations.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/organizations"

    def _required_entitlements(self):
        return []

    def destroy(self, org_name):
        """
        ``DELETE /admin/organizations/:name``

        `Admin Destroy Org API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#delete-an-organization>`_
        """
        url = f"{self._endpoint_base_url}/{org_name}"
        return self._destroy(url)

    def list(self):
        """
        ``GET /admin/organizations``

        `Admin List Orgs API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#list-all-organizations>`_

        This endpoint lists all organizations in the Terraform Cloud installation.
        """
        return self._list(self._endpoint_base_url)

    def show(self, org_name):
        """
        ``GET /admin/organizations/:name``

        `Admin Show Org API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#show-an-organization>`_
        """
        url = f"{self._endpoint_base_url}/{org_name}"
        return self._show(url)
