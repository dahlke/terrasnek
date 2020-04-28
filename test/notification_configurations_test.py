"""
Module for testing the Terraform Cloud API Endpoint: Notification Configurations.
"""

from .base import TestTFCBaseTestCase

import time


class TestTFCNotificationConfigurations(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Notification
    Configurations.
    """

    def setUp(self):
        unittest_name = "not-cng"

        # Create an OAuth client for the test and extract it's ID
        oauth_client_payload = self._get_oauth_client_create_payload(unittest_name)
        oauth_client = self._api.oauth_clients.create(oauth_client_payload)
        self._oauth_client_id = oauth_client["data"]["id"]

        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]
        ws_payload = self._get_ws_with_vcs_create_payload(unittest_name, oauth_token_id)
        workspace = self._api.workspaces.create(ws_payload)["data"]
        self._ws_id = workspace["id"]

        # Allow some time for the workspace to be created
        time.sleep(3)

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_notifications_configuration_lifecycle(self):
        """
        Test the Notification Configurations API endpoints: create, lst, show,
        update, verify, destroy.
        """

        # Show that there are no configuration notifications for the workspace
        noti_config_resp = self._api.notification_configurations.lst(self._ws_id)
        noti_configs = noti_config_resp["data"]
        self.assertEqual(len(noti_configs), 0)

        # Add one notification configuration
        payload = self._get_notification_configuration_create_payload()
        create_resp = self._api.notification_configurations.create(self._ws_id, payload)
        created_noti_config = create_resp["data"]
        created_noti_config_id = created_noti_config["id"]

        # Check that there is now one notification configuration added
        noti_config_resp = self._api.notification_configurations.lst(self._ws_id)
        noti_configs = noti_config_resp["data"]
        self.assertEqual(len(noti_configs), 1)

        # Show the notification configuration we just created, compare the IDs
        shown_resp = self._api.notification_configurations.show(created_noti_config_id)
        shown_noti_config = shown_resp["data"]
        shown_noti_config_id = shown_noti_config["id"]
        self.assertEqual(shown_noti_config_id, created_noti_config_id)

        # Update the  name of the notification configuration, and check that it worked
        name_to_update_to = "foobar"
        update_payload = {
            "data": {
                "id": created_noti_config_id,
                "type": "notification-configurations",
                "attributes": {
                    "name": name_to_update_to
                }
            }
        }
        update_resp = self._api.notification_configurations.update(created_noti_config_id, update_payload)
        updated_noti_config = update_resp["data"]
        updated_noti_name = updated_noti_config["attributes"]["name"]
        self.assertEqual(updated_noti_name, name_to_update_to)

        # Check that we can verify the notification configuration endpoint
        verify_resp = self._api.notification_configurations.verify(created_noti_config_id)
        verified_noti_config = verify_resp["data"]
        verified_noti_config_name = verified_noti_config["attributes"]["name"]
        self.assertEqual(name_to_update_to, verified_noti_config_name)

        # Destroy the notification configuraiton, and show the workspace has zero again
        self._api.notification_configurations.destroy(created_noti_config_id)
        noti_config_resp = self._api.notification_configurations.lst(self._ws_id)
        noti_configs = noti_config_resp["data"]
        self.assertEqual(len(noti_configs), 0)
