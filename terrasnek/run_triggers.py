"""
Module for Terraform Cloud API Endpoint: Run Triggers.
"""

from .endpoint import TFCEndpoint

class TFCRunTriggers(TFCEndpoint):
    """
    https://www.terraform.io/docs/cloud/api/run-triggers.html
    """
    def __init__(self, base_url, organization_name, headers, verify):
        super().__init__(base_url, organization_name, headers, verify)
        self._base_url = f"{base_url}/run-triggers"
        self._ws_base_url = f"{base_url}/workspaces"

    def create(self, workspace_id, payload):
        """
        POST /workspaces/:workspace_id/run-triggers
        """
        url = f"{self._ws_base_url}/{workspace_id}/run-triggers"
        return self._create(url, payload)

    def lst(self, workspace_id, run_trigger_type):
        """
        GET /workspaces/:workspace_id/run-triggers
        """
        url = f"{self._ws_base_url}/{workspace_id}/run-triggers"
        url += f"?filter[run-trigger][type]={run_trigger_type}"
        return self._ls(url)

    def show(self, run_trigger_id):
        """
        GET /run-triggers/:run_trigger_id
        """
        url = f"{self._base_url}/{run_trigger_id}"
        return self._show(url)

    def destroy(self, run_trigger_id):
        """
        DELETE /run-triggers/:run_trigger_id
        """
        url = f"{self._base_url}/{run_trigger_id}"
        return self._destroy(url)
