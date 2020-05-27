"""
Module for Terraform Cloud API Endpoint: Workspace Variables.
"""

from .endpoint import TFCEndpoint

class TFCWorkspaceVars(TFCEndpoint):
    """
    This set of APIs covers create, update, list and delete operations on variables,
    through the workspace API.

    https://www.terraform.io/docs/cloud/api/workspace-variables.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/vars``
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/"
        return self._create(url, payload)

    def list(self, workspace_id):
        """
        ``GET /workspaces/:workspace_id/vars``
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/"
        return self._list(url)

    def update(self, workspace_id, variable_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/vars/:variable_id``
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/{variable_id}"
        return self._update(url, payload)

    def destroy(self, workspace_id, variable_id):
        """
        ``DELETE /workspaces/:workspace_id/vars/:variable_id``
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/{variable_id}"
        return self._destroy(url)
