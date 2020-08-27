"""
Module for testing the Terraform Cloud API Endpoint: Agents.
"""

from .base import TestTFCBaseTestCase


class TestTFCAgents(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Agents.
    """

    _unittest_name = "agents"
    _endpoint_being_tested = "agents"

    def test_agent_pools_endpoints(self):
        """
        Test the Agents API endpoints: ``list``, ``show``, ``create``,
        ``show_pool``, ``list_pool``.
        """

        # Create an agent pool, we won't assert anything on it, in case it has already been created.
        self._api.agents.create_pool(self._test_org_name)

        # List the agent pools, assert that we have only one.
        agent_pools = self._api.agents.list_pools(self._test_org_name)["data"]
        self.assertEqual(len(agent_pools), 1)

        agent_pool_id = agent_pools[0]["id"]
        shown_agent_pool = self._api.agents.show_pool(agent_pool_id)["data"]
        self.assertEqual(agent_pool_id, shown_agent_pool["id"])

        # TODO: show, list require me to actually add some agents to test
