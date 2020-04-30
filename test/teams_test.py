"""
Module for testing the Terraform Cloud API Endpoint: Teams.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeams(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Teams.
    """

    def test_team_lifecycle(self):
        """
        Test the Teams API endpoints: list, create, show, destroy.
        """

        teams = self._api.teams.list()["data"]
        self.assertEqual(len(teams), 1)

        new_team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        new_team_id = new_team["id"]
        teams = self._api.teams.list()["data"]
        self.assertEqual(len(teams), 2)

        shown_team = self._api.teams.show(new_team_id)["data"]
        self.assertEqual(shown_team["id"], new_team_id)

        self._api.teams.destroy(new_team_id)
        teams = self._api.teams.list()["data"]
        self.assertEqual(len(teams), 1)
