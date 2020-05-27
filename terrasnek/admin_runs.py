"""
Module for Terraform Cloud API Endpoint: Admin Runs.
"""

from .endpoint import TFCEndpoint

class TFCAdminRuns(TFCEndpoint):
    """
    The Admin API is exclusive to Terraform Enterprise, and can only be used
    by the admins and operators who install and maintain their organization's
    Terraform Enterprise instance.

    The Runs Admin API contains endpoints to help site administrators manage
    runs.

    https://www.terraform.io/docs/cloud/api/admin/runs.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/runs"

    def required_entitlements(self):
        return []

    def list(self, query=None, filters=None, page=None, page_size=None):
        """
        ``GET /admin/runs``

        This endpoint lists all runs in the Terraform Cloud installation.
        """
        return self._list(self._endpoint_base_url, \
            query=query, filters=filters, page=page, page_size=page_size)

    def force_cancel(self, run_id, data=None):
        """
        ``POST /admin/runs/:id/actions/force-cancel``

        This endpoint forces a run (and its plan/apply, if applicable) into
        the "canceled" state. This action should only be performed for runs
        that are stuck and no longer progressing normally, as there is a risk
        of lost state data if a progressing apply is force-canceled. Healthy
        runs can be requested for cancellation by end-users.
        """
        url = f"{self._endpoint_base_url}/{run_id}/actions/force-cancel"
        return self._post(url, data=data)
