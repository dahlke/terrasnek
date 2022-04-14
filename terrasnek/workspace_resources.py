"""
Module for Terraform Cloud API Endpoint: Workspace Resources.
"""

from .endpoint import TFCEndpoint

class TFCWorkspaceResources(TFCEndpoint):
    """
    `Workspace Resources API Docs \
        <https://www.terraform.io/cloud-docs/api-docs/workspace-resources>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def list(self, workspace_id):
        """
        ``GET /workspaces/:workspace_id/resources``

        `Workspace Resources List API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/workspace-resources#list-workspace-resources>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/cloud-docs/api-docs/workspace-resources#query-parameters>`__
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/resources/"
        return self._list(url)
