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

        # Confirm an event hook was created
        shown_hook = self._api.run_tasks.show_event_hook(created_hook_id)["data"]
        self.assertEqual(shown_hook["attributes"]["name"], hook_name)

        # List the event hooks, check that we get the one we created
        listed_hooks = self._api.run_tasks.list_event_hooks()["data"]
        self.assertEqual(len(listed_hooks), 1)

        # List all the event hooks, check that we get the one we created
        all_hooks = self._api.run_tasks.list_all_event_hooks()["data"]
        self.assertEqual(len(all_hooks), 1)

        updated_hook_name = "new-example"
        update_hook_payload = {
            "data": {
                "type": "event-hooks",
                "attributes": {
                    "name": updated_hook_name
                }
            }
        }
        updated_hook = self._api.run_tasks.update_event_hook(created_hook_id, update_hook_payload)["data"]
        self.assertEqual(updated_hook["attributes"]["name"], updated_hook_name)

        # Attach the event hook as a task to a workspace
        attach_hook_payload = {
            "data": {
                "type": "tasks",
                "attributes": {
                    "enforcement-level": "advisory"
                },
                "relationships": {
                    "event-hook": {
                        "data": {
                            "id": created_hook_id,
                            "type": "event-hooks"
                        }
                    }
                }
            }
        }
        attached_task = \
            self._api.run_tasks.attach_event_hook_as_task(self._ws_id, attach_hook_payload)["data"]
        attached_task_id = attached_task["id"]
        attached_task_hook_id = attached_task["relationships"]["event-hook"]["data"]["id"]
        self.assertEqual(created_hook_id, attached_task_hook_id)

        # List the tasks, confirm we have one
        listed_tasks = self._api.run_tasks.list(self._ws_id)["data"]
        self.assertEqual(len(listed_tasks), 1)

        # Confirm that the hook has been attached by showing the task and comparing IDs
        shown_task = self._api.run_tasks.show(attached_task_id)["data"]
        self.assertEqual(shown_task["id"], attached_task_id)

        # Update the task
        updated_enforcement_level = "mandatory"
        update_task_payload = {
            "data": {
                "type": "tasks",
                "attributes": {
                    "enforcement-level": updated_enforcement_level
                }
            }
        }
        updated_task = self._api.run_tasks.update(attached_task_id, update_task_payload)["data"]
        self.assertEqual(updated_task["attributes"]["enforcement-level"], updated_enforcement_level)

        # Destroy the task, confirm it's gone
        self._api.run_tasks.destroy(attached_task_id)
        listed_tasks = self._api.run_tasks.list(self._ws_id)["data"]
        self.assertEqual(len(listed_tasks), 0)

        # Destroy the hook, confirm it's gone
        self._api.run_tasks.destroy_event_hook(created_hook_id)
        listed_hooks = self._api.run_tasks.list_event_hooks()["data"]
        self.assertEqual(len(listed_hooks), 0)
