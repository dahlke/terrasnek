import requests
import json

from .endpoint import TFEEndpoint

class TFEOAuthClients(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._org_base_url = f"{base_url}/organizations/{organization_name}/oauth-clients"
        self._oauth_clients_base_url = f"{base_url}/oauth-clients"
    
    def ls(self):
        # GET /organizations/:organization_name/oauth-clients
        return self._ls(self._org_base_url)

    def show(self, id):
        # GET /oauth-clients/:id
        url = f"{self._oauth_clients_base_url}/{id}"
        return self._show(url)
    
    def create(self, payload):
        # POST /organizations/:organization_name/oauth-clients
        return self._create(self._org_base_url, payload)
    
    def update(self, id, payload):
        # PATCH /oauth-clients/:id
        url = f"{self._oauth_clients_base_url}/{id}"
        return self._update(url, payload)

    def destroy(self, id):
        # DELETE /oauth-clients/:id
        url = f"{self._oauth_clients_base_url}/{id}"
        return self._destroy(url)
