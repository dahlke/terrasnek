"""
Module for Terraform Cloud API Endpoint: Plans.
"""

from .endpoint import TFCEndpoint


class TFCPlans(TFCEndpoint):
    """
    A plan represents the execution plan of a Run in a Terraform workspace.

    https://www.terraform.io/docs/cloud/api/plans.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/plans"

    def show(self, plan_id):
        """
        GET /plans/:plan_id
        """
        url = f"{self._base_url}/{plan_id}"
        return self._show(url)
