
"""
Module for Terraform Cloud API Endpoint: Projects.
"""

from .endpoint import TFCEndpoint

class TFCProjects(TFCEndpoint):
    """
    `Projects API Docs \
        <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._projects_api_v2_base_url = f"{self._api_v2_base_url}/projects"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/projects"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return True

    def terraform_enterprise_only(self):
        # FIXME: Once it's released to TFE, remove this
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/projects``

        `Projects Create API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#create-a-project>`_

        `Create Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def destroy(self, project_id):
        """
        ``DELETE /projects/:project_id``

        `Projects Destroy API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#delete-a-project>`_
        """
        url = f"{self._projects_api_v2_base_url}/{project_id}"
        return self._destroy(url)

    def list(self, page=None, page_size=None, filters=None, query=None):
        """
        ``GET /organizations/:organization_name/projects``

        `Projects List API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#list-projects>`_

        `Query Parameter(s) Details \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#query-parameters>`__
        """
        return self._list(\
            self._org_api_v2_base_url, page=page, page_size=page_size, filters=filters, query=query)

    def list_all(self, filters=None, query=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every run for a workspace.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_api_v2_base_url, filters=filters, query=query)

    def show(self, project_id):
        """
        ``GET /projects/:project_id``

        `Projects Show API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#show-project>`_
        """
        url = f"{self._projects_api_v2_base_url}/{project_id}"
        return self._show(url)

    def update(self, project_id, payload):
        """
        ``PATCH /projects/:project_id``

        `Projects Update API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#update-a-project>`_

        `Update Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#sample-payload-1>`_
        """
        url = f"{self._projects_api_v2_base_url}/{project_id}"
        return self._update(url, payload)
