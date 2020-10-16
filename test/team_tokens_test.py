"""
Module for testing the Terraform Cloud API Endpoint: Team Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCTeamTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Team Tokens.
    """

    _unittest_name = "team-tok"
    _endpoint_being_tested = "team_tokens"

    def setUp(self):
        self._team = self._api.teams.create(
            self._get_team_create_payload())["data"]
        self._team_id = self._team["id"]

    def tearDown(self):
        self._api.teams.destroy(self._team_id)

    def test_team_tokens(self):
        """
        Test the Team Tokens API endpoints.
        """

        # Create a test token and make sure we get an ID back
        created_token = self._api.team_tokens.create(self._team_id)["data"]
        self.assertIsNotNone(created_token["id"])

        # Then destroy it. There is no lookup so there's nothing to test here.
        self._api.team_tokens.destroy(self._team_id)
