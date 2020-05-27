"""
Module for Terraform Cloud API Endpoint: Admin Workspaces.
"""

from .endpoint import TFCEndpoint

class TFCAdminWorkspaces(TFCEndpoint):
    """
    The Admin API is exclusive to Terraform Enterprise, and can only be used
    by the admins and operators who install and maintain their organization's
    Terraform Enterprise instance.

    The Workspaces Admin API contains endpoints to help site administrators manage
    workspaces.

    https://www.terraform.io/docs/cloud/api/admin/workspaces.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/workspaces"

    def required_entitlements(self):
        return []

    def list(self, \
        filters=None, page=None, page_size=None, sort=None, search=None):
        """
        ``GET /admin/workspaces``

        This endpoint lists all organizations in the Terraform Cloud installation.
        """
        return self._list(\
            self._endpoint_base_url, filters=filters, \
            page=page, page_size=page_size, search=search, sort=sort)

    def show(self, ws_id):
        """
        ``GET /admin/workspaces/:id``
        """
        url = f"{self._endpoint_base_url}/{ws_id}"
        return self._show(url)

    def destroy(self, ws_id):
        """
        ``DELETE /admin/workspaces/:id``
        """
        url = f"{self._endpoint_base_url}/{ws_id}"
        return self._destroy(url)
