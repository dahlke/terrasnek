"""
Module for Terraform Cloud API Endpoint: Policy Sets.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicySets(TFCEndpoint):
    """
    `Policy Sets API Docs \
        <https://www.terraform.io/docs/cloud/api/policy-sets.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policy-sets"
        self._pol_set_version_api_v2_base_url = f"{self._api_v2_base_url}/policy-set-versions"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/policy-sets"

    def required_entitlements(self):
        # NOTE: Entitlements.SENTINEL has been deprecated, using Policy Enforcement instead.
        return [Entitlements.POLICY_ENFORCEMENT]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/policy-sets``

        `Policy Sets Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#create-a-policy-set>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self, filters=None, include=None, page=None, page_size=None, search=None):
        """
        ``GET /organizations/:organization_name/policy-sets``

        `Policy Sets List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#list-policy-sets>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#query-parameters>`__
        """
        return self._list(\
            self._org_api_v2_base_url, \
            filters=filters, include=include, \
            page=page, page_size=page_size, search=search)

    def list_all(self, search=None, filters=None, include=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every policy set for an organization.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_api_v2_base_url, include=include, \
            search=search, filters=filters)

    def show(self, policy_set_id, include=None):
        """
        ``GET /policy-sets/:id``

        `Policy Sets Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#show-a-policy-set>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._show(url, include=include)

    def update(self, policy_set_id, payload):
        """
        ``PATCH /policy-sets/:id``

        `Policy Sets Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#update-a-policy-set>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._update(url, payload)

    def destroy(self, policy_set_id):
        """
        ``DELETE /policies/:policy_set_id``

        `Policy Sets Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#delete-a-policy-set>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}"
        return self._destroy(url)

    def add_policies_to_set(self, policy_set_id, payload):
        """
        ``POST /policy-sets/:id/relationships/policies``

        `Policy Sets Add Policies to Set API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#add-policies-to-the-policy-set>`_

        `Add Policies to Set Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-2>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/relationships/policies"
        return self._post(url, data=payload)

    def attach_policy_set_to_workspaces(self, policy_id, payload):
        """
        ``POST /policy-sets/:id/relationships/workspaces``

        `Policy Sets Attach Set to Workspaces API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#attach-a-policy-set-to-workspaces>`_

        `Attach Policy Set to Workspaces Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-3>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/workspaces"
        return self._post(url, data=payload)

    def remove_policies_from_set(self, policy_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/policies``

        `Policy Sets Remove Policies from Set API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#remove-policies-from-the-policy-set>`_

        `Remove Policies from Set Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-4>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/policies"
        return self._destroy(url, data=payload)

    def detach_policy_set_from_workspaces(self, policy_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/workspaces``

        `Policy Sets Detach Set from Workspaces API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#detach-the-policy-set-from-workspaces>`_

        `Detach Policy Set from Workspaces Sample Payload \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#sample-payload-5>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/workspaces"
        return self._destroy(url, data=payload)

    def create_policy_set_version(self, policy_set_id):
        """
        ``POST /policy-sets/:id/versions``

        `Policy Sets Create Set Version API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#create-a-policy-set-version>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/versions"
        return self._post(url)

    def show_policy_set_version(self, policy_set_version_id):
        """
        ``GET /policy-set-versions/:id``

        `Policy Sets Show Policy Set Version API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#show-a-policy-set-version>`_
        """
        url = f"{self._pol_set_version_api_v2_base_url}/{policy_set_version_id}"
        return self._get(url)

    def upload(self, path_to_tarball, policy_set_version_id):
        """
        ``PUT {derived_policy_set_upload_url}``
        ``PUT https://archivist.terraform.io/v1/object/<UNIQUE OBJECT ID>``

        `Policy Sets Upload API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-sets.html#upload-policy-set-versions>`_
        """
        url = self.show_policy_set_version(policy_set_version_id)["data"]["links"]["upload"]
        data = None
        with open(path_to_tarball, 'rb') as data_bytes:
            data = data_bytes.read()

        return self._put(url, data=data)

    def exclude_workspaces(self, policy_set_id, payload):
        """
        ``POST /policy-sets/:id/relationships/workspace-exclusions``

        `Policy Sets Exclude Workspace API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#exclude-a-workspace-from-a-policy-set>`_

        `Policy Sets Exclude Workspace Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#sample-payload-5>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/relationships/workspace-exclusions"
        return self._post(url, data=payload)

    def reinclude_workspaces(self, policy_set_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/workspace-exclusions``

        `Policy Sets Re-Include Workspace API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#reinclude-a-workspace-to-a-policy-set>`_

        `Policy Sets Re-Include Workspace Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#reinclude-a-workspace-to-a-policy-set>`_
        """
        url = f"{self._endpoint_base_url}/{policy_set_id}/relationships/workspace-exclusions"
        return self._destroy(url, data=payload)

    def attach_policy_set_to_projects(self, policy_id, payload):
        """
        ``POST /policy-sets/:id/relationships/projects``

        `Policy Sets Attach Set to Projects API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#attach-a-policy-set-to-projects>`_

        `Attach Policy Set to Projects Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#sample-payload-3>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/projects"
        return self._post(url, data=payload)

    def detach_policy_set_from_projects(self, policy_id, payload):
        """
        ``DELETE /policy-sets/:id/relationships/projects``

        `Policy Sets Detach Set from Projects API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#detach-a-policy-set-from-projects>`_

        `Detach Policy Set from Projects Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-sets#sample-payload-7>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/relationships/projects"
        return self._destroy(url, data=payload)
