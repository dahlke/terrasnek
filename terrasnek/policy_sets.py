"""
Module for Terraform Cloud API Endpoint: Policy Sets.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicySets(TFCEndpoint):
    """
        Policy sets are groups of policies that are applied together to related
        workspaces. By using policy sets, you can group your policies by
        attributes such as environment or region. Individual policies within a
        policy set will only be checked for workspaces that the policy set
        is attached to.

        Policy sets can group indidual policies created via the policies API,
        or act as versioned sets which are either sourced from a version control
        system (such as GitHub) or uploaded as a whole via the policy set
        versions API.

        https://www.terraform.io/docs/cloud/api/policy-sets.html
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
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self, filters=None, include=None, page=None, page_size=None, search=None):
        """
        ``GET /organizations/:organization_name/policy-sets``

        PARAMS:
            https://www.terraform.io/docs/cloud/api/policy-sets.html#list-policy-sets
        """
        return self._list(\
            self._org_api_v2_base_url, \
            filters=filters, include=include, \
            page=page, page_size=page_size, search=search)

    def show(self, policy_set_id):
        """
        ``GET /policy-sets/:id``
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._show(url)

    def update(self, policy_set_id, payload):
        """
        ``PATCH /policy-sets/:id``
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._update(url, payload)

    def destroy(self, policy_set_id):
        """
        ``DELETE /policies/:policy_set_id``
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._destroy(url)

    def add_policies_to_set(self, policy_set_id, payload):
        """
        ``POST /policy-sets/:id/relationships/policies``
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/relationships/policies"
        return self._post(url, data=payload)

    def remove_policies_from_set(self, policy_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/policies``
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/policies"
        return self._delete(url, data=payload)

    def attach_policy_set_to_workspaces(self, policy_id, payload):
        """
        ``POST /policy-sets/:id/relationships/workspaces``
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/workspaces"
        return self._post(url, data=payload)

    def detach_policy_set_from_workspaces(self, policy_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/workspaces``
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/workspaces"
        return self._delete(url, data=payload)

    def create_policy_set_version(self, policy_set_id):
        """
        ``POST /policy-sets/:id/versions``

        For versioned policy sets which have no VCS repository attached,
        versions of policy code may be uploaded directly to the API by
        creating a new policy set version and, in a subsequent request,
        uploading a tarball (tar.gz) of data to it.
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/versions"
        return self._post(url)

    def show_policy_set_version(self, policy_set_version_id):
        """
        ``GET /policy-set-versions/:id``
        """
        url = f"{self._pol_set_version_api_v2_base_url}/{policy_set_version_id}"
        return self._get(url)

    def upload(self, path_to_tarball, policy_set_version_id):
        """
        ``PUT {derived_policy_set_upload_url}``
        """
        url = self.show_policy_set_version(policy_set_version_id)["data"]["links"]["upload"]
        data = None
        with open(path_to_tarball, 'rb') as data_bytes:
            data = data_bytes.read()

        return self._put(url, data=data)
