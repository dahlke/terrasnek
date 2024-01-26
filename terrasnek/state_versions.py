"""
Module for Terraform Cloud API Endpoint: State Versions.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCStateVersions(TFCEndpoint):
    """
    `State Versions API Docs \
        <https://www.terraform.io/docs/cloud/api/state-versions.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._state_version_api_v2_base_url = f"{self._api_v2_base_url}/state-versions"
        self._workspace_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return [Entitlements.STATE_STORAGE]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/state-versions``

        `State Versions Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#create-a-state-version>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#sample-payload>`_
        """
        url = f"{self._workspace_api_v2_base_url}/{workspace_id}/state-versions"
        return self._create(url, payload)

    def get_current(self, workspace_id, include=None):
        """
        ``GET /workspaces/:workspace_id/current-state-version``

        `State Versions Get Current API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#fetch-the-current-state-version-for-a-workspace>`_
        """
        url = f"{self._workspace_api_v2_base_url}/{workspace_id}/current-state-version"
        return self._get(url, include=include)

    def list(self, filters, page=None, page_size=None, include=None):
        """
        ``GET /state-versions``

        `State Versions List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#list-state-versions-for-a-workspace>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#query-parameters>`__
        """
        url = f"{self._state_version_api_v2_base_url}"
        return self._list(url, filters=filters, page=page, page_size=page_size, include=include)

    def list_all(self, filters, include=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every state version for a workspace.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._state_version_api_v2_base_url, filters=filters, include=include)


    def list_state_version_outputs(self, state_version_id):
        """
        ``GET /state-versions/:state_version_id/outputs``

        `List State Version Outputs API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#list-state-version-outputs>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#query-parameters>`__
        """
        url = f"{self._state_version_api_v2_base_url}/{state_version_id}/outputs"
        return self._list(url)

    def show(self, state_version_id, include=None):
        """
        ``GET /state-versions/:state_version_id``

        `State Versions Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-versions.html#show-a-state-version>`_
        """
        url = f"{self._state_version_api_v2_base_url}/{state_version_id}"
        return self._show(url, include=include)

    def rollback(self, workspace_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/state-versions``

        `State Versions Rollback API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#rollback-to-a-previous-state-version>`_

        `Rollback Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#sample-payload-1>`_
        """
        url = f"{self._workspace_api_v2_base_url}/{workspace_id}/state-versions"
        return self._patch(url, data=payload)

    def mark_for_garbage_collection(self, state_version_id):
        """
        ``POST /api/v2/state-versions/:state_version_id/actions/soft_delete_backing_data``

        `State Versions Mark for Garbage Collection API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#mark-a-state-version-for-garbage-collection>`_
        """
        url = f"{self._state_version_api_v2_base_url}/{state_version_id}/actions/soft_delete_backing_data"
        print("marked", url)
        return self._post(url)

    def restore_marked_for_garbage_collection(self, state_version_id):
        """
        ``POST /api/v2/state-versions/:state_version_id/actions/restore_backing_data``

        `State Versions Restore Marked for Garbage Collection API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#restore-a-state-version-marked-for-garbage-collection>`_
        """
        url = f"{self._state_version_api_v2_base_url}/{state_version_id}/actions/restore_backing_data"
        print("unmarked", url)
        return self._post(url)

    def permanently_delete_state_version(self, state_version_id):
        """
        ``POST /api/v2/state-versions/:state_version_id/actions/permanently_delete_backing_data``

        `State Versions Permanently Delete API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#permanently-delete-a-state-version>`_
        """
        url = f"{self._state_version_api_v2_base_url}/{state_version_id}/actions/permanently_delete_backing_data"
        return self._post(url)
