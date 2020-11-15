"""
Module for Terraform Cloud API Endpoint: Policy Set Params.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicySetParams(TFCEndpoint):
    """
    `Policy Set Params API Docs \
        <https://www.terraform.io/docs/cloud/api/policy-set-params.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policy-sets"

    def _required_entitlements(self):
        return [Entitlements.SENTINEL]

    def create(self, policy_set_id, payload):
        """
        ``POST /policy-sets/:policy_set_id/parameters``

        `Policy Set Params Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-set-params.html#create-a-parameter>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-set-params.html#sample-payload>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/parameters"
        return self._create(url, payload)

    def list(self, policy_set_id):
        """
        ``GET /policy-sets/:policy_set_id/parameters``

        `Policy Set Params List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-set-params.html#list-parameters>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/parameters"
        return self._list(url)

    def update(self, policy_set_id, parameter_id, payload):
        """
        ``PATCH /policy-sets/:policy_set_id/parameters/:parameter_id``

        `Policy Set Params Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-set-params.html#update-parameters>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-set-params.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/parameters/{parameter_id}"
        return self._update(url, payload)

    def destroy(self, policy_set_id, parameter_id):
        """
        ``DELETE /policy-sets/:policy_set_id/parameters/:parameter_id``

        `Policy Set Params Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-set-params.html#delete-parameters>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/parameters/{parameter_id}"
        return self._destroy(url)
