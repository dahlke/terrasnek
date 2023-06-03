"""
Module for Terraform Cloud API Endpoint: Project Team Access.
"""

from .endpoint import TFCEndpoint

class TFCProjectTeamAccess(TFCEndpoint):
    """
    `Project Team Access API Docs \
        <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/team-projects"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def add_project_team_access(self, payload):
        """
        ``POST /team-projects``

        `Project Team Access Add API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#add-team-access-to-a-projectk>`_

        `Add Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#sample-payload>`_
        """
        return self._post(self._endpoint_base_url, data=payload)

    def list(self, filters=None):
        """
        ``GET /team-projects``

        `Project Team Access List API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#list-team-access-to-a-project>`_

        Query Parameter(s) Details \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#query-parameters>`__
        """
        return self._list(self._endpoint_base_url, filters=filters)

    def remove_project_team_access(self, access_id):
        """
        ``DELETE /team-projects/:id``

        `Project Team Access Remove API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#remove-team-access-from-a-project>`_
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._destroy(url)

    def show(self, access_id):
        """
        ``GET /team-projects/:id``

        `Project Team Access Show API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#show-a-team-access-relationship>`_
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._show(url)

    def update(self, access_id, payload):
        """
        ``PATCH /team-projects/:id``

        `Project Team Access Update API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#update-team-access-to-a-project>`_

        `Update Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/project-team-access#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{access_id}"
        return self._update(url, payload)
