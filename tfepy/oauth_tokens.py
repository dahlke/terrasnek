
import requests
import json

from .endpoint import TFEEndpoint

class TFEOAuthTokens(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._oauth_clients_base_url = f"{base_url}/oauth-clients"
        self._oauth_tokens_base_url = f"{base_url}/oauth-tokens"
    
    def ls(self, oauth_client_id):
        # GET /oauth-clients/:oauth_client_id/oauth-tokens
        url = f"{self._oauth_clients_base_url}/{oauth_client_id}/oauth-tokens"
        return self._ls(url)

    def show(self, id):
        # GET /oauth-tokens/:id
        url = f"{self._oauth_tokens_base_url}/{id}"
        return self._show(url)
    
    def update(self, id, payload):
        # PATCH /oauth-tokens/:id
        url = f"{self._oauth_tokens_base_url}/{id}"
        return self._update(url, payload)

    def destroy(self, id):
        # DELETE /oauth-tokens/:id
        url = f"{self._oauth_tokens_base_url}/{id}"
        return self._destroy(url)