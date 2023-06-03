"""
Module for Terraform Cloud API Endpoint: GitHub Apps.
"""

from .endpoint import TFCEndpoint

class TFCGitHubApps(TFCEndpoint):
    """
    `GitHub Apps API Docs \
        <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/github-app-installations>`_
    """

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def list(self, filters=None):
        """
        ``GET /github-app/installations``

        `GitHub Apps List API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/github-app-installations#list-installations>`_
        """
        url = f"{self._api_v2_base_url}/github-app/installations"
        return self._list(url, filters=filters)

    def show(self, app_install_id):
        """
        ``GET /github-app/installation/:gh_app_installation_id``

        `GitHub Apps Show API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/github-app-installations#show-installation>`_
        """
        url = f"{self._api_v2_base_url}/github-app/installation/{app_install_id}"
        return self._list(url)
