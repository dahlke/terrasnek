"""
Module for Terraform Cloud API Endpoint: Runs.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCRuns(TFCEndpoint):
    """
    Performing a run on a new configuration is a multi-step process.

    - Create a configuration version on the workspace.
    - Upload configuration files to the configuration version.
    - Create a run on the workspace; this is done automatically when a config file is uploaded.
    - Create and queue an apply on the run; if the run can't be auto-applied.

    Alternatively, you can create a run with a pre-existing configuration version, even one from
    another workspace. This is useful for promoting known good code from one workspace to another.

    https://www.terraform.io/docs/cloud/api/run.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"
        self._runs_api_v2_base_url = f"{self._api_v2_base_url}/runs"

    def required_entitlements(self):
        return [Entitlements.OPERATIONS]

    def list(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/runs``

        This endpoint supports pagination with standard URL query parameters; remember to
        percent-encode.
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/runs"
        return self._list(url, page=page, page_size=page_size)

    def show(self, run_id):
        """
        ``GET /runs/:run_id``

        This endpoint is used for showing details of a specific run.
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}"
        return self._show(url)

    def create(self, payload):
        """
        ``POST /runs``

        A run performs a plan and apply, using a configuration version and the workspace’s
        current variables. You can specify a configuration version when creating a run; if
        you don’t provide one, the run defaults to the workspace’s most recently used version.
        """
        return self._create(self._runs_api_v2_base_url, payload)

    def apply(self, run_id):
        """
        ``POST /runs/:run_id/actions/apply``

        Applies a run that is paused waiting for confirmation after a plan. This includes runs
        in the "needs confirmation" and "policy checked" states. This action is only required for
        runs that can't be auto-applied. (Plans can be auto-applied if the auto-apply setting is
        enabled on the workspace, the plan is not a destroy plan, and the plan was not queued by a
        user without write permissions.)

        This endpoint queues the request to perform an apply; the apply might not happen
        immediately.

        This endpoint represents an action as opposed to a resource. As such, the endpoint does
        not return any object in the response body.
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/apply"
        return self._post(url)

    def discard(self, run_id):
        """
        ``POST /runs/:run_id/actions/discard``

        The discard action can be used to skip any remaining work on runs that are paused
        waiting for confirmation or priority. This includes runs in the "pending,"
        "needs confirmation," "policy checked," and "policy override" states.

        This endpoint queues the request to perform a discard; the discard might not happen
        immediately. After discarding, the run is completed and later runs can proceed.

        This endpoint represents an action as opposed to a resource. As such, it does not
        return any object in the response body.
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/discard"
        return self._post(url)

    def cancel(self, run_id):
        """
        ``POST /runs/:run_id/actions/cancel``

        The cancel action can be used to interrupt a run that is currently planning or applying.
        Performing a cancel is roughly equivalent to hitting ctrl+c during a Terraform plan or
        apply on the CLI. The running Terraform process is sent an INT signal, which instructs
        Terraform to end its work and wrap up in the safest way possible.

        This endpoint queues the request to perform a cancel; the cancel might not happen
        immediately. After canceling, the run is completed and later runs can proceed.

        This endpoint represents an action as opposed to a resource. As such, it does not
        return any object in the response body.
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/cancel"
        return self._post(url)

    def force_cancel(self, run_id):
        """
        ``POST /runs/:run_id/actions/force-cancel``

        The force-cancel action is like cancel, but ends the run immediately. Once invoked,
        the run is placed into a canceled state, and the running Terraform process is terminated.
        The workspace is immediately unlocked, allowing further runs to be queued. The force-cancel
        operation requires workspace admin privileges.

        This endpoint enforces a prerequisite that a non-forceful cancel is performed first, and a
        cool-off period has elapsed. To determine if this criteria is met, it is useful to check
        the data.attributes.is-force-cancelable value of the run details endpoint. The time at
        which the force-cancel action will become available can be found using the run details
        endpoint, in the key data.attributes.force_cancel_available_at. Note that this key is only
        present in the payload after the initial cancel has been initiated.

        This endpoint represents an action as opposed to a resource. As such, it does not return any
        object in the response body.
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/force-cancel"
        return self._post(url)

    def force_execute(self, run_id):
        """
        ``POST /runs/:run_id/actions/force-execute``

        The force-execute action cancels all prior runs that are not already complete, unlocking
        the run's workspace and allowing the run to be executed. (It initiates the same actions
        as the "Run this plan now" button at the top of the view of a pending run.)

        This endpoint enforces the following prerequisites:
            The target run is in the "pending" state.
            The workspace is locked by another run.
            The run locking the workspace can be discarded.

        This endpoint represents an action as opposed to a resource. As such, it does not return any
        object in the response body.
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/force-execute"
        return self._post(url)
