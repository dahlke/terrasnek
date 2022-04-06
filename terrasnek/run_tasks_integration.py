"""
Module for Terraform Cloud API Endpoint: Run Tasks Integration.
"""

from .endpoint import TFCEndpoint

class TFCRunTasksIntegration(TFCEndpoint):
    """
    `Run Tasks Integration API Docs \
        <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return True

    def terraform_enterprise_only(self):
        return False

    def request(self, run_id, payload):
        """
        ``POST :url``

        `Run Task Integration Request API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#run-task-request>`_

        `Request Sample Payload \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#sample-payload>`_
        """
        url = f"{self._runs_base_url}/{run_id}/comments"
        return self._create(url, payload=payload)

    def callback(self, comment_id):
        """
        ``PATCH :callback_url``

        `Run Task Integration Callback API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#run-task-callback>`_

        `Callback Sample Payload \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#request-body-1>`_
        """
        url = f"{self._endpoint_base_url}/{comment_id}"
        return self._show(url)