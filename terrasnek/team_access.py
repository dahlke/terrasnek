"""
Module for Terraform Cloud API Endpoint: Team Access.
"""

import json
import requests

from .endpoint import TFCEndpoint

class TFCTeamAccess(TFCEndpoint):
    """
    The team access APIs are used to associate a team to permissions on a workspace.
    A single team-workspace resource contains the relationship between the Team and Workspace,
    including the privileges the team has on the workspace.

    https://www.terraform.io/docs/cloud/api/team-access.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._base_url = f"{base_url}/team-workspaces"

    def add_team_access(self, payload):
        """
        POST /team-workspaces
        """
        results = None
        req = requests.post(self._base_url, json.dumps(payload), headers=self._headers)

        if req.status_code == 201:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def lst(self):
        """
        GET /team-workspaces
        """
        return self._ls(self._base_url)

    def remove_team_access(self, access_id):
        """
        DELETE /team-workspaces/:id
        """
        url = f"{self._base_url}/{access_id}"
        req = requests.delete(url, headers=self._headers)

        if req.status_code == 204:
            self._logger.info("Team access removed.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def show(self, access_id):
        """
        GET /team-workspaces/:id
        """
        url = f"{self._base_url}/{access_id}"
        return self._show(url)
