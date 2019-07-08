import requests
import json

from .endpoint import TFEEndpoint

class TFETeamTokens(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._base_url = f"{base_url}/teams"
    
    def create(self, team_id):
        # POST /teams/:team_id/authentication-token
        url = f"{self._base_url}/{team_id}/authentication-token"
        payload = {}
        return self._create(url, payload)

    
    def destroy(self, team_id):
        # DELETE /teams/:team_id/authentication-token
        url = f"{self._base_url}/{team_id}/authentication-token"
        return self._destroy(url)