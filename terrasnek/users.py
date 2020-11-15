"""
Module for Terraform Cloud API Endpoint: Users.
"""

from .endpoint import TFCEndpoint

class TFCUsers(TFCEndpoint):
    """
    `Users API Docs \
        <https://www.terraform.io/docs/cloud/api/users.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._users_api_v2_base_url = f"{self._api_v2_base_url}/users"

    def _required_entitlements(self):
        return []

    def show(self, user_id):
        """
        ``GET /users/:user_id``

        `Users Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/users.html#show-a-user>`_
        """
        url = f"{self._users_api_v2_base_url}/{user_id}"
        return self._show(url)
