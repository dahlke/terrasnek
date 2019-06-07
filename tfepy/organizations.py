import requests
import json

from .endpoint import TFEEndpoint

class TFEOrganizations(TFEEndpoint):
    
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)
        self._orgs_base_url = f"{base_url}/organizations"

    def create(self, payload):
        # POST /organizations
        results = None
        r = requests.post(self._orgs_base_url, data=json.dumps(payload), headers=self._headers)

        if r.status_code == 201:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def destroy(self, organization_name):
        # DELETE /organizations/:organization_name
        url = f"{self._orgs_base_url}/{organization_name}"
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)


    def entitlements(self, organization_name):
        # GET /organizations/:organization_name/entitlement-set
        results = None
        url = f"{self._orgs_base_url}/{organization_name}/entitlement-set"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))["errors"][0]
            self._logger.error(err)

        return results

    def ls(self):
        # GET /organizations
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
        # GET /organizations/:organization_name
        results = None
        url = f"{self._orgs_base_url}/{organization_name}"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def update(self, organization_name, payload):
        # PATCH /organizations/:organization_name
        results = None
        url = f"{self._orgs_base_url}/{organization_name}"
        r = requests.patch(url, data=json.dumps(payload), headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results