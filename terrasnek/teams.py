"""
Module for Terraform Cloud API Endpoint: Teams.
"""

from .endpoint import TFCEndpoint

class TFCTeams(TFCEndpoint):
    """
    The Teams API is used to create, edit, and destroy teams as well as manage a team's
    organization-level permissions. The Team Membership API is used to add or remove users
    from a team. Use the Team Access API to associate a team with privileges on an
    individual workspace.

    https://www.terraform.io/docs/cloud/api/teams.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._teams_base_url = f"{base_url}/teams"
        self._org_base_url = f"{base_url}/organizations/{organization_name}/teams"

    def create(self, payload):
        """
        POST /organizations/:organization_name/teams
        """
        return self._create(self._org_base_url, payload)

    def destroy(self, team_id):
        """
        DELETE /teams/:team_id
        """
        url = f"{self._teams_base_url}/{team_id}"
        return self._destroy(url)

    def lst(self):
        """
        GET organizations/:organization_name/teams
        """
        return self._ls(self._org_base_url)

    def show(self, team_id):
        """
        GET /teams/:team_id
        """
        url = f"{self._teams_base_url}/{team_id}"
        return self._show(url)
