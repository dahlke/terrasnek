import requests
import json

from .endpoint import TFEEndpoint

class TFEStateVersions(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._state_version_base_url = f"{base_url}/state-versions"
        self._workspace_base_url = f"{base_url}/workspaces"
    
    def create(self, workspace_id, payload):
        # POST /workspaces/:workspace_id/state-versions
        url = f"{self._workspace_base_url}/{workspace_id}/state-versions"
        return self._create(url, payload)
    
    def get_current(self, workspace_id):
        # GET /workspaces/:workspace_id/current-state-version
        results = None
        url = f"{self._workspace_base_url}/{workspace_id}/current-state-version"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
    
    def ls(self, workspace_name):
        # GET /state-versions
        url = f"{self._state_version_base_url}?filter[organization][name]={self._organization_name}&filter[workspace][name]={workspace_name}"
        return self._ls(url)

    def show(self, state_version_id):
        # GET /state-versions/:state_version_id
        url = f"{self._state_version_base_url}/{state_version_id}"
        return self._show(url)
    