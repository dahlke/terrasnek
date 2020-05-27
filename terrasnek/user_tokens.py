"""
Module for Terraform Cloud API Endpoint: User Tokens.
"""

from .endpoint import TFCEndpoint

class TFCUserTokens(TFCEndpoint):
    """
    https://www.terraform.io/docs/cloud/api/user-tokens.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._users_api_v2_base_url = f"{self._api_v2_base_url}/users"
        self._tokens_api_v2_base_url = f"{self._api_v2_base_url}/authentication-tokens"

    def required_entitlements(self):
        return []

    def create(self, user_id, payload):
        """
        ``POST /users/:user_id/authentication-tokens``

        This endpoint returns the secret text of the created authentication token. A token
        is only shown upon creation, and cannot be recovered later.

        NOTE: the following method descriptor is here for the api_comparison.py script to pass,
        since it uses a different prefix than the majority of endpoints.

        ``POST /api/v2/users/:user_id/authentication-tokens``
        """
        url = f"{self._users_api_v2_base_url}/{user_id}/authentication-tokens"
        return self._create(url, payload)

    def destroy(self, token_id):
        """
        ``DELETE /authentication-tokens/:id``

        NOTE: the following method descriptor is here for the api_comparison.py script to pass,
        since it uses a different prefix than the majority of endpoints.

        ``DELETE /api/v2/authentication-tokens/:id``
        """
        url = f"{self._tokens_api_v2_base_url}/{token_id}"
        self._destroy(url)

    def list(self, user_id):
        """
        ``GET /users/:user_id/authentication-tokens``

        Use the Account API to find your own user ID.

        The objects returned by this endpoint only contain metadata, and do not include the
        secret text of any authentication tokens. A token is only shown upon creation, and
        cannot be recovered later.

        NOTE: the following method descriptor is here for the api_comparison.py script to pass,
        since it uses a different prefix than the majority of endpoints.

        ``GET /api/v2/users/:user_id/authentication-tokens``
        """
        url = f"{self._users_api_v2_base_url}/{user_id}/authentication-tokens"
        return self._list(url)

    def show(self, token_id):
        """
        ``GET /authentication-tokens/:id``

        The objects returned by this endpoint only contain metadata, and do not include the
        secret text of any authentication tokens. A token is only shown upon creation, and
        cannot be recovered later.

        NOTE: the following method descriptor is here for the api_comparison.py script to pass,
        since it uses a different prefix than the majority of endpoints.

        ``GET /api/v2/authentication-tokens/:id``
        """
        url = f"{self._tokens_api_v2_base_url}/{token_id}"
        return self._show(url)
