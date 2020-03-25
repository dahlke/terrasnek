"""
Module for Terraform Cloud API Endpoint: Workspaces.
"""

import json
import requests
from urllib import parse

from .endpoint import TFCEndpoint

class TFCWorkspaces(TFCEndpoint):
    """
    Workspaces represent running infrastructure managed by Terraform.

    https://www.terraform.io/docs/cloud/api/workspaces.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._ws_base_url = f"{base_url}/workspaces"
        self._org_base_url = f"{base_url}/organizations/{organization_name}/workspaces"
        # TODO: Assign and Unassign SSH key, requires SSH key endpoint

    def create(self, payload):
        """
        POST /organizations/:organization_name/workspaces
        """
        return self._create(self._org_base_url, payload)

    def destroy(self, workspace_id=None, workspace_name=None):
        """
        GET /organizations/:organization_name/workspaces/:name
        DELETE /workspaces/:workspace_id

        A workspace can be deleted via two endpoints, which behave identically. One refers to a
        workspace by its ID, and the other by its name and organization.
        """
        if workspace_name is not None:
            url = f"{self._org_base_url}/{workspace_name}"
        elif workspace_id is not None:
            url = f"{self._ws_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._destroy(url)

    def force_unlock(self, workspace_id):
        """
        POST /workspaces/:workspace_id/actions/force-unlock

        This endpoint force unlocks a workspace. Only users with admin access are authorized to
        force unlock a workspace.
        """
        results = None
        url = f"{self._ws_base_url}/{workspace_id}/actions/force-unlock"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def lock(self, workspace_id, payload):
        """
        POST /workspaces/:workspace_id/actions/lock

        This endpoint locks a workspace.
        """
        results = None
        url = f"{self._ws_base_url}/{workspace_id}/actions/lock"
        req = requests.post(url, json.dumps(payload), headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def lst(self, page_number=None, page_size=None):
        """
        GET /organizations/:organization_name/workspaces

        This endpoint lists workspaces in the organization.
        """
        url = f"{self._org_base_url}"

        filters = {}
        if page_number is not None:
            filters["page[number]"] = page_number

        if page_size is not None:
            filters["page[size]"] = page_size

        if filters:
            url += "?" + parse.urlencode(filters)
        return self._ls(url)

    def show(self, workspace_name=None, workspace_id=None):
        """
        GET /organizations/:organization_name/workspaces/:name
        GET /workspaces/:workspace_id

        Details on a workspace can be retrieved from two endpoints, which behave identically.
        One refers to a workspace by its ID, and the other by its name and organization.
        """
        if workspace_name is not None:
            url = f"{self._org_base_url}/{workspace_name}"
        elif workspace_id is not None:
            url = f"{self._ws_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._show(url)

    def unlock(self, workspace_id):
        """
        POST /workspaces/:workspace_id/actions/unlock

        This endpoint unlocks a workspace.
        """
        results = None
        url = f"{self._ws_base_url}/{workspace_id}/actions/unlock"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def update(self, workspace_id, payload):
        """
        PATCH /workspaces/:workspace_id

        A workspace can be updated via two endpoints, which behave identically. One refers to a
        workspace by its ID, and the other by its name and organization.
        """
        url = f"{self._ws_base_url}/{workspace_id}"
        return self._update(url, payload)
