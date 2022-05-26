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

        # Confirm we have our teams, as well as the included values
        some_teams_raw = self._api.teams.list(include=["users"])
        self.assertIn("included", some_teams_raw)

        some_teams = some_teams_raw["data"]
        found_team = False
        owners_team_id = None
        for team in some_teams:
            if team["id"] == new_team_id:
                found_team = True
            if team["attributes"]["name"] == "owners":
                owners_team_id = team["id"]
            if found_team and owners_team_id is not None:
                break
        self.assertTrue(found_team)

        # Show the owners team, assert that the response matches the ID we fed in
        shown_team_raw = self._api.teams.show(owners_team_id, include=["users"])
        # Make sure that we have the related resources
        self.assertIn("included", shown_team_raw)
        shown_team = shown_team_raw["data"]
        self.assertEqual(shown_team["id"], owners_team_id)

        # List all the teams, confirm we have the right number and the related resources
        all_teams = self._api.teams.list_all(include=["users"])
        self.assertIn("included", all_teams)
        self.assertEqual(len(all_teams["data"]), 2)

        new_team_name = new_team["attributes"]["name"]
        test_filters = [
            {
                "keys": ["names"],
                "value": new_team_name
            }
        ]
        filtered_teams = self._api.teams.list_all(filters=test_filters)["data"]
        self.assertTrue(filtered_teams[0]["attributes"]["name"], new_team_name)

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
        some_teams = self._api.teams.list()["data"]
        found_team = False
        for team in some_teams:
            if team["id"] == new_team_id:
                found_team = True
                break
        self.assertFalse(found_team)
