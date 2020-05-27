"""
Module for Terraform Cloud API Endpoint: Applies.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCApplies(TFCEndpoint):
    """
    An apply represents the results of applying a Terraform Run's execution plan.

    https://www.terraform.io/docs/cloud/api/applies.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/applies"

    def required_entitlements(self):
        return [Entitlements.OPERATIONS]

    def show(self, apply_id):
        """
        ``GET /applies/:id``

        There is no endpoint to list applies. You can find the ID for an apply in
        the relationships.apply property of a run object.
        """
        url = f"{self._endpoint_base_url}/{apply_id}"
        return self._show(url)
