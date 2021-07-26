"""
Module for Terraform Cloud API Endpoint: Admin Workspaces.
"""

from .endpoint import TFCEndpoint

class TFCAdminWorkspaces(TFCEndpoint):
    """
    `Admin Workspaces API Docs \
        <https://www.terraform.io/docs/cloud/api/admin/workspaces.html>`_

    The Admin API is exclusive to Terraform Enterprise, and can only be used
    by the admins and operators who install and maintain their organization's
    Terraform Enterprise instance.

    The Workspaces Admin API contains endpoints to help site administrators manage
    workspaces.
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return True

    def list(self, filters=None, page=None, page_size=None, sort=None, search=None, include=None):
        """
        ``GET /api/v2/admin/workspaces``

        `Admin Workspaces List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/workspaces.html#list-all-workspaces>`_
        """
        return self._list(\
            self._endpoint_base_url, filters=filters, \
            page=page, page_size=page_size, search=search, sort=sort, include=include)

    def show(self, ws_id):
        """
        ``GET /api/v2/admin/workspaces/:id``

        `Admin Workspaces Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/workspaces.html#show-a-workspace>`_
        """
        url = f"{self._endpoint_base_url}/{ws_id}"
        return self._show(url)

    def destroy(self, ws_id):
        """
        ``DELETE /admin/workspaces/:id``

        `Admin Workspaces Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/workspaces.html#destroy-a-workspace>`_
        """
        url = f"{self._endpoint_base_url}/{ws_id}"
        return self._destroy(url)
