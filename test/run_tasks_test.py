"""
Module for testing the Terraform Cloud API Endpoint: Run Tasks.
"""

from .base import TestTFCBaseTestCase


class TestTFCRunTasks(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Run Tasks.
    """

    _unittest_name = "run-task"
    _endpoint_being_tested = "run_tasks"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_name)

    def test_run_tasks(self):
        """
        Test the Run Tasks API endpoints.
        """

        # TODO: delete hooks that were created

        # List the event hooks, check that there are none
        hooks = self._api.run_tasks.list_event_hooks(self._ws_id)["data"]
        self.assertEqual(len(hooks), 0)

        # Create an event hook
        hook_name = "example"
        create_hook_payload = {
            "data": {
                "type": "event-hooks",
                "attributes": {
                    "name": hook_name,
                    "url": "http://example.com",
                    "hmac_key": "secret",
                    "category": "task"
                }
            }
        }
        created_hook = self._api.run_tasks.create_event_hook(create_hook_payload)["data"]
        created_hook_id = created_hook["id"]
        self.assertEqual(created_hook["attributes"]["name"], hook_name)

        # Confirm we created the event hook
        shown_hook = self._api.run_tasks.show_event_hook(created_hook_id)["data"]
        self.assertEqual(shown_hook["attributes"]["name"], hook_name)

        # List all the event hooks, check that we get the one we created
        all_hooks = self._api.run_tasks.list_all_event_hooks()["data"]
        self.assertEqual(len(all_hooks), 1)

        # Delete the hook we created
        self._api.run_tasks.destroy_event_hook(created_hook_id)

        # Confirm there are no hooks left
        hooks = self._api.run_tasks.list_event_hooks(self._ws_id)["data"]
        self.assertEqual(len(hooks), 0)