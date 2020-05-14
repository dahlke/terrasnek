"""
Module for Terraform Cloud API Endpoint: Cost Estimates.
"""

from .endpoint import TFCEndpoint

class TFCCostEstimates(TFCEndpoint):
    """
    A cost represents the cost estimates for many resources found in a TFC workspace.

    https://www.terraform.io/docs/cloud/api/cost-estimates.html
    """

    def __init__(self, instance_url, org_name, headers, verify):
        super().__init__(instance_url, org_name, headers, verify)
        self._api_v2_base_url = f"{self._api_v2_base_url}/cost-estimates"

    def required_entitlements(self):
        return []

    def show(self, cost_est_id):
        """
        ``GET /cost-estimates/:cost_est_id``
        """
        url = f"{self._api_v2_base_url}/{cost_est_id}"
        return self._show(url)
