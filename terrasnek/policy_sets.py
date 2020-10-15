"""
Module for Terraform Cloud API Endpoint: Policy Sets.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicySets(TFCEndpoint):
    """
    `API Docs \
        <https://www.terraform.io/docs/cloud/api/policy-sets.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policy-sets"
        self._pol_set_version_api_v2_base_url = f"{self._api_v2_base_url}/policy-set-versions"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/policy-sets"

    def required_entitlements(self):
        return [Entitlements.SENTINEL]

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/policy-sets``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#create-a-policy-set>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self, filters=None, include=None, page=None, page_size=None, search=None):
        """
        ``GET /organizations/:organization_name/policy-sets``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#list-policy-sets>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#query-parameters>`_):
            - ``filter[versioned]`` (Optional)
            - ``include`` (Optional)
            - ``page`` (Optional)
            - ``page_size`` (Optional)
            - ``search`` (Optional)

        Example filter(s):

        .. code-block:: python

            filters = [
                {
                    "keys": ["versioned"],
                    "value": "foo"
                }
            ]
        """
        return self._list(\
            self._org_api_v2_base_url, \
            filters=filters, include=include, \
            page=page, page_size=page_size, search=search)

    def show(self, policy_set_id):
        """
        ``GET /policy-sets/:id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#show-a-policy-set>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._show(url)

    def update(self, policy_set_id, payload):
        """
        ``PATCH /policy-sets/:id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#update-a-policy-set>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._update(url, payload)

    def destroy(self, policy_set_id):
        """
        ``DELETE /policies/:policy_set_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#delete-a-policy-set>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._destroy(url)

    def add_policies_to_set(self, policy_set_id, payload):
        """
        ``POST /policy-sets/:id/relationships/policies``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#add-policies-to-the-policy-set>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-2>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/relationships/policies"
        return self._post(url, data=payload)

    def attach_policy_set_to_workspaces(self, policy_id, payload):
        """
        ``POST /policy-sets/:id/relationships/workspaces``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#attach-a-policy-set-to-workspaces>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-3>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/workspaces"
        return self._post(url, data=payload)

    def remove_policies_from_set(self, policy_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/policies``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#remove-policies-from-the-policy-set>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-4>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/policies"
        return self._delete(url, data=payload)

    def detach_policy_set_from_workspaces(self, policy_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/workspaces``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#detach-the-policy-set-from-workspaces>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-5>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/workspaces"
        return self._delete(url, data=payload)

    def create_policy_set_version(self, policy_set_id):
        """
        ``POST /policy-sets/:id/versions``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#create-a-policy-set-version>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/versions"
        return self._post(url)

    def show_policy_set_version(self, policy_set_version_id):
        """
        ``GET /policy-set-versions/:id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#show-a-policy-set-version>`_
        """
        url = f"{self._pol_set_version_api_v2_base_url}/{policy_set_version_id}"
        return self._get(url)

    def upload(self, path_to_tarball, policy_set_version_id):
        """
        ``PUT {derived_policy_set_upload_url}``
        ``PUT https://archivist.terraform.io/v1/object/<UNIQUE OBJECT ID>``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#upload-policy-set-versions>`_
        """
        url = self.show_policy_set_version(policy_set_version_id)["data"]["links"]["upload"]
        data = None
        with open(path_to_tarball, 'rb') as data_bytes:
            data = data_bytes.read()

        return self._put(url, data=data)
