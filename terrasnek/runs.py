"""
Module for Terraform Cloud API Endpoint: Runs.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCRuns(TFCEndpoint):
    """
    `Runs API Docs \
        <https://www.terraform.io/docs/cloud/api/run.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"
        self._runs_api_v2_base_url = f"{self._api_v2_base_url}/runs"

    def _required_entitlements(self):
        return [Entitlements.OPERATIONS]

    def list(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/runs``

        `Runs List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#list-runs-in-a-workspace>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/run.html#query-parameters>`_):
            - ``page`` (Optional)
            - ``page_size`` (Optional)
        """

        url = f"{self._ws_api_v2_base_url}/{workspace_id}/runs"
        return self._list(url, page=page, page_size=page_size)

    def show(self, run_id):
        """
        ``GET /runs/:run_id``

        `Runs Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#get-run-details>`_
        """

        url = f"{self._runs_api_v2_base_url}/{run_id}"
        return self._show(url)

    def create(self, payload):
        """
        ``POST /runs``

        `Runs Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#create-a-run>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run.html#sample-payload>`_
        """

        return self._create(self._runs_api_v2_base_url, payload)

    def apply(self, run_id, payload):
        """
        ``POST /runs/:run_id/actions/apply``

        `Runs Apply API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#apply-a-run>`_
        """

        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/apply"
        return self._post(url, data=payload)

    def discard(self, run_id, payload):
        """
        ``POST /runs/:run_id/actions/discard``

        `Runs Discard API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#discard-a-run>`_
        """

        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/discard"
        return self._post(url, data=payload)

    def cancel(self, run_id, payload):
        """
        ``POST /runs/:run_id/actions/cancel``

        `Runs Cancel API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#cancel-a-run>`_
        """

        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/cancel"
        return self._post(url, data=payload)

    def force_cancel(self, run_id, payload):
        """
        ``POST /runs/:run_id/actions/force-cancel``

        `Runs Force Cancel API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#forcefully-cancel-a-run>`_
        """

        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/force-cancel"
        return self._post(url, data=payload)

    def force_execute(self, run_id):
        """
        ``POST /runs/:run_id/actions/force-execute``

        `Runs Force Execute API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run.html#forcefully-execute-a-run>`_
        """

        url = f"{self._runs_api_v2_base_url}/{run_id}/actions/force-execute"
        return self._post(url)
