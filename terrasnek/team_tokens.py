"""
Module for Terraform Cloud API Endpoint: Team Tokens.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCTeamTokens(TFCEndpoint):
    """
    Each team can have a special service account API token that is not associated with a
    specific user.

    https://www.terraform.io/docs/cloud/api/team-tokens.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/teams"

    def required_entitlements(self):
        return [Entitlements.TEAMS]

    def create(self, team_id):
        """
        ``POST /teams/:team_id/authentication-token``

        Generates a new team token and overrides existing token if one exists.
        """
        url = f"{self._endpoint_base_url}/{team_id}/authentication-token"
        payload = {}
        return self._create(url, payload)


    def destroy(self, team_id):
        """
        ``DELETE /teams/:team_id/authentication-token``
        """
        url = f"{self._endpoint_base_url}/{team_id}/authentication-token"
        return self._destroy(url)
