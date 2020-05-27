"""
Module for Terraform Cloud API Endpoint: Run Triggers.
"""

from .endpoint import TFCEndpoint

class TFCRunTriggers(TFCEndpoint):
    """
    https://www.terraform.io/docs/cloud/api/run-triggers.html
    """
    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/run-triggers"
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/run-triggers``
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/run-triggers"
        return self._create(url, payload)

    def list(self, workspace_id, filters=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/run-triggers``
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/run-triggers"
        return self._list(url, filters=filters, page_size=page_size)

    def show(self, run_trigger_id):
        """
        ``GET /run-triggers/:run_trigger_id``
        """
        url = f"{self._endpoint_base_url}/{run_trigger_id}"
        return self._show(url)

    def destroy(self, run_trigger_id):
        """
        ``DELETE /run-triggers/:run_trigger_id``
        """
        url = f"{self._endpoint_base_url}/{run_trigger_id}"
        return self._destroy(url)
