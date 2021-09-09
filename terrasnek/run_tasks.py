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
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create_event_hook(self, payload):
        """
        ``POST /organizations/:organization_name/event-hooks``

        `Run Tasks Create Event Hook API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#create-an-event-hook>`_

        `Create Event Hook Sample Payload \
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

    def destroy_event_hook(self, event_hook_id):
        """
        ``DELETE /event-hooks/:id``

        `Run Tasks Destroy Event Hook API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-tasks.html#delete-an-event-hook>`_
        """
        url = f"{self._event_hooks_base_url}/{event_hook_id}"
        return self._destroy(url)

    def attach_event_hook_as_task(self):
        pass

    def list(self, workspace_id):
        pass

    def show(self, workspace_id):
        pass

    def update(self, workspace_id):
        pass

    def destroy(self, workspace_id):
        pass