"""
Module for Terraform Cloud API Endpoint: Agent Pools and Agents.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCAgents(TFCEndpoint):
    """
    https://www.terraform.io/docs/cloud/api/agents.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._agent_pools_api_v2_base_url = f"{self._api_v2_base_url}/agent-pools"
        self._agents_api_v2_base_url = f"{self._api_v2_base_url}/agents"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations"

    def required_entitlements(self):
        return [Entitlements.AGENTS]

    def create_pool(self, org_name):
        """
        ``POST /organizations/:organization_name/agent-pool``
        """
        url = f"{self._org_api_v2_base_url}/{org_name}/agent-pools"
        payload = {
            "data": {
                "type": "agent-pools"
            }
        }
        return self._create(url, payload)

    def list_pools(self, org_name):
        """
        ``GET /organizations/:organization_name/agent-pools``
        """
        url = f"{self._org_api_v2_base_url}/{org_name}/agent-pools"
        return self._list(url)

    def list(self, agent_pool_id):
        """
        ``GET /agent-pools/:agent_pool_id/agents``
        """
        url = f"{self._agent_pools_api_v2_base_url}/{agent_pool_id}/agents"
        return self._list(url)

    def show_pool(self, agent_pool_id):
        """
        ``GET /agent-pools/:id``
        """
        url = f"{self._agent_pools_api_v2_base_url}/{agent_pool_id}"
        return self._show(url)

    def show(self, agent_id):
        """
        ``GET /agents/:id``
        """
        url = f"{self._agents_api_v2_base_url}/{agent_id}"
        return self._show(url)
