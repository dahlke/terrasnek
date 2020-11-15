"""
Module for Terraform Cloud API Endpoint: Audit Trails.
"""

from .endpoint import TFCEndpoint

class TFCAuditTrails(TFCEndpoint):
    """
    `Audit Trails API Docs \
        <https://www.terraform.io/docs/cloud/api/audit-trails.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._audit_trail_api_v2_base_url = f"{self._api_v2_base_url}/organization/audit-trail"

    def _required_entitlements(self):
        return []

    def list(self, since=None, page=None):
        """
        ``GET /organization/audit-trail``

        `Audit Trails List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/audit-trails.html#list-audit-trails>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/audit-trails.html#query-parameters>`_):
            - ``since`` (Optional)
            - ``page`` (Optional)
        """

        return self._list(self._audit_trail_api_v2_base_url, \
            page=page, since=since)
