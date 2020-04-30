"""
Module for Terraform Cloud API Endpoint: Policy Set Params.
"""


from .endpoint import TFCEndpoint

class TFCPolicySetParams(TFCEndpoint):
    """
        https://www.terraform.io/docs/cloud/api/policy-set-params.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/policy-sets"

    def create(self, policy_set_id, payload):
        """
        POST /policy-sets/:policy_set_id/parameters
        """
        url = f"{self._base_url}/{policy_set_id}/parameters"
        return self._create(url, payload)

    def list(self, policy_set_id):
        """
        GET /policy-sets/:policy_set_id/parameters
        """
        url = f"{self._base_url}/{policy_set_id}/parameters"
        return self._list(url)

    def update(self, policy_set_id, parameter_id, payload):
        """
        PATCH /policy-sets/:policy_set_id/parameters/:parameter_id
        """
        url = f"{self._base_url}/{policy_set_id}/parameters/{parameter_id}"
        return self._update(url, payload)

    def destroy(self, policy_set_id, parameter_id):
        """
        DELETE /policy-sets/:policy_set_id/parameters/:parameter_id
        """
        url = f"{self._base_url}/{policy_set_id}/parameters/{parameter_id}"
        return self._destroy(url)
