"""
Module for Terraform Cloud API Endpoint: Workspaces.
"""

from .endpoint import TFCEndpoint

class TFCWorkspaces(TFCEndpoint):
    """
    `API Docs \
        <https://www.terraform.io/docs/cloud/api/workspaces.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/workspaces"

    def required_entitlements(self):
        return []

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/workspaces``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#create-a-workspace>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def destroy(self, workspace_id=None, workspace_name=None):
        """
        ``DELETE /organizations/:organization_name/workspaces/:name``
        ``DELETE /workspaces/:workspace_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#delete-a-workspace>`_
        """
        if workspace_name is not None:
            url = f"{self._org_api_v2_base_url}/{workspace_name}"
        elif workspace_id is not None:
            url = f"{self._ws_api_v2_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._destroy(url)

    def force_unlock(self, workspace_id):
        """
        ``POST /workspaces/:workspace_id/actions/force-unlock``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#force-unlock-a-workspace>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/actions/force-unlock"
        return self._post(url)

    def lock(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/actions/lock``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#lock-a-workspace>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-2>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/actions/lock"
        return self._post(url, data=payload)

    def list(self, page=None, page_size=None):
        """
        ``GET /organizations/:organization_name/workspaces``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#list-workspaces>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#query-parameters>`_):
            - ``page`` (Optional)
            - ``page_size`` (Optional)
        """
        return self._list(self._org_api_v2_base_url, page=page, page_size=page_size)

    def show(self, workspace_name=None, workspace_id=None):
        """
        ``GET /organizations/:organization_name/workspaces/:name``
        ``GET /workspaces/:workspace_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#show-workspace>`_
        """
        if workspace_name is not None:
            url = f"{self._org_api_v2_base_url}/{workspace_name}"
        elif workspace_id is not None:
            url = f"{self._ws_api_v2_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._show(url)

    def unlock(self, workspace_id):
        """
        ``POST /workspaces/:workspace_id/actions/unlock``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#unlock-a-workspace>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/actions/unlock"
        return self._post(url)

    def update(self, payload, workspace_name=None, workspace_id=None):
        """
        ``PATCH /organizations/:organization_name/workspaces/:name``
        ``PATCH /workspaces/:workspace_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#update-a-workspace>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-1>`_
        """
        if workspace_name is not None:
            url = f"{self._org_api_v2_base_url}/{workspace_name}"
        elif workspace_id is not None:
            url = f"{self._ws_api_v2_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")
        return self._update(url, payload)


    def assign_ssh_key(self, workspace_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/relationships/ssh-key``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#assign-an-ssh-key-to-a-workspace>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-3>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/ssh-key"
        self._patch(url, data=payload)

    def unassign_ssh_key(self, workspace_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/relationships/ssh-key``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#unassign-an-ssh-key-from-a-workspace>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-4>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/ssh-key"
        self._patch(url, data=payload)
