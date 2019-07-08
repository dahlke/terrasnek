import requests
import json

from .endpoint import TFEEndpoint

class TFEVariables(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._base_url = f"{base_url}/vars"
    
    def create(self, payload):
        # POST /vars
        return self._create(self._base_url, payload)
    
    def ls(self, workspace_name=None):
        # GET /vars
        url = f"{self._base_url}?filter[organization][name]={self._organization_name}&filter[workspace][name]={workspace_name}"

        # TODO: follow this pattern for other filters, maybe enumerate kwargs?
        if workspace_name is not None:
            url = f"{url}&filter[workspace][name]={workspace_name}"

        return self._ls(url)
    
    def update(self, variable_id, payload):
        # PATCH /vars/:variable_id
        url = f"{self._base_url}/{variable_id}"
        return self._update(url, payload)
    
    def destroy(self, variable_id):
        # DELETE /vars/:variable_id
        url = f"{self._base_url}/{variable_id}"
        return self._destroy(url)