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

    def upload(self, path_to_tarball, id):
        # PUT {derived_config_version_upload_url}
        results = None
        # TODO: Validate the path to tarball a bit
        upload_url = self.show(id)["data"]["attributes"]["upload-url"]

        # TODO: Exception and error handling
        r = None
        with open(path_to_tarball, 'rb') as data:
            r = requests.put(upload_url, data=data, headers=self._headers)
        
        if r.status_code == 200:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
