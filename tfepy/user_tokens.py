import requests
import json

from .endpoint import TFEEndpoint

class TFEUserTokens(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._users_base_url = f"{base_url}/users"
        self._tokens_base_url = f"{base_url}/authentication-tokens"
    
    def create(self, user_id, payload):
        # POST /users/:user_id/authentication-tokens
        url = f"{self._users_base_url}/{user_id}/authentication-tokens"
        print(url, payload)
        return self._create(url, payload)

    def destroy(self, token_id):
        # DELETE /authentication-tokens/:token_id
        url = f"{self._tokens_base_url}/{token_id}"
        self._destroy(url)

    def ls(self, user_id):
        # GET /users/:user_id/authentication-tokens
        url = f"{self._users_base_url}/{user_id}/authentication-tokens"
        return self._ls(url)

    def show(self, token_id):
        # GET /authentication-tokens/:token_id
        url = f"{self._tokens_base_url}/{token_id}"
        return self._show(url)