"""
Module for Terraform Cloud API Endpoint: Team Access.
"""

from .endpoint import TFCEndpoint

class TFCTeamAccess(TFCEndpoint):
    """
    The team access APIs are used to associate a team to permissions on a workspace.
    A single team-workspace resource contains the relationship between the Team and Workspace,
    including the privileges the team has on the workspace.

    https://www.terraform.io/docs/cloud/api/team-access.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/team-workspaces"

    def add_team_access(self, payload):
        """
        POST /team-workspaces
        """
        return self._post(self._base_url, data=payload)

    def list(self):
        """
        GET /team-workspaces
        """
        return self._list(self._base_url)

    def remove_team_access(self, access_id):
        """
        DELETE /team-workspaces/:id
        """
        url = f"{self._base_url}/{access_id}"
        return self._delete(url)

    def show(self, access_id):
        """
        GET /team-workspaces/:id
        """
        url = f"{self._base_url}/{access_id}"
        return self._show(url)
