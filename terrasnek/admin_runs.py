"""
Module for Terraform Cloud API Endpoint: Admin Runs.
"""

from .endpoint import TFCEndpoint

class TFCAdminRuns(TFCEndpoint):
    """
    `Admin Runs API Docs \
        <https://www.terraform.io/docs/cloud/api/admin/runs.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/runs"

    def _required_entitlements(self):
        return []

    def list(self, query=None, filters=None, page=None, page_size=None):
        """
        ``GET /admin/runs``

        `Admin List Runs API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/runs.html#list-all-runs>`_
        """
        return self._list(self._endpoint_base_url, \
            query=query, filters=filters, page=page, page_size=page_size)

    def force_cancel(self, run_id, data=None):
        """
        ``POST /admin/runs/:id/actions/force-cancel``

        `Admin Force Cancel Run API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/runs.html#force-a-run-into-the-quot-cancelled-quot-state>`_
        """
        url = f"{self._endpoint_base_url}/{run_id}/actions/force-cancel"
        return self._post(url, data=data)
