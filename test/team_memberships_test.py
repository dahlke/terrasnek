"""
Module for testing the Terraform Cloud API Endpoint: Team Memberships.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeamMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Memberships.
    """

    def setUp(self):
        # Invite a user to the owners team, then we'll invite them to the newly created team
        teams = self._api.teams.list()
        owners_team = teams["data"][0]
        self._owners_team_id = owners_team["id"]
        invite_payload = self._get_org_membership_invite_payload()
        invite = self._api.org_memberships.invite(invite_payload)
        self._org_membership_id = invite["data"]["id"]

    def tearDown(self):
        self._api.org_memberships.remove(self._org_membership_id)

    def test_team_memberships(self):
        """
        Test the Team Memberships API endpoints: add, show, remove.
        """

        membership_payload = {
            "data": [
                {
                    "type": "users",
                    "id": self._test_username
                }
            ]
        }

        self._api.team_memberships.add_a_user_to_team(
            self._owners_team_id, membership_payload)

        # TODO: Both of the following asserts will not work unless the user
        # accepts the request.

        # shown_team = self._api.teams.show(self._owners_team_id)["data"]
        # self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 3)

        self._api.team_memberships.remove_a_user_from_team(
            self._owners_team_id, membership_payload)

        # shown_team = self._api.teams.show(self._owners_team_id)["data"]
        # self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 0)
