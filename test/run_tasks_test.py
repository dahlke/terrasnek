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
        # List the run tasks, check that there are none
        tasks = self._api.run_tasks.list(self._ws_id)["data"]
        self.assertEqual(len(tasks), 0)

        # Create a run task
        task_name = "example"
        create_task_payload = {
            "data": {
                "type": "tasks",
                "attributes": {
                    "name": task_name,
                    "url": "http://example.com",
                    "hmac_key": "secret",
                    "category": "task"
                }
            }
        }
        created_task = self._api.run_tasks.create(create_task_payload)["data"]
        created_task_id = created_task["id"]
        self.assertEqual(created_task["attributes"]["name"], task_name)

        # Confirm a run task was created
        shown_task = self._api.run_tasks.show(created_task_id)["data"]
        self.assertEqual(shown_task["attributes"]["name"], task_name)

        # List the run tasks, check that we get the one we created
        listed_tasks = self._api.run_tasks.list()["data"]
        self.assertEqual(len(listed_tasks), 1)

        # List all the run tasks, check that we get the one we created
        all_tasks = self._api.run_tasks.list_all()["data"]
        self.assertEqual(len(all_tasks), 1)

        updated_task_name = "new-example"
        update_task_payload = {
            "data": {
                "type": "tasks",
                "attributes": {
                    "name": updated_task_name
                }
            }
        }
        updated_task = self._api.run_tasks.update(created_task_id, update_task_payload)["data"]
        self.assertEqual(updated_task["attributes"]["name"], updated_task_name)

        # Attach the run task to a workspace
        attach_task_payload = {
            "data": {
                "type": "tasks",
                "attributes": {
                    "enforcement-level": "advisory"
                },
                "relationships": {
                    "task": {
                        "data": {
                            "id": created_task_id,
                            "type": "tasks"
                        }
                    }
                }
            }
        }
        attached_task = \
            self._api.run_tasks.attach_task_to_workspace(self._ws_id, attach_task_payload)["data"]
        attached_related_task_id = attached_task["relationships"]["task"]["data"]["id"]
        attached_task_id = attached_task["id"]
        self.assertEqual(created_task_id, attached_related_task_id)

        # List the tasks, confirm we have one
        listed_tasks_on_workspace = self._api.run_tasks.list_tasks_on_workspace(self._ws_id)["data"]
        self.assertEqual(len(listed_tasks_on_workspace), 1)

        # Test listing all on workspace
        all_listed_tasks_on_workspace = self._api.run_tasks.list_all_tasks_on_workspace(self._ws_id)["data"]
        self.assertEqual(len(all_listed_tasks_on_workspace), 1)

        # Confirm that the run task has been attached by showing the task and comparing IDs
        shown_task_on_workspace = self._api.run_tasks.show_task_on_workspace(self._ws_id, attached_task_id)["data"]
        self.assertEqual(shown_task_on_workspace["id"], attached_task_id)

        # Update the task on the workspace
        updated_enforcement_level = "mandatory"
        update_task_on_workspace_payload = {
            "data": {
                "type": "workspace-tasks",
                "attributes": {
                    "enforcement-level": updated_enforcement_level
                }
            }
        }
        updated_task_on_workspace = \
            self._api.run_tasks.update_task_on_workspace(\
                self._ws_id, attached_task_id, update_task_on_workspace_payload)["data"]
        self.assertEqual(updated_task_on_workspace["attributes"]["enforcement-level"], updated_enforcement_level)

        # Remove the task from the workspace, confirm it's gone
        self._api.run_tasks.remove_task_from_workspace(self._ws_id, attached_task_id)
        listed_tasks_on_workspace = self._api.run_tasks.list_tasks_on_workspace(self._ws_id)["data"]
        self.assertEqual(len(listed_tasks_on_workspace), 0)

        # Destroy the run task, confirm it's gone
        self._api.run_tasks.destroy(created_task_id)
        listed_tasks = self._api.run_tasks.list()["data"]
        self.assertEqual(len(listed_tasks), 0)
