"""
Module for Terraform Cloud API Endpoint: Run Tasks Integration.
"""

from .endpoint import TFCEndpoint

class TFCRunTasksIntegration(TFCEndpoint):
    """
    `Run Tasks Integration API Docs \
        <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration>`_
    """

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def request(self, url):
        """
        ``POST :url``

        `Run Task Integration Request API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#run-task-request>`_

        `Request Sample Payload \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#sample-payload>`_
        """
        return self._post(url)

    def callback(self, callback_url):
        """
        ``PATCH :callback_url``

        `Run Task Integration Callback API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#run-task-callback>`_

        `Callback Sample Payload \
            <https://www.terraform.io/cloud-docs/api-docs/run-tasks-integration#request-body-1>`_
        """
        return self._patch(callback_url)
