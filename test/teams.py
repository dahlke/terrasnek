import unittest
import os
from .base import TestTFEBaseTestCase

from terrasnek.api import TFE

class TestTFETeams(TestTFEBaseTestCase):

    def test_team_lifecycle(self):
        teams = self._api.teams.ls()["data"]
        self.assertEqual(len(teams), 1)

        new_team = self._api.teams.create(self._team_create_payload)["data"]
        new_team_id = new_team["id"]
        self.assertEqual(new_team["attributes"]["name"], self._test_team_name)

        shown_team = self._api.teams.show(new_team_id)["data"]
        self.assertEqual(shown_team["attributes"]["name"], self._test_team_name)

        self._api.teams.destroy(new_team_id)
        teams = self._api.teams.ls()["data"]
        self.assertEqual(len(teams), 1)
    
    def test_team_memberships(self):
        team_id = self._api.teams.create(self._team_create_payload)["data"]["id"]
        membership_payload = {
            "data": [
                {
                    "type": "users",
                    "id": self._test_username
                }
            ]
        }

        self._api.team_memberships.add_a_user_to_team(team_id, membership_payload)
        shown_team = self._api.teams.show(team_id)["data"]
        self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 1)

        self._api.team_memberships.delete_a_user_from_team(team_id, membership_payload)
        shown_team = self._api.teams.show(team_id)["data"]
        self._api.teams.destroy(team_id)
        self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 0)


    def test_team_access(self):
        # Create a test workspace
        ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        ws_id = ws["data"]["id"]

        # Create a test team
        team_id = self._api.teams.create(self._team_create_payload)["data"]["id"]

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
                            "id": ws_id
                        }
                    },
                    "team": {
                        "data": {
                            "type": "teams",
                            "id": team_id
                        }
                    }
                }
            }
        }
        workspace_accesses = self._api.team_access.ls()
        self.assertNotEqual(len(workspace_accesses["data"]), 0)

        access = self._api.team_access.add_team_access(team_access_create_payload)
        access_id = access["data"]["id"]
        shown_access = self._api.team_access.show(access_id)
        self.assertEqual(shown_access["data"]["id"], access_id)

        self._api.team_access.remove_team_access(access_id)
        shown_access = self._api.team_access.show(access_id)
        self.assertEqual(shown_access, None)

        # Delete the test workspace
        self._api.workspaces.destroy(workspace_name=ws["data"]["attributes"]["name"])

        # Delete the test team
        self._api.teams.destroy(team_id)

    def test_team_tokens(self):
        # TODO
        pass