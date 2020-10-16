"""
Module for testing the Terraform Cloud API Endpoint: Teams.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeams(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Teams.
    """

    _unittest_name = "teams"
    _endpoint_being_tested = "teams"

    def test_teams(self):
        """
        Test the Teams API endpoints.
        """

        # List all the teams, confirm that the response type
        teams = self._api.teams.list()["data"]
        self.assertEqual("teams", teams[0]["type"])

        # Create a new team, confirm that it has been created
        new_team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        new_team_id = new_team["id"]
        all_teams = self._api.teams.list()["data"]
        found_team = False
        for team in all_teams:
            if team["id"] == new_team_id:
                found_team = True
                break
        self.assertTrue(found_team)

        # Show the newly created team, assert that the response matches the ID we fed in.
        shown_team = self._api.teams.show(new_team_id)["data"]
        self.assertEqual(shown_team["id"], new_team_id)

        # Update the team to have VCS management access, confirm the changes took effect.
        update_payload = {
            "data": {
                "type": "teams",
                "attributes": {
                    "visibilty": "organization",
                    "organization-access": {
                        "manage-vcs-settings": True
                    }
                }
            }
        }
        updated_team = self._api.teams.update(new_team_id, update_payload)["data"]
        self.assertTrue(updated_team["attributes"]["organization-access"]["manage-vcs-settings"])

        # Destroy the team, confirm it's gone
        self._api.teams.destroy(new_team_id)
        all_teams = self._api.teams.list()["data"]
        found_team = False
        for team in all_teams:
            if team["id"] == new_team_id:
                found_team = True
                break
        self.assertFalse(found_team)
