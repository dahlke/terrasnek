import requests
import json

from .endpoint import TFEEndpoint

class TFEAdminOrganizations(TFEEndpoint):
    
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)
        self._orgs_base_url = f"{base_url}/admin/organizations"

    def destroy(self, organization_name):
        # DELETE /admin/organizations/:organization_name
        url = f"{self._orgs_base_url}/{organization_name}"
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def ls(self):
        # GET /admin/organizations
        results = None
        # TODO: include query parameters
        r = requests.get(self._orgs_base_url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def show(self, organization_name):
        # GET /admin/organizations/:organization_name
        results = None
        url = f"{self._orgs_base_url}/{organization_name}"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results