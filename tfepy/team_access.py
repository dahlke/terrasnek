import requests
import json

from .endpoint import TFEEndpoint

class TFETeamAccess(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._base_url = f"{base_url}/team-workspaces"

    def add_team_access(self, payload):
        # POST /team-workspaces
        results = None
        r = requests.post(self._base_url, json.dumps(payload), headers=self._headers)

        if r.status_code == 201:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def ls(self):
        # GET /team-workspaces
        results = None
        r = requests.get(self._base_url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def remove_team_access(self, access_id):
        # DELETE /team-workspaces/:id
        url = f"{self._base_url}/{access_id}"
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"Workspace access {access_id} removed.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def show_team_access(self, access_id):
        # GET /team-workspaces/:id
        results = None
        url = f"{self._base_url}/{access_id}"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
