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

    def required_entitlements(self):
        # NOTE: Entitlements.SENTINEL has been deprecated, using Policy Enforcement instead.
        return [Entitlements.POLICY_ENFORCEMENT]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/policies``

        `Policies Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#create-a-policy>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self, page=None, page_size=None, search=None, include=None):
        """
        ``GET /organizations/:organization_name/policies``

        `Policies List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#list-policies>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/policies.html#query-parameters>`__
        """
        return self._list(self._org_api_v2_base_url, \
            page=page, page_size=page_size, search=search, include=include)

    def list_all(self, search=None, include=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every policy for an organization.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_api_v2_base_url, include=include, search=search)

    def show(self, policy_id, include=None):
        """
        ``GET /policies/:policy_id``

        `Policies Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#show-a-policy>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}"
        return self._show(url, include=include)

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

    def get_policy_text(self, policy_id, include=None):
        """
        ``GET /policies/:policy_id/download``

        This endpoint is currently not documented in the offical TFC API docs. You can find a
        reference to it in the `sample response \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-response-1>` for the
        `show` function.
        """
        url = f"{self._endpoint_base_url}/{policy_id}/download"
        byte_results = self._get(url, return_raw=True, allow_redirects=True, include=include)
        return byte_results.decode("utf-8")

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
