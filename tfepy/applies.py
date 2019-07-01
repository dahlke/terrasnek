import requests
import json

from .endpoint import TFEEndpoint

class TFEApplies(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._base_url = f"{base_url}/applies"
    
    def show(self, apply_id):
        # GET /applies/:apply_id
        url = f"{self._base_url}/{apply_id}"
        return self._show(url)