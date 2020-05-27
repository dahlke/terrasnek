"""
Module for Terraform Cloud API Endpoint: Team Access.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCTeamAccess(TFCEndpoint):
    """
    The team access APIs are used to associate a team to permissions on a workspace.
    A single team-workspace resource contains the relationship between the Team and Workspace,
    including the privileges the team has on the workspace.

    https://www.terraform.io/docs/cloud/api/team-access.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/team-workspaces"

    def required_entitlements(self):
        return [Entitlements.TEAMS]

    def add_team_access(self, payload):
        """
        ``POST /team-workspaces``
        """
        return self._post(self._endpoint_base_url, data=payload)

    def list(self):
        """
        ``GET /team-workspaces``
        """
        return self._list(self._endpoint_base_url)

    def remove_team_access(self, access_id):
        """
        ``DELETE /team-workspaces/:id``
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._delete(url)

    def show(self, access_id):
        """
        ``GET /team-workspaces/:id``
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._show(url)

    def update(self, access_id, payload):
        """
        ``PATCH /team-workspaces/:id``
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._update(url, payload)
