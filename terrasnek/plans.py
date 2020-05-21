"""
Module for Terraform Cloud API Endpoint: Plans.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCPlans(TFCEndpoint):
    """
    A plan represents the execution plan of a Run in a Terraform workspace.

    https://www.terraform.io/docs/cloud/api/plans.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify)
        self._endpoint_base_url = f"{self._api_v2_base_url}/plans"

    def required_entitlements(self):
        return [Entitlements.OPERATIONS]

    def show(self, plan_id):
        """
        ``GET /plans/:plan_id``

        There is no endpoint to list plans. You can find the ID for a plan
        in the relationships.plan property of a run object.
        """
        url = f"{self._endpoint_base_url}/{plan_id}"
        return self._show(url)
