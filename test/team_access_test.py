"""
Module for testing the Terraform Cloud API Endpoint: Team Access.
"""

from .base import TestTFCBaseTestCase

class TestTFCTeamAccess(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Access.
    """

    _unittest_name = "team-acc"
    _endpoint_being_tested = "team_access"

    def setUp(self):
        # Create a test team
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]

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
        self._api.org_memberships.remove(self._org_membership_id)

    def test_team_access(self):
        """
        Test the Team Access API endpoints.
        """

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

        # Update team access
        update_payload = {
            "data": {
                "attributes": {
                    "access": "custom",
                    "state-versions": "none"
                }
            }
        }
        updated_access = self._api.team_access.update(access_id, update_payload)["data"]
        self.assertEqual(updated_access["attributes"]["state-versions"], "none")

        list_filters = [
            {
                "keys": ["workspace", "id"],
                "value": self._ws_id
            }
        ]
        listed_access = self._api.team_access.list(filters=list_filters)["data"]
        self.assertEqual(updated_access["id"], listed_access[0]["id"])

        # Remove the team access, confirm it's gone
        self._api.team_access.remove_team_access(access_id)
        all_team_access = self._api.workspaces.list()["data"]
        found_team_access = False
        for team_access in all_team_access:
            if team_access["id"] == access_id:
                found_team_access = True
                break
        self.assertFalse(found_team_access)
