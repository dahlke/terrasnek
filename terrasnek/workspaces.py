"""
Module for Terraform Cloud API Endpoint: Workspaces.
"""

from .endpoint import TFCEndpoint

class TFCWorkspaces(TFCEndpoint):
    """
    Workspaces represent running infrastructure managed by Terraform.

    https://www.terraform.io/docs/cloud/api/workspaces.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._ws_base_url = f"{base_url}/workspaces"
        self._org_base_url = f"{base_url}/organizations/{org_name}/workspaces"

    def create(self, payload):
        """
        POST /organizations/:org_name/workspaces
        """
        return self._create(self._org_base_url, payload)

    def destroy(self, workspace_id=None, workspace_name=None):
        """
        GET /organizations/:org_name/workspaces/:name
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
        url = f"{self._ws_base_url}/{workspace_id}/actions/force-unlock"
        return self._post(url)

    def lock(self, workspace_id, payload):
        """
        POST /workspaces/:workspace_id/actions/lock

        This endpoint locks a workspace.
        """
        url = f"{self._ws_base_url}/{workspace_id}/actions/lock"
        return self._post(url, data=payload)

    def list(self, page=None, page_size=None):
        """
        GET /organizations/:org_name/workspaces

        This endpoint lists workspaces in the organization.
        """
        return self._list(self._org_base_url, page=page, page_size=page_size)

    def show(self, workspace_name=None, workspace_id=None):
        """
        GET /organizations/:org_name/workspaces/:name
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
        url = f"{self._ws_base_url}/{workspace_id}/actions/unlock"
        return self._post(url)

    def update(self, workspace_id, payload):
        """
        PATCH /workspaces/:workspace_id

        A workspace can be updated via two endpoints, which behave identically. One refers to a
        workspace by its ID, and the other by its name and organization.
        """
        url = f"{self._ws_base_url}/{workspace_id}"
        return self._update(url, payload)


    def assign_ssh_key(self, workspace_id, data):
        """
        PATCH /workspaces/:workspace_id/relationships/ssh-key

        This endpoint assigns an SSH key to a workspace.
        """
        url = f"{self._ws_base_url}/{workspace_id}/relationships/ssh-key"
        self._patch(url, data=data)

    def unassign_ssh_key(self, workspace_id, data):
        """
        PATCH /workspaces/:workspace_id/relationships/ssh-key

        This endpoint unassigns the currently assigned SSH key from a
        workspace.
        """
        url = f"{self._ws_base_url}/{workspace_id}/relationships/ssh-key"
        self._patch(url, data=data)
