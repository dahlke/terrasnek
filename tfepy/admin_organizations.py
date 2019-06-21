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
        return self._destroy(url)

    def ls(self):
        # GET /admin/organizations
        return self._ls(self._orgs_base_url)

    def show(self, organization_name):
        # GET /admin/organizations/:organization_name
        url = f"{self._orgs_base_url}/{organization_name}"
        return self._show(url)