"""
Module for Terraform Cloud API Endpoint: Teams.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCTeams(TFCEndpoint):
    """
    `Teams API Docs \
        <https://www.terraform.io/docs/cloud/api/teams.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._teams_api_v2_base_url = f"{self._api_v2_base_url}/teams"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/teams"

    def required_entitlements(self):
        return [Entitlements.TEAMS]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/teams``

        `Teams Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#create-a-team>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/teams.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def destroy(self, team_id):
        """
        ``DELETE /teams/:team_id``

        `Teams Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#delete-a-team>`_
        """
        url = f"{self._teams_api_v2_base_url}/{team_id}"
        return self._destroy(url)

    def list(self, page=None, page_size=None, filters=None, include=None):
        """
        ``GET organizations/:organization_name/teams``

        `Teams List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#list-teams>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/teams.html#query-parameters>`__
        """
        return self._list(\
            self._org_api_v2_base_url, page=page, page_size=page_size, filters=filters, include=include)

    def list_all(self, filters=None, include=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every run for a workspace.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_api_v2_base_url, filters=filters, include=include)

    def show(self, team_id, include=None):
        """
        ``GET /teams/:team_id``

        `Teams Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#show-team-information>`_
        """
        url = f"{self._teams_api_v2_base_url}/{team_id}"
        return self._show(url, include=include)

    def update(self, team_id, payload):
        """
        ``PATCH /teams/:team_id``

        `Teams Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#update-a-team>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/teams.html#sample-payload-1>`_
        """
        url = f"{self._teams_api_v2_base_url}/{team_id}"
        return self._update(url, payload)
