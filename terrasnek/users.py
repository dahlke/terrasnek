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
        url = f"{self._users_base_url}/{user_id}"
        return self._show(url)