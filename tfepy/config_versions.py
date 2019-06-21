import requests
import json

from .endpoint import TFEEndpoint

class TFEConfigVersions(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._ws_base_url = f"{base_url}/workspaces"
        self._config_version_base_url = f"{base_url}/configuration-versions"
    
    def ls(self, workspace_id):
        # GET /workspaces/:workspace_id/configuration-versions
        url = f"{self._ws_base_url}/{workspace_id}/configuration-versions"
        return self._ls(url)

    def show(self, id):
        # GET /configuration-versions/:configuration-id
        url = f"{self._config_version_base_url}/{id}"
        return self._show(url)
    
    def create(self, workspace_id, payload):
        # POST /workspaces/:workspace_id/configuration-versions
        url = f"{self._ws_base_url}/{workspace_id}/configuration-versions"
        return self._create(url, payload)

    """    
    # As of now, this will remain unimplemented. 

    def upload(self):
        self._logger.error("Upload Configuration versions has not been implemented.")
    """    