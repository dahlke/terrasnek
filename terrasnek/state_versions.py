"""
Module for Terraform Cloud API Endpoint: State Versions.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements, MAX_PAGE_SIZE

class TFCStateVersions(TFCEndpoint):
    """
    `State Versions API Docs \
        <https://www.terraform.io/docs/cloud/api/state-versions.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._state_version_api_v2_base_url = f"{self._api_v2_base_url}/state-versions"
        self._workspace_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return [Entitlements.STATE_STORAGE]

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/state-versions``

        `State Versions Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#create-a-state-version>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#sample-payload>`_
        """
        url = f"{self._workspace_api_v2_base_url}/{workspace_id}/state-versions"
        return self._create(url, payload)

    def get_current(self, workspace_id):
        """
        ``GET /workspaces/:workspace_id/current-state-version``

        `State Versions Get Current API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#fetch-the-current-state-version-for-a-workspace>`_
        """
        url = f"{self._workspace_api_v2_base_url}/{workspace_id}/current-state-version"
        return self._get(url)

    def list(self, filters, page=None, page_size=None):
        """
        ``GET /state-versions``

        `State Versions List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#list-state-versions-for-a-workspace>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#query-parameters>`_):
            - ``filter[workspace][name]`` (Required)
            - ``filter[organization][name]`` (Required)
            - ``page`` (Optional)
            - ``page_size`` (Optional)

        Example filter(s):

        .. code-block:: python

            filters = [
                {
                    "keys": ["workspace", "name"],
                    "value": "foo"
                },
                {
                    "keys": ["organization", "name"],
                    "value": "bar"
                }
            ]
        """
        url = f"{self._state_version_api_v2_base_url}"
        return self._list(url, filters=filters, page=page, page_size=page_size)

    def list_all(self, filters):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every state version for a workspace.

        Returns an array of objects.
        """
        url = self._state_version_api_v2_base_url

        current_page_number = 1
        state_versions_resp = \
            self._list(url, filters=filters, page=current_page_number, page_size=MAX_PAGE_SIZE)
        total_pages = state_versions_resp["meta"]["pagination"]["total-pages"]

        state_versions = []
        while current_page_number <= total_pages:
            state_versions_resp = \
                self._list(url, filters=filters, page=current_page_number, page_size=MAX_PAGE_SIZE)
            state_versions += state_versions_resp["data"]
            current_page_number += 1

        return state_versions

    def show(self, state_version_id):
        """
        ``GET /state-versions/:state_version_id``

        `State Versions Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#show-a-state-version>`_
        """
        url = f"{self._state_version_api_v2_base_url}/{state_version_id}"
        return self._show(url)
