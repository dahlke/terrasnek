"""
Module for Terraform Cloud API Endpoint: Notification Configurations.
"""

import requests
import json

from .endpoint import TFCEndpoint


class TFCNotificationConfigurations(TFCEndpoint):
    """
        Terraform Cloud can be configured to send notifications for run state
        transitions. The configuration allows you to specify a destination URL,
        request type, and what events will trigger the notification. Each workspace
        can have up to 20 notification configurations, and they apply to all runs
        for that workspace.

        https://www.terraform.io/docs/cloud/api/notification-configurations.html
    """
    def __init__(self, base_url, organization_name, headers, verify):
        super().__init__(base_url, organization_name, headers, verify)
        self._base_url = f"{base_url}/notification-configurations"
        self._ws_base_url = f"{base_url}/workspaces"

    def create(self, workspace_id, payload):
        """
        POST /workspaces/:workspace_id/notification-configurations
        """
        url = f"{self._ws_base_url}/{workspace_id}/notification-configurations"
        return self._create(url, payload)

    def lst(self, workspace_id):
        """
        GET /workspaces/:workspace_id/notification-configurations
        """
        url = f"{self._ws_base_url}/{workspace_id}/notification-configurations"
        return self._ls(url)

    def show(self, notification_configuration_id):
        """
        GET /notification-configurations/:notification-configuration-id
        """
        url = f"{self._base_url}/{notification_configuration_id}"
        return self._show(url)

    def update(self, notification_configuration_id, payload):
        """
        PATCH /notification-configurations/:notification-configuration-id
        """
        url = f"{self._base_url}/{notification_configuration_id}"
        return self._update(url, payload)

    def verify(self, notification_configuration_id):
        """
        POST /notification-configurations/:notification-configuration-id/actions/verify
        """
        url = f"{self._base_url}/{notification_configuration_id}/actions/verify"
        return self._post(url)

    def destroy(self, notification_configuration_id):
        """
        DELETE /notification-configurations/:notification-configuration-id
        """
        url = f"{self._base_url}/{notification_configuration_id}"
        return self._destroy(url)
