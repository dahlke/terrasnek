import requests
import json

from .endpoint import TFEEndpoint

class TFEPlans(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._base_url = f"{base_url}/plans"
    
    def show(self, plan_id):
        # GET /plans/:plan_id
        url = f"{self._base_url}/{plan_id}"
        return self._show(url)