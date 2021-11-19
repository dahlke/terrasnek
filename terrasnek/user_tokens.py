"""
Module for Terraform Cloud API Endpoint: User Tokens.
"""

from .endpoint import TFCEndpoint

class TFCUserTokens(TFCEndpoint):
    """
    `User Tokens API Docs \
        <https://www.terraform.io/docs/cloud/api/user-tokens.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._users_api_v2_base_url = f"{self._api_v2_base_url}/users"
        self._tokens_api_v2_base_url = f"{self._api_v2_base_url}/authentication-tokens"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, user_id, payload):
        """
        ``POST /users/:user_id/authentication-tokens``

        `User Tokens Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/user-tokens.html#create-a-user-token>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/user-tokens.html#sample-payload>`_
        """
        url = f"{self._users_api_v2_base_url}/{user_id}/authentication-tokens"
        return self._create(url, payload)

    def destroy(self, token_id):
        """
        ``DELETE /authentication-tokens/:id``

        `User Tokens Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/user-tokens.html#destroy-a-user-token>`_

        """
        url = f"{self._tokens_api_v2_base_url}/{token_id}"
        self._destroy(url)

    def list(self, user_id):
        """
        ``GET /users/:user_id/authentication-tokens``

        `User Tokens List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/user-tokens.html#list-user-tokens>`_

        """
        url = f"{self._users_api_v2_base_url}/{user_id}/authentication-tokens"
        return self._list(url)

    def show(self, token_id):
        """
        ``GET /authentication-tokens/:id``

        `User Tokens Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/user-tokens.html#show-a-user-token>`_
        """
        url = f"{self._tokens_api_v2_base_url}/{token_id}"
        return self._show(url)
