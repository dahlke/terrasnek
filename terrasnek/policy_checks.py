"""
Module for Terraform Cloud API Endpoint: Policy Checks.
"""


from .endpoint import TFCEndpoint

class TFCPolicyChecks(TFCEndpoint):
    """
        https://www.terraform.io/docs/cloud/api/policy-checks.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/policy-checks"
        self._runs_base_url = f"{base_url}/runs"

    def list(self, run_id):
        """
        ``GET /runs/:run_id/policy-checks``

        This endpoint lists the policy checks in a run.
        """
        url = f"{self._runs_base_url}/{run_id}/policy-checks"
        return self._list(url)

    def override(self, policy_check_id):
        """
        ``POST /policy-checks/:policy_check_id/actions/override``
        """
        url = f"{self._base_url}/{policy_check_id}/actions/override"
        return self._post(url)
