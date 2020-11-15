"""
Module for Terraform Cloud API Endpoint: Team Access.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCTeamAccess(TFCEndpoint):
    """
    `Team Access API Docs \
        <https://www.terraform.io/docs/cloud/api/team-access.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/team-workspaces"

    def _required_entitlements(self):
        return [Entitlements.TEAMS]

    def add_team_access(self, payload):
        """
        ``POST /team-workspaces``

        `Team Access Add API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/team-access.html#add-team-access-to-a-workspace>`_

        `Add Sample Payload \
            <https://www.terraform.io/docs/cloud/api/team-access.html#sample-payload>`_
        """
        return self._post(self._endpoint_base_url, data=payload)

    def list(self, filters=None):
        """
        ``GET /team-workspaces``

        `Team Access List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/team-access.html#list-team-access-to-a-workspace>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/team-access.html#query-parameters>`_):
            - ``filter[workspace][id]`` (Required)

        Example filter(s):

        .. code-block:: python

            filters = [
                {
                    "keys": ["workspace", "id"],
                    "value": "foo"
                }
            ]
        """
        return self._list(self._endpoint_base_url, filters=filters)

    def remove_team_access(self, access_id):
        """
        ``DELETE /team-workspaces/:id``

        `Team Access Remove API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/team-access.html#remove-team-access-to-a-workspace>`_
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._delete(url)

    def show(self, access_id):
        """
        ``GET /team-workspaces/:id``

        `Team Access Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/team-access.html#show-a-team-access-relationship>`_
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._show(url)

    def update(self, access_id, payload):
        """
        ``PATCH /team-workspaces/:id``

        `Team Access Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/team-access.html#update-team-access-to-a-workspace>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/team-access.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._update(url, payload)
