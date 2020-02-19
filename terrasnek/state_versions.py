"""
Module for Terraform Cloud API Endpoint: State Versions.
"""

import json
import requests

from .endpoint import TFCEndpoint

class TFCStateVersions(TFCEndpoint):
    """
    https://www.terraform.io/docs/cloud/api/state-versions.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
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
        results = None
        url = f"{self._workspace_base_url}/{workspace_id}/current-state-version"
        req = requests.get(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def lst(self, workspace_name, page_number=None, page_size=None):
        """
        GET /state-versions

        This endpoint supports pagination with standard URL query parameters; remember to
        percent-encode.
        """
        url = f"{self._state_version_base_url}"
        url += f"?filter[organization][name]={self._organization_name}"
        url += f"&filter[workspace][name]={workspace_name}"

        filters = []
        if page_number is not None:
            filters.append(f"page[number]={page_number}")

        if page_size is not None:
            filters.append(f"page[size]={page_size}")

        if filters:
            url += "&".join(filters)
        return self._ls(url)

    def show(self, state_version_id):
        """
        GET /state-versions/:state_version_id
        """
        url = f"{self._state_version_base_url}/{state_version_id}"
        return self._show(url)
