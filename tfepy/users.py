import requests
import json

from .endpoint import TFEEndpoint

class TFEUsers(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._users_base_url = f"{base_url}/users"
    
    def show(self, user_id):
        # GET /users/:user_id
        results = None
        url = f"{self._users_base_url}/{user_id}"
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results