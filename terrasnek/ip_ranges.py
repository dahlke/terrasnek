"""
Module for Terraform Cloud API Endpoint: IP Ranges.
"""

from .endpoint import TFCEndpoint

class TFCIPRanges(TFCEndpoint):
    """
    The IP Ranges API is used to list egress IP ranges.

    https://www.terraform.io/docs/cloud/api/ip-ranges.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._meta_base_url}/ip-ranges"

    def required_entitlements(self):
        return []

    def list(self):
        """
        ``GET /meta/ip-ranges``
        """
        return self._list(self._endpoint_base_url)
