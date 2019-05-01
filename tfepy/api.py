import requests
import json
import logging

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
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)


class TFEOrganizations(TFEEndpoint):
    
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)
        self._base_url = '%s/organizations' % (base_url)

    def ls(self):
        # GET /organizations
        results = None
        # TODO: include query parameters
        r = requests.get(self._base_url, headers=self._headers)

        if r.status_code == 200:
            self._logger.info("Successfuly listed organizations.")
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def show(self, organization_name):
        # GET /organizations/:organization_name
        results = None
        url = '%s/%s' % (self._base_url, organization_name)
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            self._logger.info("The request was successful.")
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def create(self, payload):
        # POST /organizations
        results = None
        r = requests.post(self._base_url, data=payload, headers=self._headers)

        if r.status_code == 201:
            self._logger.info("The organization was successfully created.")
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def update(self, organization_name, payload):
        # PATCH /organizations/:organization_name
        results = None
        url = '%s/%s' % (self._base_url, organization_name)
        r = requests.patch(url, data=payload, headers=self._headers)

        if r.status_code == 200:
            self._logger.info("The organization was successfully updated.")
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def destroy(self, organization_name):
        # DELETE /organizations/:organization_name
        url = '%s/%s' % (self._base_url, organization_name)
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info("The organization was successfully destroyed.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)


    def entitlements(self, organization_name):
        # GET /organizations/:organization_name/entitlement-set
        results = None
        url = '%s/%s/entitlement-set' % (self._base_url, organization_name)
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))["errors"][0]
            self._logger.error(err)

        return results