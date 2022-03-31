"""
Module for Terraform Cloud API Endpoint: State Version Outputs.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCStateVersionOutputs(TFCEndpoint):
    """
    `State Version Outputs API Docs \
        <https://www.terraform.io/docs/cloud/api/state-version-outputs.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/state-version-outputs"
        self._state_versions_base_url = f"{self._api_v2_base_url}/state-versions"
        self._ws_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return [Entitlements.STATE_STORAGE]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def list(self, state_version_id, page=None, page_size=None):
        """
        ``GET /state-versions/:state_version_id/outputs``

        `State Version Outputs List API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/state-version-outputs#list-state-version-outputs>`_
        """
        url = f"{self._state_versions_base_url}/{state_version_id}/outputs"
        return self._list(url, page=page, page_size=page_size)


    def show(self, state_version_output_id):
        """
        ``GET /state-version-outputs/:state_version_output_id``

        `State Version Outputs Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-version-outputs.html#show-a-state-version-output>`_
        """
        url = f"{self._endpoint_base_url}/{state_version_output_id}"
        return self._show(url)


    def show_current_for_workspace(self, workspace_id):
        """
        ``GET /workspaces/:workspace_id/current-state-version-outputs``

        `State Version Outputs Show Current for Workspace API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/state-version-outputs#show-current-state-version-outputs-for-a-workspace>`_
        """
        url = f"{self._ws_base_url}/{workspace_id}/current-state-version-outputs"
        return self._show(url)
