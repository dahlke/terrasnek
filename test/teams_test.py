"""
Module for testing the Terraform Cloud API Endpoint: Teams.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeams(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Teams.
    """

    _unittest_name = "teams"

    def test_team(self):
        """
        Test the Teams API endpoints: ``list``, ``create``, ``show``, ``destroy``.
        """
        # List all the teams, confirm that there is only one team
        # TODO: check the response type instead
        teams = self._api.teams.list()["data"]
        self.assertEqual(len(teams), 1)

        # Create a new team, confirm that it has been created
        new_team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        new_team_id = new_team["id"]
        teams = self._api.teams.list()["data"]
        # TODO: look for the newly created team instead of checking length
        self.assertEqual(len(teams), 2)

        # Show the newly created team, assert that the response matches the ID we fed in.
        shown_team = self._api.teams.show(new_team_id)["data"]
        self.assertEqual(shown_team["id"], new_team_id)

        # Destroy the team, confirm it's gone
        self._api.teams.destroy(new_team_id)
        teams = self._api.teams.list()["data"]
        # TODO: Look for the team by ID instead of looking at the length
        self.assertEqual(len(teams), 1)
