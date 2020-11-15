"""
Module for Terraform Cloud API Endpoint: Policy Checks.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicyChecks(TFCEndpoint):
    """
    `Policy Checks API Docs \
        <https://www.terraform.io/docs/cloud/api/policy-checks.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policy-checks"
        self._runs_api_v2_base_url = f"{self._api_v2_base_url}/runs"

    def _required_entitlements(self):
        return [Entitlements.SENTINEL]

    def list(self, run_id):
        """
        ``GET /runs/:run_id/policy-checks``

        `Policy Checks List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-checks.html#list-policy-checks>`_
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/policy-checks"
        return self._list(url)

    def override(self, policy_check_id):
        """
        ``POST /policy-checks/:policy_check_id/actions/override``

        `Policy Checks Override API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-checks.html#override-policy>`_
        """
        url = f"{self._endpoint_base_url}/{policy_check_id}/actions/override"
        return self._post(url)
