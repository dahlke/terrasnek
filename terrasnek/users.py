"""
Module for Terraform Cloud API Endpoint: Users.
"""

from .endpoint import TFCEndpoint

class TFCUsers(TFCEndpoint):
    """
    Terraform Cloud (TFC)'s user objects do not contain any identifying information about a
    user, other than their TFC username and avatar image; they are intended for displaying names
    and avatars in contexts that refer to a user by ID, like lists of team members or the details
    of a run. Most of these contexts can already include user objects via an ?include parameter,
    so you shouldn't usually need to make a separate call to this endpoint.

    https://www.terraform.io/docs/cloud/api/users.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._users_api_v2_base_url = f"{self._api_v2_base_url}/users"

    def required_entitlements(self):
        return []

    def show(self, user_id):
        """
        ``GET /users/:user_id``

        Shows details for a given user.
        """
        url = f"{self._users_api_v2_base_url}/{user_id}"
        return self._show(url)
