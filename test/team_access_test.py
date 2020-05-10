"""
Module for testing the Terraform Cloud API Endpoint: Team Access.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeamAccess(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Access.
    """

    _unittest_name = "team-acc"

    def setUp(self):
        # Create a test team
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]

        # Invite a test user to this org, will be removed after
        invite_payload = self._get_org_membership_invite_payload()
        invite = self._api.org_memberships.invite(invite_payload)
        self._org_membership_id = invite["data"]["id"]

        # Create a test workspace
        workspace = self._api.workspaces.create(self._get_ws_without_vcs_create_payload())["data"]
        self._ws_id = workspace["id"]
        self._ws_name = workspace["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_name)
        self._api.teams.destroy(self._team_id)
        self._api.org_memberships.remove(self._org_membership_id)

    def test_team_access(self):
        """
        Test the Team Access API endpoints: ``list``, ``add``, ``remove``.
        """
        # List the team-access to workspaces, confirm there are none
        workspace_accesses = self._api.team_access.list()["data"]
        # TODO: try not to do this based on length (look for the created WS)
        self.assertEqual(len(workspace_accesses), 0)

        # Create new Team access, confirm it has been created
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
        access = self._api.team_access.add_team_access(
            team_access_create_payload)
        access_id = access["data"]["id"]

        # Show the newly created team access, confirm the ID matches to the created one
        shown_access = self._api.team_access.show(access_id)
        self.assertEqual(shown_access["data"]["id"], access_id)

        # Remove the team access, confirm it's gone
        len_after_adding = len(self._api.team_access.list()["data"])
        self._api.team_access.remove_team_access(access_id)
        # TODO: once again, do not do this based on length.
        len_after_removing = self._api.team_access.list()["data"]
        self.assertNotEqual(len_after_adding, len_after_removing)
