"""
Module for Terraform Cloud API Endpoint: Team Tokens.
"""

from .endpoint import TFCEndpoint

class TFCTeamTokens(TFCEndpoint):
    """
    Each team can have a special service account API token that is not associated with a
    specific user.

    https://www.terraform.io/docs/cloud/api/team-tokens.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/teams"

    def create(self, team_id):
        """
        POST /teams/:team_id/authentication-token

        Generates a new team token and overrides existing token if one exists.
        """
        url = f"{self._base_url}/{team_id}/authentication-token"
        payload = {}
        return self._create(url, payload)


    def destroy(self, team_id):
        """
        DELETE /teams/:team_id/authentication-token
        """
        url = f"{self._base_url}/{team_id}/authentication-token"
        return self._destroy(url)
