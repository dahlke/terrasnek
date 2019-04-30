import requests
import json

TFE_SAAS_URL = "https://app.terraform.io"

class TFE():

    def __init__(self, api_token, url=TFE_SAAS_URL):
        self._instance_url = "%s/api/v2" % (url)
        self._token = api_token
        self._headers = {
            "Authorization": "Bearer %s" % api_token,
            "Content-Type": "application/vnd.api+json"
        }

        self.organizations = TFEOrganizations(self._instance_url, self._headers)

class TFEEndpoint():

    def __init__(self, base_url, headers):
        self._base_url = base_url
        self._headers = headers


class TFEOrganizations(TFEEndpoint):
    
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)
        self._base_url = '%s/organizations' % (base_url)

    def ls(self):
        # GET /organizations
        results = None
        r = requests.get(self._base_url, headers=self._headers)

        if r.status_code == 400:
            # TODO
            pass
        elif r.status_code == 200:
            results = json.loads(r.content)

        return results

    def show(self, organization_name):
        # GET /organizations/:organization_name
        _url = '%s/%s' % (organization_name)

        # Handle Error Codes
        pass

    def create(self, payload):
        # POST /organizations

        # Handle Error Codes
        pass

    def update(self, organization_name, payload):
        # PATCH /organizations/:organization_name

        # Handle Error Codes
        pass

    def destroy(self, organization_name):
        # DELETE /organizations/:organization_name

        # Handle Error Codes
        pass

    def entitlements(self, organization_name):
        # GET /organizations/:organization_name/entitlement-set

        # Handle Error Codes
        pass