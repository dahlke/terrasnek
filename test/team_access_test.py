"""
Module for testing the Terraform Cloud API Endpoint: Team Access.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeamAccess(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Access.
    """

    def setUp(self):
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]

        # Create a test workspace
        workspace = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("team-access"))["data"]
        self._ws_id = workspace["id"]
        self._ws_name = workspace["attributes"]["name"]
        # Create a test team

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_name)
        self._api.teams.destroy(self._team_id)

    def test_team_access(self):
        """
        Test the Team Access API endpoints: list, add, remove.
        """

        team_access_create_payload = {
            "data": {
                "type": "team-workspaces",
                "attributes": {
                    "access": "admin"
                },
                "relationships": {
                    "workspace": {
                        "data": {
                            "type": "workspaces",
                            "id": self._ws_id
                        }
                    },
                    "team": {
                        "data": {
                            "type": "teams",
                            "id": self._team_id
                        }
                    }
                }
            }
        }
        workspace_accesses = self._api.team_access.lst()["data"]
        self.assertNotEqual(len(workspace_accesses), 0)

        access = self._api.team_access.add_team_access(
            team_access_create_payload)
        access_id = access["data"]["id"]
        shown_access = self._api.team_access.show(access_id)
        self.assertEqual(shown_access["data"]["id"], access_id)

        len_after_adding = len(self._api.team_access.lst()["data"])
        self._api.team_access.remove_team_access(access_id)
        len_after_removing = self._api.team_access.lst()["data"]
        self.assertNotEqual(len_after_adding, len_after_removing)
