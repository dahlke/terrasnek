"""
Module for testing the Terraform Cloud API Endpoint: Team Memberships.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeamMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Memberships.
    """

    _unittest_name = "team-mem"
    _endpoint_being_tested = "team_memberships"

    def setUp(self):
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]
        invite = self._api.org_memberships.invite(self._get_org_membership_invite_payload())
        self._org_membership_id = invite["data"]["id"]

    def tearDown(self):
        self._api.teams.destroy(self._team_id)
        self._api.org_memberships.remove(self._org_membership_id)

    def test_team_memberships(self):
        """
        Test the Team Memberships API endpoints.
        """

        logged_in_user = self._api.account.show()["data"]
        logged_in_username = logged_in_user["attributes"]["username"]

        # Add our user to the team, confirm they have been added
        membership_payload = {
            "data": [
                {
                    "type": "users",
                    "id": logged_in_username
                }
            ]
        }
        self._api.team_memberships.add_user_to_team(
            self._team_id, membership_payload)

        # Show the team memberships, confirm that only one user is in the teeam
        # since we just created it.
        shown_team = self._api.teams.show(self._team_id)["data"]
        self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 1)

        # Remove the user from the team, and confirm there are no users
        # left in the team.
        self._api.team_memberships.remove_user_from_team(
            self._team_id, membership_payload)
        shown_team = self._api.teams.show(self._team_id)["data"]
        self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 0)
