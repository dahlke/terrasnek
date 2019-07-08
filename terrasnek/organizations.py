import requests
import json

from .endpoint import TFEEndpoint

class TFEOrganizations(TFEEndpoint):
    
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)
        self._org_base_url = f"{base_url}/organizations"

    def create(self, payload):
        # POST /organizations
        return self._create(self._org_base_url, payload)

    def destroy(self, organization_name):
        # DELETE /organizations/:organization_name
        url = f"{self._org_base_url}/{organization_name}"
        return self._destroy(url)

    def entitlements(self, organization_name):
        # GET /organizations/:organization_name/entitlement-set
        results = None
        url = f"{self._org_base_url}/{organization_name}/entitlement-set"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))["errors"][0]
            self._logger.error(err)

        return results

    def ls(self):
        # GET /organizations
        # TODO: include query parameters
        return self._ls(self._org_base_url)

    def show(self, organization_name):
        # GET /organizations/:organization_name
        url = f"{self._org_base_url}/{organization_name}"
        return self._show(url)

    def update(self, organization_name, payload):
        # PATCH /organizations/:organization_name
        url = f"{self._org_base_url}/{organization_name}"
        return self._update(url, payload)