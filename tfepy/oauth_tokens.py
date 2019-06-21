
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
        results = None
        url = f"{self._oauth_clients_base_url}/{oauth_client_id}/oauth-tokens"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def show(self, id):
        # GET /oauth-tokens/:id
        results = None
        url = f"{self._oauth_tokens_base_url}/{id}"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
    
    def update(self, id, payload):
        # PATCH /oauth-tokens/:id
        results = None
        url = f"{self._oauth_tokens_base_url}/{id}"
        r = requests.patch(url, data=json.dumps(payload), headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def destroy(self, id):
        # DELETE /oauth-tokens/:id
        url = f"{self._oauth_tokens_base_url}/{id}"
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"OAuth client {id} destroyed.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)
