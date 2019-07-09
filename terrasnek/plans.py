"""
Module for Terraform Enterprise API Endpoint: Plans.
"""

from .endpoint import TFEEndpoint

class TFEPlans(TFEEndpoint):
    """
    A plan represents the execution plan of a Run in a Terraform workspace.

    https://www.terraform.io/docs/enterprise/api/plans.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._base_url = f"{base_url}/plans"

    def show(self, plan_id):
        """
        GET /plans/:plan_id
        """
        url = f"{self._base_url}/{plan_id}"
        return self._show(url)
