"""
Module for Terraform Cloud API Endpoint: Subscriptions.
"""

from .endpoint import TFCEndpoint

class TFCSubscriptions(TFCEndpoint):
    """
    `Subscriptions API Docs \
        <https://www.terraform.io/docs/cloud/api/subscriptions.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._subscriptions_base_url = \
            f"{self._api_v2_base_url}/subscriptions"
        self._org_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/subscription"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return True

    def terraform_enterprise_only(self):
        return False

    def show(self):
        """
        ``GET /organizations/:organization_name/subscription``

        `Subscriptions Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/subscriptions.html#show-subscription-for-organization>`_
        """
        return self._get(self._org_base_url)

    def show_by_id(self, sub_id):
        """
        ``GET /subscriptions/:id``

        `Subscriptions Show by ID API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/subscriptions.html#show-subscription-by-id>`_
        """
        url = f"{self._subscriptions_base_url}/{sub_id}"
        return self._get(url)
