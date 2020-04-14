"""
Module for testing the Terraform Cloud API Endpoint: Team Memberships.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeamMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Memberships.
    """

    def setUp(self):
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]

    def tearDown(self):
        self._api.teams.destroy(self._team_id)

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
            self._team_id, membership_payload)
        shown_team = self._api.teams.show(self._team_id)["data"]
        self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 1)
        self._api.team_memberships.remove_a_user_from_team(
            self._team_id, membership_payload)
        shown_team = self._api.teams.show(self._team_id)["data"]
        self.assertEqual(len(shown_team["relationships"]["users"]["data"]), 0)
