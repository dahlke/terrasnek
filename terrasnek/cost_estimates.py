"""
Module for Terraform Cloud API Endpoint: Cost Estimates.
"""

from .endpoint import TFCEndpoint

class TFCCostEstimates(TFCEndpoint):
    """
    `Cost Estimates API Docs \
        <https://www.terraform.io/docs/cloud/api/cost-estimates.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/cost-estimates"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def show(self, cost_est_id):
        """
        ``GET /cost-estimates/:id``

        `Cost Estimates Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/cost-estimates.html#show-a-cost-estimate>`_
        """
        url = f"{self._endpoint_base_url}/{cost_est_id}"
        return self._show(url)
