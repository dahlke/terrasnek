"""
Module for Terraform Cloud API Endpoint: Admin Terraform Versions.
"""

from .endpoint import TFCEndpoint

class TFCAdminTerraformVersions(TFCEndpoint):
    """
    The Terraform Versions Admin API lets site administrators manage which
    versions of Terraform are available to the Terraform Cloud users within
    their enterprise.

    https://www.terraform.io/docs/cloud/api/admin/terraform-versions.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/terraform-versions"

    def list(self, page=None, page_size=None):
        """
        ``GET /admin/terraform-versions``

        This endpoint lists all organizations in the Terraform Cloud installation.
        """
        return self._list(self._endpoint_base_url, page=page, page_size=page_size)

    def required_entitlements(self):
        return []

    def create(self, data):
        """
        ``POST /admin/terraform-versions``
        """
        return self._post(self._endpoint_base_url, data=data)

    def show(self, version_id):
        """
        ``GET /admin/terraform-versions/:id``
        """
        url = f"{self._endpoint_base_url}/{version_id}"
        return self._show(url)

    def update(self, version_id, data):
        """
        ``PATCH /admin/terraform-versions/:id``
        """
        url = f"{self._endpoint_base_url}/{version_id}"
        return self._patch(url, data)

    def destroy(self, version_id):
        """
        ``DELETE /admin/terraform-versions/:id``
        """
        url = f"{self._endpoint_base_url}/{version_id}"
        return self._destroy(url)
