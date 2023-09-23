"""
Module for testing the Terraform Cloud API Endpoint: Projects.
"""

from .base import TestTFCBaseTestCase


class TestTFCProjects(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Projects.
    """

    _unittest_name = "projs"
    _endpoint_being_tested = "projects"

    def test_projects(self):
        """
        Test the Projects API endpoints.
        """

        # List all the projects, confirm that the response type
        projects = self._api.projects.list()["data"]
        self.assertEqual("projects", projects[0]["type"])

        # Create a new project, confirm that it has been created
        new_project = self._api.projects.create(
            self._get_project_create_payload())["data"]
        new_project_id = new_project["id"]
        new_project_name = new_project["attributes"]["name"]

        # Confirm we have the default project and the newly created one
        some_projects_raw = self._api.projects.list()["data"]
        self.assertEqual("Default Project", some_projects_raw[0]["attributes"]["name"])
        self.assertEqual(new_project_id, some_projects_raw[-1]["id"])

        # Show the newly created project
        shown_project = self._api.projects.show(new_project_id)["data"]
        self.assertEqual(new_project_id, shown_project["id"])

        # TODO: test the filters param once permissions API is in place for terrasnek
        all_projects_raw = self._api.projects.list()["data"]
        self.assertEqual("Default Project", all_projects_raw[0]["attributes"]["name"])
        self.assertEqual(new_project_id, all_projects_raw[-1]["id"])

        # Update the project to have VCS management access, confirm the changes took effect.
        new_project_name = self._random_name(ran_str_len=4)
        update_payload = {
            "data": {
                "type": "projects",
                "attributes": {
                    "name": new_project_name
                }
            }
        }
        updated_project = self._api.projects.update(new_project_id, update_payload)["data"]
        self.assertEqual(new_project_name, updated_project["attributes"]["name"])


        # Set up a workspace to move, then move it and confirm it works
        workspace = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]
        ws_id = workspace["id"]
        move_workspace_payload = {
            "data": [
                {
                    "type": "workspaces",
                    "id": ws_id
                }
            ]
        }
        moved_workspace = self._api.projects.move_workspaces_into_project(new_project_id, move_workspace_payload)
        self.assertIsNone(moved_workspace)

        # Delete the workspace that was created so the project can be destroyed
        self._api.workspaces.destroy(workspace_id=ws_id)

        # Destroy the project, confirm it's gone
        self._api.projects.destroy(new_project_id)
        some_projects = self._api.projects.list()["data"]
        found_project = False
        for project in some_projects:
            if project["id"] == new_project_id:
                found_project = True
                break
        self.assertFalse(found_project)
