"""
Module for Terraform Cloud API Endpoint: OAuth Tokens.
"""

from .endpoint import TFCEndpoint

class TFCOAuthTokens(TFCEndpoint):
    """
    The oauth-token object represents a VCS configuration which includes the OAuth
    connection and the associated OAuth token. This object is used when creating a
    workspace to identify which VCS connection to use.

    https://www.terraform.io/docs/cloud/api/oauth-tokens.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._oauth_clients_base_url = f"{base_url}/oauth-clients"
        self._oauth_tokens_base_url = f"{base_url}/oauth-tokens"

    def list(self, oauth_client_id):
        """
        GET /oauth-clients/:oauth_client_id/oauth-tokens

        List all the OAuth Tokens for a given OAuth Client
        """
        url = f"{self._oauth_clients_base_url}/{oauth_client_id}/oauth-tokens"
        return self._list(url)

    def show(self, token_id):
        """
        GET /oauth-tokens/:token_id
        """
        url = f"{self._oauth_tokens_base_url}/{token_id}"
        return self._show(url)

    def update(self, token_id, payload):
        """
        PATCH /oauth-tokens/:token_id
        """
        url = f"{self._oauth_tokens_base_url}/{token_id}"
        return self._update(url, payload)

    def destroy(self, token_id):
        """
        DELETE /oauth-tokens/:token_id
        """
        url = f"{self._oauth_tokens_base_url}/{token_id}"
        return self._destroy(url)
