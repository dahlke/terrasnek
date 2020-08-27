"""
Module for Terraform Cloud API Endpoint: Audit Trails.
"""

from .endpoint import TFCEndpoint

class TFCAuditTrails(TFCEndpoint):
    """
    The Audit Trails API exposes a stream of audit events, which describe
    changes to the application entities (workspaces, runs, etc.) that
    belong to a Terraform Cloud organization.

    https://www.terraform.io/docs/cloud/api/audit-trails.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._audit_trail_api_v2_base_url = f"{self._api_v2_base_url}/audit-trail"

    def required_entitlements(self):
        return []

    def list(self, since=None, page=None):
        """
        ``GET /organization/audit-trail``
        """
        return self._list(self._audit_trail_api_v2_base_url, \
            page=page, since=since)
