"""
Module for Terraform Cloud API Endpoint: Audit Trails.
"""

from .endpoint import TFCEndpoint
from ._constants import MAX_PAGE_SIZE

class TFCAuditTrails(TFCEndpoint):
    """
    `Audit Trails API Docs \
        <https://www.terraform.io/docs/cloud/api/audit-trails.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._audit_trail_api_v2_base_url = f"{self._api_v2_base_url}/organization/audit-trail"

    def required_entitlements(self):
        return []

    def list(self, since=None, page=None, page_size=None):
        """
        ``GET /organization/audit-trail``

        `Audit Trails List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/audit-trails.html#list-audit-trails>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/audit-trails.html#query-parameters>`_):
            - ``since`` (Optional)
            - ``page_size`` (Optional)
            - ``page`` (Optional)
        """

        return self._list(self._audit_trail_api_v2_base_url, \
            page=page, page_size=page_size, since=since)

    def list_all(self):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every audit trail in an organization.

        Returns an array of objects.
        """
        current_page_number = 1
        audit_trails_resp = \
            self._list(self._audit_trail_api_v2_base_url, page=current_page_number, page_size=MAX_PAGE_SIZE)
        total_pages = audit_trails_resp["pagination"]["total_pages"]

        audit_trails = []
        while current_page_number <= total_pages:
            audit_trails_resp = \
                self._list(self._audit_trail_api_v2_base_url, \
                    page=current_page_number, page_size=MAX_PAGE_SIZE)
            audit_trails += audit_trails_resp["data"]
            current_page_number += 1

        return audit_trails