
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
        results = None
        r = requests.get(self._org_base_url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def show(self, id):
        # GET /oauth-clients/:id
        results = None
        url = f"{self._oauth_clients_base_url}/{id}"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
    
    def create(self, payload):
        # POST /organizations/:organization_name/oauth-clients
        results = None
        r = requests.post(self._org_base_url, json.dumps(payload), headers=self._headers)

        if r.status_code == 201:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
    
    def update(self, id, payload):
        # PATCH /oauth-clients/:id
        results = None
        url = f"{self._oauth_clients_base_url}/{id}"
        r = requests.patch(url, data=json.dumps(payload), headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def destroy(self, id):
        # DELETE /oauth-clients/:id
        url = f"{self._oauth_clients_base_url}/{id}"
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"OAuth client {id} destroyed.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

