"""
Module for Terraform Cloud API Endpoint: OAuth Tokens.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCOAuthTokens(TFCEndpoint):
    """
    `OAuth Tokens API Docs \
        <https://www.terraform.io/docs/cloud/api/oauth-tokens.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._oauth_clients_api_v2_base_url = f"{self._api_v2_base_url}/oauth-clients"
        self._oauth_tokens_api_v2_base_url = f"{self._api_v2_base_url}/oauth-tokens"

    def _required_entitlements(self):
        return [Entitlements.VCS_INTEGRATIONS]

    def list(self, oauth_client_id):
        """
        ``GET /oauth-clients/:oauth_client_id/oauth-tokens``

        `OAuth Tokens List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/oauth-tokens.html#list-oauth-tokens>`_
        """
        url = f"{self._oauth_clients_api_v2_base_url}/{oauth_client_id}/oauth-tokens"
        return self._list(url)

    def show(self, token_id):
        """
        ``GET /oauth-tokens/:id``

        `OAuth Tokens Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/oauth-tokens.html#show-an-oauth-token>`_
        """
        url = f"{self._oauth_tokens_api_v2_base_url}/{token_id}"
        return self._show(url)

    def update(self, token_id, payload):
        """
        ``PATCH /oauth-tokens/:id``

        `OAuth Tokens Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/oauth-tokens.html#update-an-oauth-token>`_
        """
        url = f"{self._oauth_tokens_api_v2_base_url}/{token_id}"
        return self._update(url, payload)

    def destroy(self, token_id):
        """
        ``DELETE /oauth-tokens/:id``

        `OAuth Tokens Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/oauth-tokens.html#destroy-an-oauth-token>`_
        """
        url = f"{self._oauth_tokens_api_v2_base_url}/{token_id}"
        return self._destroy(url)
