"""
Module for testing the Terraform Cloud API Endpoint: Agent Tokens.
"""

from .base import TestTFCBaseTestCase


class TestTFCAgentTokens(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Agent Tokens.
    """

    _unittest_name = "agt-tokens"
    _endpoint_being_tested = "agent_tokens"

    def setUp(self):
        # Make sure that we have an Agent Pool on the org if it hasn't already been enabled.
        self._api.agents.create_pool(self._test_org_name)

        agent_pools = self._api.agents.list_pools(self._test_org_name)["data"]
        self._agent_pool_id = agent_pools[0]["id"]

    def test_agent_tokens_endpoints(self):
        """
        Test the Agent Tokens API endpoints: ``list``, ``show``, ``create``, ``destroy``.
        """

        # List the tokens, assert we have zero
        agent_tokens = self._api.agent_tokens.list(self._agent_pool_id)["data"]
        self.assertEqual(len(agent_tokens), 0)

        # Create an agent token, store it's ID
        created_agent_token = self._api.agent_tokens.create(self._agent_pool_id)["data"]
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
