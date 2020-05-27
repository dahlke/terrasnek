"""
Module for Terraform Cloud API Endpoint: Policy Checks.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicyChecks(TFCEndpoint):
    """
        https://www.terraform.io/docs/cloud/api/policy-checks.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policy-checks"
        self._runs_api_v2_base_url = f"{self._api_v2_base_url}/runs"

    def required_entitlements(self):
        return [Entitlements.SENTINEL]

    def list(self, run_id):
        """
        ``GET /runs/:run_id/policy-checks``

        This endpoint lists the policy checks in a run.
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/policy-checks"
        return self._list(url)

    def override(self, policy_check_id):
        """
        ``POST /policy-checks/:policy_check_id/actions/override``
        """
        url = f"{self._endpoint_base_url}/{policy_check_id}/actions/override"
        return self._post(url)
