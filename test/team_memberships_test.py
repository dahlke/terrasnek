"""
Module for testing the Terraform Cloud API Endpoint: Team Memberships.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeamMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Memberships.
    """

    _unittest_name = "team-mem"

    def setUp(self):
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]
        # TODO: allow passing vars to the invite payload function
        invite_payload = self._get_org_membership_invite_payload()
        invite = self._api.org_memberships.invite(invite_payload)
        self._org_membership_id = invite["data"]["id"]

    def tearDown(self):
        self._api.teams.destroy(self._team_id)
        self._api.org_memberships.remove(self._org_membership_id)

    def test_team_memberships(self):
        """
        Test the Team Memberships API endpoints: ``add``, ``show``, ``remove``.
        """
        # Add the testing user to the team, confirm they have been added
        membership_payload = {
            "data": [
                {
                    "type": "users",
                    "id": self._test_username
                }
            ]
        }
        self._api.team_memberships.add_a_user_to_team(
            self._team_id, membership_payload)

        # TODO: Both of the following asserts will not work unless the user
        # accepts the request.

        # Show the team memberships, confirm it's the length we expect
        # TODO: look for the user, not just the number of team members
        # shown_team = self._api.teams.show(self._owners_team_id)["data"]
        # self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 3)

        self._api.team_memberships.remove_a_user_from_team(
            self._team_id, membership_payload)

        # shown_team = self._api.teams.show(self._owners_team_id)["data"]
        # self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 0)
