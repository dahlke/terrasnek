"""
Module for Terraform Cloud API Endpoint: Policy Sets.
"""

from .endpoint import TFCEndpoint

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

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/policy-sets"
        self._org_base_url = f"{base_url}/organizations/{org_name}/policy-sets"

    def create(self, payload):
        """
        POST /organizations/:org_name/policy-sets
        """
        return self._create(self._org_base_url, payload)

    def list(self, filters=None, include=None, page=None, page_size=None, search=None):
        """
        GET /organizations/:org_name/policy-sets

        PARAMS:
            https://www.terraform.io/docs/cloud/api/policy-sets.html#list-policy-sets
        """
        return self._list(\
            self._org_base_url, \
            filters=filters, include=include, \
            page=page, page_size=page_size, search=search)

    def show(self, policy_set_id):
        """
        GET /policy-sets/:id
        """
        url = f"{self._base_url}/{policy_set_id}"
        return self._show(url)

    def update(self, policy_set_id, payload):
        """
        PATCH /policy-sets/:id
        """
        url = f"{self._base_url}/{policy_set_id}"
        return self._update(url, payload)

    def destroy(self, policy_set_id):
        """
        DELETE /policies/:policy_set_id
        """
        url = f"{self._base_url}/{policy_set_id}"
        return self._destroy(url)

    def add_policies_to_set(self, policy_set_id, payload):
        """
        POST /policy-sets/:id/relationships/policies
        """
        url = f"{self._base_url}/{policy_set_id}/relationships/policies"
        return self._post(url, data=payload)

    def remove_policies_from_set(self, policy_id, payload):
        """
        DELETE /policy-sets/:id/relationships/policies
        """
        url = f"{self._base_url}/{policy_id}/relationships/policies"
        return self._delete(url, data=payload)

    def attach_policy_set_to_workspaces(self, policy_id, payload):
        """
        POST /policy-sets/:id/relationships/workspaces
        """
        url = f"{self._base_url}/{policy_id}/relationships/workspaces"
        return self._post(url, data=payload)

    def detach_policy_set_from_workspaces(self, policy_id, payload):
        """
        POST /policy-sets/:id/relationships/workspaces
        """
        url = f"{self._base_url}/{policy_id}/relationships/workspaces"
        return self._delete(url, data=payload)

    def create_policy_set_version(self):
        """
        For versioned policy sets which have no VCS repository attached,
        versions of policy code may be uploaded directly to the API by
        creating a new policy set version and, in a subsequent request,
        uploading a tarball (tar.gz) of data to it.

        POST /policy-sets/:id/versions
        """
        # TODO

    def show_policy_set_version(self, policy_set_id):
        """
        GET /policy-sets/:id
        """
        # TODO
