"""
Module for Terraform Cloud API Endpoint: Notification Configurations.
"""

from .endpoint import TFCEndpoint

class TFCNotificationConfigurations(TFCEndpoint):
    """
    `API Docs \
        <https://www.terraform.io/docs/cloud/api/notification-configurations.html>`_
    """
    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/notification-configurations"
        self._ws_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/notification-configurations``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#create-a-notification-configuration>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#sample-payload-for-generic-notification-configurations>`_
        """
        url = f"{self._ws_base_url}/{workspace_id}/notification-configurations"
        return self._create(url, payload)

    def list(self, workspace_id):
        """
        ``GET /workspaces/:workspace_id/notification-configurations``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#list-notification-configurations>`_
        """
        url = f"{self._ws_base_url}/{workspace_id}/notification-configurations"
        return self._list(url)

    def show(self, notification_config_id):
        """
        ``GET /notification-configurations/:notification-configuration-id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#show-a-notification-configuration>`_
        """
        url = f"{self._endpoint_base_url}/{notification_config_id}"
        return self._show(url)

    def update(self, notification_config_id, payload):
        """
        ``PATCH /notification-configurations/:notification-configuration-id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#update-a-notification-configuration>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{notification_config_id}"
        return self._update(url, payload)

    def verify(self, notification_config_id):
        """
        ``POST /notification-configurations/:notification-configuration-id/actions/verify``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#verify-a-notification-configuration>`_
        """
        url = f"{self._endpoint_base_url}/{notification_config_id}/actions/verify"
        return self._post(url)

    def destroy(self, notification_config_id):
        """
        ``DELETE /notification-configurations/:notification-configuration-id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/notification-configurations.html#delete-a-notification-configuration>`_
        """
        url = f"{self._endpoint_base_url}/{notification_config_id}"
        return self._destroy(url)
