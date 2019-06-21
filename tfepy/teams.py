import requests
import json

from .endpoint import TFEEndpoint

class TFETeams(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._teams_base_url = f"{base_url}/teams"
        self._org_base_url = f"{base_url}/organizations/{organization_name}/teams"
    
    def create(self, payload):
        # POST /organizations/:organization_name/teams
        return self._create(self._org_base_url, payload)

    def destroy(self, team_id):
        # DELETE /teams/:team_id
        url = f"{self._teams_base_url}/{team_id}"
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"Team {team_id} destroyed.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def ls(self):
        # GET organizations/:organization_name/teams
        return self._ls(self._org_base_url)

    def show(self, team_id):
        # GET /teams/:team_id
        url = f"{self._teams_base_url}/{team_id}"
        return self._show(url)