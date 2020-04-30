"""
Module for Terraform Cloud API Endpoint: Applies.
"""

from .endpoint import TFCEndpoint

class TFCApplies(TFCEndpoint):
    """
    An apply represents the results of applying a Terraform Run's execution plan.

    https://www.terraform.io/docs/cloud/api/applies.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/applies"

    def show(self, apply_id):
        """
        GET /applies/:apply_id

        There is no endpoint to list applies. You can find the ID for an apply in
        the relationships.apply property of a run object.
        """
        url = f"{self._base_url}/{apply_id}"
        return self._show(url)
