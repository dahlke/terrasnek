"""
Module for testing the Terraform Cloud API Endpoint: Notification Configurations.
"""

from .base import TestTFCBaseTestCase


class TestTFCNotificationConfigurations(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Notification
    Configurations.
    """

    _unittest_name = "not-cng"
    _endpoint_being_tested = "notification_configs"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = oauth_client["data"]["id"]
        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id)
        workspace = self._api.workspaces.create(ws_payload)["data"]
        self._ws_id = workspace["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_notifications_configurations(self):
        """
        Test the Notification Configurations API endpoints.
        """

        # Show that there are no configuration notifications for the workspace
        all_noti_configs = self._api.notification_configs.list(self._ws_id)["data"]
        self.assertEqual(len(all_noti_configs), 0)

        # Add one notification configuration
        not_cnf_name = self._unittest_random_name()
        payload = {
            "data": {
                "type": "notification-configurations",
                "attributes": {
                    "destination-type": "generic",
                    "enabled": True,
                    "name": not_cnf_name,
                    "url": "https://httpstat.us/200",
                    "triggers": [
                        "run:applying"
                    ]
                }
            }
        }
        created_noti_config = self._api.notification_configs.create(self._ws_id, payload)["data"]
        created_noti_config_id = created_noti_config["id"]

        # Check that the notification config we added is now there
        all_noti_configs = self._api.notification_configs.list(self._ws_id)["data"]
        found_noti_conf = False
        for noti_conf in all_noti_configs:
            if noti_conf["id"] == created_noti_config_id:
                found_noti_conf = True
                break
        self.assertTrue(found_noti_conf)

        # Show the notification configuration we just created, compare the IDs
        shown_noti_config = self._api.notification_configs.show(created_noti_config_id)["data"]
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
        updated_noti_config = \
            self._api.notification_configs.update(created_noti_config_id, update_payload)["data"]
        updated_noti_name = updated_noti_config["attributes"]["name"]
        self.assertEqual(updated_noti_name, name_to_update_to)

        # Check that we can verify the notification configuration endpoint
        verified_noti_config = self._api.notification_configs.verify(created_noti_config_id)["data"]
        verified_noti_config_name = verified_noti_config["attributes"]["name"]
        self.assertEqual(name_to_update_to, verified_noti_config_name)

        # Destroy the notification configuraiton, and show the workspace has zero again
        self._api.notification_configs.destroy(created_noti_config_id)
        all_noti_configs = self._api.notification_configs.list(self._ws_id)["data"]
        found_noti_conf = False
        for noti_conf in all_noti_configs:
            if noti_conf["id"] == created_noti_config_id:
                found_noti_conf = True
                break
        self.assertFalse(found_noti_conf)
