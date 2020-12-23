"""
Module for Terraform Cloud API Endpoint: IP Ranges.
"""

from .endpoint import TFCEndpoint

class TFCIPRanges(TFCEndpoint):
    """
    `IP Ranges API Docs \
        <https://www.terraform.io/docs/cloud/api/ip-ranges.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._meta_base_url}/ip-ranges"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return True

    def terraform_enterprise_only(self):
        return False

    def list(self):
        """
        ``GET /meta/ip-ranges``

        `IP Ranges List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/ip-ranges.html#get-ip-ranges>`_
        """
        return self._list(self._endpoint_base_url)
