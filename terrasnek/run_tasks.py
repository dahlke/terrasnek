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
        self._org_event_hooks_base_url = f"{self._api_v2_base_url}/organizations/{self._org_name}/event-hooks"
        self._event_hooks_base_url = f"{self._api_v2_base_url}/event-hooks"
        self._tasks_base_url = f"{self._api_v2_base_url}/tasks"
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        # TODO: remove this once it goes to TFE GA
        return True

    def terraform_enterprise_only(self):
        return False

    def create_event_hook(self, payload):
        """
        ``POST /organizations/:organization_name/event-hooks``

        `Run Tasks Create Event Hook API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#create-an-event-hook>`_

        `Run Tasks Create Event Hook Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-payload>`_
        """
        return self._create(self._org_event_hooks_base_url, payload)


    def list_event_hooks(self, page=None, page_size=None, include=None):
        """
        ``GET /organizations/:organization_name/event-hooks``

        `Run Tasks List Event Hooks API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#list-event-hooks>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#query-parameters>`__):
            - ``page_size`` (Optional)
            - ``page`` (Optional)
            - ``include`` (Optional)
        """
        return self._list(self._org_event_hooks_base_url, page=page, page_size=page_size, include=include)

    def list_all_event_hooks(self):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every run trigger for a workspace.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_event_hooks_base_url)

    def show_event_hook(self, event_hook_id):
        """
        ``GET /event-hooks/:id``

        `Run Tasks Show Event Hook API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#show-an-event-hook>`_
        """
        url = f"{self._event_hooks_base_url}/{event_hook_id}"
        return self._show(url)

    def update_event_hook(self, event_hook_id, payload):
        """
        ``PATCH /event-hooks/:id``

        `Run Tasks Update Event Hook API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#update-a-task>`_

        `Update Event Hook Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-payload-3>`_
        """
        url = f"{self._event_hooks_base_url}/{event_hook_id}"
        return self._update(url, payload)

    def destroy_event_hook(self, event_hook_id):
        """
        ``DELETE /event-hooks/:id``

        `Run Tasks Destroy Event Hook API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#delete-an-event-hook>`_
        """
        url = f"{self._event_hooks_base_url}/{event_hook_id}"
        return self._destroy(url)

    def attach_event_hook_as_task(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/tasks``

        `Run Tasks Attach Event Hook API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#attach-an-event-hook-to-a-workspace-as-a-task>`_

        `Attach Event Hook Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-payload-2>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks"
        return self._post(url, data=payload)

    def list(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/tasks``

        `Run Tasks List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#list-tasks>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#query-parameters-1>`__):
            - ``page_size`` (Optional)
            - ``page`` (Optional)
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/tasks"
        return self._list(url, page=page, page_size=page_size)

    def show(self, task_id):
        """
        ``GET /tasks/:id``

        `Run Tasks Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#show-a-task>`_
        """
        url = f"{self._tasks_base_url}/{task_id}"
        return self._show(url)

    def update(self, task_id, payload):
        """
        ``PATCH /tasks/:id``

        `Run Tasks Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#update-a-task>`_

        `Run Tasks Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#sample-response-7>`_
        """
        url = f"{self._tasks_base_url}/{task_id}"
        return self._update(url, payload)

    def destroy(self, task_id):
        """
        ``DELETE /tasks/:id``

        `Run Tasks Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#delete-a-task>`_
        """
        url = f"{self._tasks_base_url}/{task_id}"
        return self._destroy(url)
