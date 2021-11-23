"""
Module for testing the Terraform Cloud API Endpoint: Agents.
"""

from terrasnek.exceptions import TFCHTTPUnprocessableEntity
from .base import TestTFCBaseTestCase


class TestTFCAgents(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Agents.
    """

    _unittest_name = "agents"
    _endpoint_being_tested = "agents"

    def test_agents(self):
        """
        Test the Agent Pools API endpoints.
        """

        # Create an agent pool, we won't assert anything on it, in case it has already been created.
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

        # List the agent pools, assert that we have only one.
        agent_pools = self._api.agents.list_pools()["data"]
        self.assertEqual(len(agent_pools), 1)

        agent_pool_id = agent_pools[0]["id"]
        shown_agent_pool = self._api.agents.show_pool(agent_pool_id)["data"]
        self.assertEqual(agent_pool_id, shown_agent_pool["id"])

        # Update the agent pool name, check that it has taken effect.
        updated_agent_pool_name = self._random_name()
        update_payload = {
            "data": {
                "type": "agent-pools",
                "attributes": {
                    "name": updated_agent_pool_name
                }
            }
        }
        updated_agent_pool = self._api.agents.update(agent_pool_id, update_payload)
        self.assertEqual(updated_agent_pool_name, updated_agent_pool["data"]["attributes"]["name"])

        # Destroy the agent pool, confirm that it's gone.
        self._api.agents.destroy_pool(agent_pool_id)
        agent_pools = self._api.agents.list_pools()["data"]
        self.assertEqual(len(agent_pools), 0)
