import requests
import json

from .endpoint import TFEEndpoint

class TFETeamMemberships(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._base_url = f"{base_url}/teams"
    
    def add_a_user_to_team(self, team_id, payload):
        # POST /teams/:team_id/relationships/users
        url = f"{self._base_url}/{team_id}/relationships/users"
        r = requests.post(url, json.dumps(payload), headers=self._headers)

        # NOTE: payload needs username, not user id
        if r.status_code == 204:
            self._logger.info(f"Users added to team {team_id}.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def delete_a_user_from_team(self, team_id, payload):
        # DELETE /teams/:team_id/relationships/users
        url = f"{self._base_url}/{team_id}/relationships/users"
        r = requests.delete(url, data=json.dumps(payload), headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"Users deleted from team {team_id}.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)
