"""
Module for Terraform Cloud API Endpoint: Workspaces.
"""

from .endpoint import TFCEndpoint

class TFCWorkspaces(TFCEndpoint):
    """
    `Workspaces API Docs \
        <https://www.terraform.io/docs/cloud/api/workspaces.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/workspaces``

        `Workspaces Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#create-a-workspace>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def destroy(self, workspace_id=None, workspace_name=None):
        """
        ``DELETE /organizations/:organization_name/workspaces/:name``
        ``DELETE /workspaces/:workspace_id``

        `Workspaces Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#delete-a-workspace>`_
        """
        if workspace_name is not None:
            url = f"{self._org_api_v2_base_url}/{workspace_name}"
        elif workspace_id is not None:
            url = f"{self._ws_api_v2_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._destroy(url)

    def safe_destroy(self, workspace_id=None, workspace_name=None):
        """
        ``POST /workspaces/:workspace_id/actions/safe-delete``
        ``DELETE /organizations/:organization_name/workspaces/:name/actions/safe-delete``

        TODO / NOTE: the above DELETE should really be a POST, the docs don't match reality, so
        need to leave it as DELETE for now since our API comparison script relies on those strings.

        `Workspaces Safe Destroy API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces#safe-delete-a-workspace>`_
        """
        resp = None

        if workspace_name is not None:
            url = f"{self._org_api_v2_base_url}/{workspace_name}/actions/safe-delete"
            resp = self._post(url)
        elif workspace_id is not None:
            url = f"{self._ws_api_v2_base_url}/{workspace_id}/actions/safe-delete"
            resp = self._post(url)
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return resp

    def force_unlock(self, workspace_id):
        """
        ``POST /workspaces/:workspace_id/actions/force-unlock``

        `Workspaces Force Unlock API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#force-unlock-a-workspace>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/actions/force-unlock"
        return self._post(url)

    def lock(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/actions/lock``

        `Workspaces Lock API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#lock-a-workspace>`_

        `Lock Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-2>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/actions/lock"
        return self._post(url, data=payload)

    def list(self, page=None, page_size=None, include=None, search=None, filters=None):
        """
        ``GET /organizations/:organization_name/workspaces``

        `Workspaces List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#list-workspaces>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#query-parameters>`__
        """
        return self._list(self._org_api_v2_base_url, \
            page=page, page_size=page_size, include=include, search=search, filters=filters)

    def list_all(self, search=None, include=None, filters=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every workspace in an organization.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_api_v2_base_url, search=search, include=include, filters=filters)

    def show(self, workspace_name=None, workspace_id=None, include=None):
        """
        ``GET /organizations/:organization_name/workspaces/:name``
        ``GET /workspaces/:workspace_id``

        `Workspaces Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#show-workspace>`_
        """
        if workspace_name is not None:
            url = f"{self._org_api_v2_base_url}/{workspace_name}"
        elif workspace_id is not None:
            url = f"{self._ws_api_v2_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._show(url, include=include)

    def unlock(self, workspace_id):
        """
        ``POST /workspaces/:workspace_id/actions/unlock``

        `Workspaces Unlock API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#unlock-a-workspace>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/actions/unlock"
        return self._post(url)

    def update(self, payload, workspace_name=None, workspace_id=None):
        """
        ``PATCH /organizations/:organization_name/workspaces/:name``
        ``PATCH /workspaces/:workspace_id``

        `Workspaces Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#update-a-workspace>`_

        `Update Sample Payload \
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

        `Workspaces Assign SSH Key API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#assign-an-ssh-key-to-a-workspace>`_

        `Assign Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-3>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/ssh-key"
        return self._patch(url, data=payload)

    def unassign_ssh_key(self, workspace_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/relationships/ssh-key``

        `Workspaces Unassign SSH Key API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#unassign-an-ssh-key-from-a-workspace>`_

        `Unassign Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-4>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/ssh-key"
        self._patch(url, data=payload)

    def get_remote_state_consumers(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/relationships/remote-state-consumers``

        `Get Remote State Consumers API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#get-remote-state-consumers>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#query-parameters-1>`__
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/remote-state-consumers"
        return self._get(url, page=page, page_size=page_size)

    def replace_remote_state_consumers(self, workspace_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/relationships/remote-state-consumers``

        `Replace Remote State Consumers API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#replace-remote-state-consumers>`_

        `Replace Remote State Consumers Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-5>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/remote-state-consumers"
        return self._patch(url, data=payload)

    def add_remote_state_consumers(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/relationships/remote-state-consumers``

        `Add Remote State Consumers API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#add-remote-state-consumers>`_

        `Add Remote State Consumers Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-6>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/remote-state-consumers"
        return self._post(url, data=payload)

    def delete_remote_state_consumers(self, workspace_id, payload):
        """
        ``DELETE /workspaces/:workspace_id/relationships/remote-state-consumers``

        `Delete Remote State Consumers API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#delete-remote-state-consumers>`_

        `Delete Remote State Consumers Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-7>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/remote-state-consumers"
        return self._destroy(url, data=payload)

    def list_tags(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/relationships/tags``

        `Get Tags API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#get-tags>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#query-parameters-2>`__
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/tags"
        return self._get(url, page=page, page_size=page_size)

    def list_all_tags(self, workspace_id):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every workspace in an organization.

        Returns an object with two arrays of objects.
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/tags"
        return self._list_all(url)

    def add_tags(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/relationships/tags``

        `Add Tags to a Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#add-tags-to-a-workspace>`_

        `Add Tags to a Workspace API Doc Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-8>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/tags"
        return self._post(url, data=payload)

    def remove_tags(self, workspace_id, payload):
        """
        ``DELETE /workspaces/:workspace_id/relationships/tags``

        `Remove Tags from a Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#remove-tags-from-workspace>`_

        `Remove Tags from a Workspace API Doc Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload-9>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/relationships/tags"
        return self._destroy(url, data=payload)

    def list_resources(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/resources``

        `Get Workspace Resources API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/workspace-resources#list-workspace-resources>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/cloud-docs/api-docs/workspace-resources#query-parameters>`__
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/resources"
        return self._get(url, page=page, page_size=page_size)

    def list_all_resources(self, workspace_id):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every workspace in an organization.

        Returns an object with two arrays of objects.
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/resources"
        return self._list_all(url)
