"""
Module for Terraform Cloud API Endpoint: Team Memberships.
"""

from .endpoint import TFCEndpoint

class TFCTeamMemberships(TFCEndpoint):
    """
    The Team Membership API is used to add or remove users from teams. The Team API is
    used to create or destroy teams.

    https://www.terraform.io/docs/cloud/api/team-members.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/teams"

    def add_a_user_to_team(self, team_id, payload):
        """
        POST /teams/:team_id/relationships/users

        This method adds multiple users to a team. Both users and teams must already exist.
        """
        url = f"{self._base_url}/{team_id}/relationships/users"
        return self._post(url, data=payload)

    def remove_a_user_from_team(self, team_id, payload):
        """
        DELETE /teams/:team_id/relationships/users

        This method removes multiple users from a team. Both users and teams must already exist.
        This DOES NOT delete the user; it only removes them from this team.
        """
        url = f"{self._base_url}/{team_id}/relationships/users"
        return self._delete(url, data=payload)
