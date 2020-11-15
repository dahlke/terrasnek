"""
Module for Terraform Cloud API Endpoint: State Versions.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCStateVersions(TFCEndpoint):
    """
    `State Versions API Docs \
        <https://www.terraform.io/docs/cloud/api/state-versions.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._state_version_api_v2_base_url = f"{self._api_v2_base_url}/state-versions"
        self._workspace_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def _required_entitlements(self):
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

    def list(self, filters=None, page=None, page_size=None):
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

    def show(self, state_version_id):
        """
        ``GET /state-versions/:state_version_id``

        `State Versions Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#show-a-state-version>`_
        """
        url = f"{self._state_version_api_v2_base_url}/{state_version_id}"
        return self._show(url)
