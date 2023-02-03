"""
Module for testing the Terraform Cloud API Endpoint: Project Team Access.
"""

from .base import TestTFCBaseTestCase


class TestTFCProjectTeamAccess(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Project Team Access.
    """

    _unittest_name = "team-acc"
    _endpoint_being_tested = "team_access"

    def setUp(self):
        # Create a test team
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]

        self._project = self._api.projects.create(
            self._get_project_create_payload())["data"]
        self._project_id = self._project["id"]

        # Invite a test user to this org, will be removed after
        invite = self._api.org_memberships.invite(self._get_org_membership_invite_payload())
        self._org_membership_id = invite["data"]["id"]

        # Create a test workspace
        workspace = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())["data"]
        self._ws_id = workspace["id"]
        self._ws_name = workspace["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_name)
        self._api.teams.destroy(self._team_id)
        self._api.projects.destroy(self._project_id)
        self._api.org_memberships.remove(self._org_membership_id)

    def test_project_team_access(self):
        """
        Test the Team Access API endpoints.
        """
        listed_proj_filters = [
            {
                "keys": ["project", "id"],
                "value": self._project_id
            }
        ]
        listed_proj_access = self._api.project_team_access.list(filters=listed_proj_filters)
        self.assertEqual(len(listed_proj_access["data"]), 0)

        # Create new project team access, confirm it has been created
        proj_team_access_payload = {
            "data": {
                "attributes": {
                    "access": "read"
                },
                "relationships": {
                    "project": {
                        "data": {
                            "type": "projects",
                            "id": self._project_id
                        }
                    },
                    "team": {
                        "data": {
                            "type": "teams",
                            "id": self._team_id
                        }
                    }
                },
                "type": "team-projects"
            }
        }
        proj_team_access = self._api.project_team_access.add_project_team_access(
            proj_team_access_payload)
        proj_team_access_id = proj_team_access["data"]["id"]

        # Show the newly created project team access, confirm the ID matches to the created one
        shown_proj_team_access = self._api.project_team_access.show(proj_team_access_id)
        self.assertEqual(shown_proj_team_access["data"]["id"], proj_team_access_id)

        # Update team access
        update_proj_team_access_payload = {
            "data": {
                "id": proj_team_access_id,
                "attributes": {
                    "access": "admin"
                }
            }
        }
        updated_proj_team_access = \
            self._api.project_team_access.update(proj_team_access_id, update_proj_team_access_payload)["data"]
        self.assertEqual(updated_proj_team_access["attributes"]["access"], "admin")

        # Remove the team access, confirm it's gone
        self._api.project_team_access.remove_project_team_access(proj_team_access_id)
        listed_proj_access = self._api.project_team_access.list(filters=listed_proj_filters)
        self.assertEqual(len(listed_proj_access["data"]), 0)
