"""
Module for Terraform Cloud API Endpoint: Team Memberships.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCTeamMemberships(TFCEndpoint):
    """
    `Team Membership API Docs \
        <https://www.terraform.io/docs/cloud/api/team-members.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/teams"

    def _required_entitlements(self):
        return [Entitlements.TEAMS]

    def add_user_to_team(self, team_id, payload):
        """
        ``POST /teams/:team_id/relationships/users``

        `Team Membership Add User To Team API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/team-members.html#add-a-user-to-team>`_

        `Add Sample Payload \
            <https://www.terraform.io/docs/cloud/api/team-members.html#sample-payload>`_
        """
        url = f"{self._endpoint_base_url}/{team_id}/relationships/users"
        return self._post(url, data=payload)

    def remove_user_from_team(self, team_id, payload):
        """
        ``DELETE /teams/:team_id/relationships/users``

        `Team Membership Remove User From Team API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/team-members.html#delete-a-user-from-team>`_

        `Remove Sample Payload \
            <https://www.terraform.io/docs/cloud/api/team-members.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{team_id}/relationships/users"
        return self._delete(url, data=payload)
