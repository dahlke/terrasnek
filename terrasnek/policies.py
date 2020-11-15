"""
Module for Terraform Cloud API Endpoint: Policies.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicies(TFCEndpoint):
    """
    `Policies API Docs \
        <https://www.terraform.io/docs/cloud/api/policies.html>`_
    """
    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policies"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/policies"

    def _required_entitlements(self):
        return [Entitlements.SENTINEL]

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/policies``

        `Policies Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#create-a-policy>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self, page=None, page_size=None, search=None):
        """
        ``GET /organizations/:organization_name/policies``

        `Policies List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#list-policies>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/policies.html#query-parameters>`_):
            - ``page`` (Optional)
            - ``page_size`` (Optional)
            - ``search`` (Optional)
        """
        return self._list(\
            self._org_api_v2_base_url, page=page, page_size=page_size, search=search)

    def show(self, policy_id):
        """
        ``GET /policies/:policy_id``

        `Policies Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#show-a-policy>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}"
        return self._show(url)

    def update(self, policy_id, payload):
        """
        ``PATCH /policies/:policy_id``

        `Policies Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#update-a-policy>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-payload-2>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}"
        return self._update(url, payload)

    def upload(self, policy_id, payload):
        """
        ``PUT /policies/:policy_id/upload``

        `Policies Upload API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#upload-a-policy>`_

        `Upload Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/upload"
        return self._put(url, octet=True, data=payload)

    def destroy(self, policy_id):
        """
        ``DELETE /policies/:policy_id``

        `Policies Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#delete-a-policy>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}"
        return self._destroy(url)
