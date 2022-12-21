"""
Module for Terraform Cloud API Endpoint: Run Tasks.
"""

from .endpoint import TFCEndpoint

class TFCRunTasks(TFCEndpoint):
    """
    `Run Tasks API Docs \
        <https://www.terraform.io/docs/cloud/api/run-tasks.html>`_
    """
    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_tasks_base_url = f"{self._api_v2_base_url}/organizations/{self._org_name}/tasks"
        self._tasks_base_url = f"{self._api_v2_base_url}/tasks"
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/tasks``

        `Run Tasks Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#create-a-run-task>`_

        `Run Tasks Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-payload>`_
        """
        return self._create(self._org_tasks_base_url, payload)


    def list(self, page=None, page_size=None, include=None):
        """
        ``GET /organizations/:organization_name/tasks``

        `Run Tasks List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#list-run-tasks>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#query-parameters>`__
        """
        return self._list(self._org_tasks_base_url, page=page, page_size=page_size, include=include)

    def list_all(self):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every run trigger for a workspace.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_tasks_base_url)

    def show(self, task_id, include=None):
        """
        ``GET /tasks/:id``

        `Run Tasks Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#show-a-run-task>`_
        """
        url = f"{self._tasks_base_url}/{task_id}"
        return self._show(url, include=include)

    def update(self, task_id, payload):
        """
        ``PATCH /tasks/:id``

        `Run Tasks Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#update-a-task>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-payload-1>`_
        """
        url = f"{self._tasks_base_url}/{task_id}"
        return self._update(url, payload)

    def destroy(self, task_id):
        """
        ``DELETE /tasks/:id``

        `Run Tasks Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#delete-a-run-task>`_
        """
        url = f"{self._tasks_base_url}/{task_id}"
        return self._destroy(url)

    # WORKSPACE RELATIONSHIPS
    def attach_task_to_workspace(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/tasks``

        `Run Tasks Attach To Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#attach-a-run-task-to-a-workspace>`_

        `Attach Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-payload-2>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks"
        return self._post(url, data=payload)

    def list_tasks_on_workspace(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/tasks``

        `Run Tasks List On Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#list-workspace-run-tasks>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#query-parameters-1>`__
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks"
        return self._get(url, page=page, page_size=page_size)

    def list_all_tasks_on_workspace(self, workspace_id):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every policy for an organization.

        Returns an object with two arrays of objects.
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks"
        return self._list_all(url)

    def show_task_on_workspace(self, workspace_id, task_id):
        """
        ``GET /workspaces/:workspace_id/tasks/:id``

        `Run Tasks Show On Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#show-workspace-run-task>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks/{task_id}"
        return self._get(url)

    def update_task_on_workspace(self, workspace_id, task_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/tasks/:id``

        `Run Tasks Update On Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#update-workspace-run-task>`_

        `Update On Workspace Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-payload-3>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks/{task_id}"
        return self._update(url, payload=payload)

    def remove_task_from_workspace(self, workspace_id, task_id):
        """
        ``DELETE /workspaces/:workspace_id/tasks/:id``

        `Run Tasks Remove From Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#delete-workspace-task>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks/{task_id}"
        return self._destroy(url)
