"""
Module for Terraform Cloud API Endpoint: State Versions.
"""

from .endpoint import TFCEndpoint

class TFCStateVersions(TFCEndpoint):
    """
    https://www.terraform.io/docs/cloud/api/state-versions.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._state_version_base_url = f"{base_url}/state-versions"
        self._workspace_base_url = f"{base_url}/workspaces"

    def create(self, workspace_id, payload):
        """
        POST /workspaces/:workspace_id/state-versions

        Creates a state version and sets it as the current state version for the given workspace.
        The workspace must be locked by the user creating a state version. The workspace may be
        locked with the API or with the UI. This is most useful for migrating existing state from
        open source Terraform into a new TFC workspace.
        """
        url = f"{self._workspace_base_url}/{workspace_id}/state-versions"
        return self._create(url, payload)

    def get_current(self, workspace_id):
        """
        GET /workspaces/:workspace_id/current-state-version

        Fetches the current state version for the given workspace. This state version will be
        the input state when running terraform operations.
        """
        url = f"{self._workspace_base_url}/{workspace_id}/current-state-version"
        return self._get(url)

    def list(self, filters=None, page=None, page_size=None):
        """
        GET /state-versions

        This endpoint supports pagination with standard URL query parameters; remember to
        percent-encode.
        """
        url = f"{self._state_version_base_url}"
        return self._list(url, filters=filters, page=page, page_size=page_size)

    def show(self, state_version_id):
        """
        GET /state-versions/:state_version_id
        """
        url = f"{self._state_version_base_url}/{state_version_id}"
        return self._show(url)
