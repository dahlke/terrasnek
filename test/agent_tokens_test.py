"""
Module for testing the Terraform Cloud API Endpoint: Agent Tokens.
"""

from terrasnek.exceptions import TFCHTTPUnprocessableEntity
from .base import TestTFCBaseTestCase


class TestTFCAgentTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Agent Tokens.
    """

    _unittest_name = "agt-tokens"
    _endpoint_being_tested = "agent_tokens"

    def setUp(self):
        # Make sure that we have an Agent Pool on the org if it hasn't already been enabled.
        create_payload = {
            "data": {
                "type": "agent-pools",
                "attributes": {
                    "name": self._random_name()
                }
            }
        }

        try:
            self._api.agents.create_pool(create_payload)
        except TFCHTTPUnprocessableEntity as exc:
            # NOTE: this is not a good test, but the API endpoint isn't very flexible.
            self._logger.info("\
                Unprocessable entity for agent pool. You may already have one created.")
            self._logger.error(exc)

        agent_pools = self._api.agents.list_pools()["data"]
        self._agent_pool_id = agent_pools[0]["id"]

    def test_agent_tokens(self):
        """
        Test the Agent Tokens API endpoints.
        """

        # List the tokens, assert we have zero
        agent_tokens = self._api.agent_tokens.list(self._agent_pool_id)["data"]
        self.assertEqual(len(agent_tokens), 0)

        # Create an agent token, store it's ID
        create_payload = {
            "data": {
                "type": "authentication-tokens",
                "attributes": {
                    "description": "foo"
                }
            }
        }
        created_agent_token = \
            self._api.agent_tokens.create(self._agent_pool_id, create_payload)["data"]
        created_agent_token_id = created_agent_token["id"]

        # List the agent tokens again, assert we have one
        agent_tokens = self._api.agent_tokens.list(self._agent_pool_id)["data"]
        self.assertEqual(len(agent_tokens), 1)

        shown_agent_token = self._api.agent_tokens.show(created_agent_token_id)["data"]
        self.assertEqual(shown_agent_token["id"], created_agent_token_id)

        # Destroy the token, assert we have zero again
        self._api.agent_tokens.destroy(created_agent_token_id)
        agent_tokens = self._api.agent_tokens.list(self._agent_pool_id)["data"]
        self.assertEqual(len(agent_tokens), 0)
