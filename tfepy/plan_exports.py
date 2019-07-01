import requests
import json

from .endpoint import TFEEndpoint

class TFEPlanExports(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._base_url = f"{base_url}/plan-exports"
    
    def create(self, payload):
        # POST /plan-exports
        return self._create(self._base_url, payload)

    def show(self, plan_export_id):
        # GET /plan-exports/:plan_export_id
        url = f"{self._base_url}/{plan_export_id}"
        return self._show(url)
    
    def download(self, plan_export_id, target_path="/tmp/terrasnek.planexport.tar.gz"):
        # GET /plan-exports/:plan_export_id/download
        url = f"{self._base_url}/{plan_export_id}/download"
        r = requests.get(url, headers=self._headers)
        with open(target_path, 'wb') as f:
            f.write(r.content)

    def destroy(self, plan_export_id):
        # DELETE /plan-exports/:plan_export_id
        url = f"{self._base_url}/{plan_export_id}"
        return self._destroy(url)