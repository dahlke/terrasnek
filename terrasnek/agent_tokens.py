"""
Module for Terraform Cloud API Endpoint: Agent Tokens.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCAgentTokens(TFCEndpoint):
    """
    `Agent Tokens API Docs \
        <https://www.terraform.io/docs/cloud/api/agent-tokens.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._agent_pools_api_v2_base_url = f"{self._api_v2_base_url}/agent-pools"
        self._auth_tokens_api_v2_base_url = f"{self._api_v2_base_url}/authentication-tokens"

    def required_entitlements(self):
        return [Entitlements.AGENTS]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, agent_pool_id, payload):
        """
        ``POST /agent-pools/:agent_pool_id/authentication-tokens``

        `Agent Tokens Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/agent-tokens.html#create-an-agent-token>`_
        """
        url = f"{self._agent_pools_api_v2_base_url}/{agent_pool_id}/authentication-tokens"
        return self._create(url, payload)

    def list(self, agent_pool_id):
        """
        ``GET /agent-pools/:agent_pool_id/authentication-tokens``

        `Agent Tokens List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/agent-tokens.html#list-agent-tokens>`_
        """
        url = f"{self._agent_pools_api_v2_base_url}/{agent_pool_id}/authentication-tokens"
        return self._list(url)

    def show(self, token_id):
        """
        ``GET /authentication-tokens/:id``

        `Agent Tokens Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/agent-tokens.html#show-an-agent-token>`_
        """
        url = f"{self._auth_tokens_api_v2_base_url}/{token_id}"
        return self._show(url)

    def destroy(self, token_id):
        """
        ``DELETE /api/v2/authentication-tokens/:id``

        `Agent Tokens Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/agent-tokens.html#destroy-an-agent-token>`_
        """
        url = f"{self._auth_tokens_api_v2_base_url}/{token_id}"
        return self._destroy(url)
