"""
Module for Terraform Cloud API Endpoint: Variable Sets.
"""

from .endpoint import TFCEndpoint


class TFCVarSets(TFCEndpoint):
    """
    `Variable Sets API Docs \
        <https://www.terraform.io/docs/cloud/api/variable-sets.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_varsets_base_url = f"{self._api_v2_base_url}/organizations/{self._org_name}/varsets"
        self._endpoint_base_url = f"{self._api_v2_base_url}/varsets"
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST organizations/:organization_name/varsets``

        `Variable Sets Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#create-a-variable-set>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#sample-payload>`_
        """
        return self._create(self._org_varsets_base_url, payload)

    def show(self, varset_id):
        """
        ``GET varsets/:varset_id``

        `Variable Sets Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#show-variable-set>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}"
        return self._show(url)

    def list_for_org(self):
        """
        ``GET organizations/:organization_name/varsets``

        `Variable Sets List For Organization API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#list-variable-set>`_
        """
        return self._list(self._org_varsets_base_url)

    def list_all_for_org(self):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every workspace in an organization.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_varsets_base_url)

    def list_for_workspace(self, workspace_id):
        """
        ``GET workspaces/:workspace_id/varsets``

        `Variable Sets List For Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#list-variable-set>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/varsets"
        return self._list(url)

    def list_all_for_workspace(self, workspace_id):
        """
        ``GET workspaces/:workspace_id/varsets``

        `Variable Sets List For Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#list-variable-set>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/varsets"
        return self._list_all(url)

    def update(self, varset_id, payload):
        """
        ``PUT/PATCH varsets/:varset_id``

        `Variable Sets Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#update-a-variable-set>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}"
        return self._update(url, payload)

    def destroy(self, varset_id):
        """
        ``DELETE varsets/:varset_id``

        `Variable Sets Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#delete-a-variable-set>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}"
        return self._destroy(url)

    # VARIABLE RELATIONSHIPS
    def add_var_to_varset(self, varset_id, payload):
        """
        ``POST varsets/:varset_external_id/relationships/vars``

        `Variable Sets Add Variable API Doc Reference \
            <POST varsets/:varset_external_id/relationships/vars>`_

        `Add Variable To Variable Set Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#sample-payload-2>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/vars"
        return self._post(url, data=payload)

    def update_var_in_varset(self, varset_id, var_id, payload):
        """
        ``PATCH varsets/:varset_id/relationships/vars/:var_id``

        `Variable Sets Update Variable API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#update-a-variable-in-a-variable-set>`_

        `Update Variable In Variable Set Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#sample-payload-3>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/vars/{var_id}"
        return self._update(url, payload)

    def delete_var_from_varset(self, varset_id, var_id):
        """
        ``DELETE varsets/:varset_id/relationships/vars/:var_id``

        `Variable Sets Delete Variable API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#delete-a-variable-in-a-variable-set>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/vars/{var_id}"
        return self._destroy(url)

    def list_vars_in_varset(self, varset_id):
        """
        ``GET varsets/:varset_id/relationships/vars``

        `Variable Sets List In Variable Set API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#list-variables-in-a-variable-set>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/vars"
        return self._list(url)

    # WORKSPACE RELATIONSHIPS
    def apply_varset_to_workspace(self, varset_id, payload):
        """
        ``POST varsets/:varset_id/relationships/workspaces``

        `Variable Sets Apply To Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#apply-variable-set-to-workspaces>`_

        `Apply Variable Set to Workspace Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#sample-payload-4>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/workspaces"
        return self._post(url, data=payload)

    def remove_varset_from_workspace(self, varset_id, payload):
        """
        ``DELETE varsets/:varset_id/relationships/workspaces``

        `Variable Sets Remove From Workspace API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#remove-a-variable-set-from-workspaces>`_

        `Remove Variable Set From Workspace Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variable-sets.html#sample-payload-5>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/workspaces"
        self._destroy(url, data=payload)


    # PROJECT RELATIONSHIPS
    def apply_varset_to_project(self, varset_id, payload):
        """
        ``POST varsets/:varset_id/relationships/projects``

        `Variable Sets Apply To Project API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets#apply-variable-set-to-projects>`_

        `Apply Variable Set to Project Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets#sample-payload-6>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/projects"
        return self._post(url, data=payload)

    def remove_varset_from_project(self, varset_id, payload):
        """
        ``DELETE varsets/:varset_id/relationships/projects``

        `Variable Sets Remove From Project API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets#remove-a-variable-set-from-projects>`_

        `Remove Variable Set From Project Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets#sample-payload-7>`_
        """
        url = f"{self._endpoint_base_url}/{varset_id}/relationships/projects"
        self._destroy(url, data=payload)
