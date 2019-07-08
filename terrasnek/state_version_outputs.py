import requests
import json

from .endpoint import TFEEndpoint

class TFEStateVersionOutputs(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._base_url = f"{base_url}/state-version-outputs"
    
    def show(self, state_version_output_id):
        # GET /state-version-outputs/:state_version_output_id
        url = f"{self._base_url}/{state_version_output_id}"
        return self._show(url)
    