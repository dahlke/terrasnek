"""
Module for Terraform Cloud API Endpoint: User Tokens.
"""

from .endpoint import TFCEndpoint

class TFCUserTokens(TFCEndpoint):
    """
    https://www.terraform.io/docs/cloud/api/user-tokens.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._users_base_url = f"{base_url}/users"
        self._tokens_base_url = f"{base_url}/authentication-tokens"

    def create(self, user_id, payload):
        """
        POST /users/:user_id/authentication-tokens

        This endpoint returns the secret text of the created authentication token. A token
        is only shown upon creation, and cannot be recovered later.
        """
        url = f"{self._users_base_url}/{user_id}/authentication-tokens"
        return self._create(url, payload)

    def destroy(self, token_id):
        """
        DELETE /authentication-tokens/:token_id
        """
        url = f"{self._tokens_base_url}/{token_id}"
        self._destroy(url)

    def list(self, user_id):
        """
        GET /users/:user_id/authentication-tokens

        Use the Account API to find your own user ID.

        The objects returned by this endpoint only contain metadata, and do not include the
        secret text of any authentication tokens. A token is only shown upon creation, and
        cannot be recovered later.
        """
        url = f"{self._users_base_url}/{user_id}/authentication-tokens"
        return self._list(url)

    def show(self, token_id):
        """
        GET /authentication-tokens/:token_id

        The objects returned by this endpoint only contain metadata, and do not include the
        secret text of any authentication tokens. A token is only shown upon creation, and
        cannot be recovered later.
        """
        url = f"{self._tokens_base_url}/{token_id}"
        return self._show(url)
