"""
Module for Terraform Cloud API Endpoint: Comments.
"""

from .endpoint import TFCEndpoint

class TFCComments(TFCEndpoint):
    """
    `Comments API Docs \
        <https://www.terraform.io/cloud-docs/api-docs/comments>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/comments"
        self._runs_base_url = f"{self._api_v2_base_url}/runs"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def list_for_run(self, run_id):
        """
        ``GET /runs/:id/comments``

        `Comments List for Run API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/comments#list-comments-for-a-run>`_
        """
        url = f"{self._runs_base_url}/{run_id}/comments"
        return self._list(url)

    def show(self, comment_id):
        """
        ``GET /comments/:id``

        `Comments Show API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/comments#show-a-comment>`_
        """
        url = f"{self._endpoint_base_url}/{comment_id}"
        return self._show(url)

    def create_for_run(self, run_id, payload):
        """
        ``POST /runs/:id/comments``

        `Comments Create for Run API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/comments#create-comment>`_

        `Create Sample Payload \
            <https://www.terraform.io/cloud-docs/api-docs/comments#sample-payload>`_
        """
        url = f"{self._runs_base_url}/{run_id}/comments"
        return self._create(url, payload=payload)
