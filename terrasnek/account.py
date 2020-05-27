"""
Module for Terraform Cloud API Endpoint: Account.
"""

from .endpoint import TFCEndpoint

class TFCAccount(TFCEndpoint):
    """
    Account represents the current user interacting with Terraform. It returns
    the same type of object as the Users API, but also includes an email
    address, which is hidden when viewing info about other users.

    https://www.terraform.io/docs/cloud/api/account.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/account"

    def required_entitlements(self):
        return []

    def show(self):
        """
        ``GET /account/details``
        """
        url = f"{self._endpoint_base_url}/details"
        return self._show(url)

    def update(self, data):
        """
        ``PATCH /account/update``

        Your username and email address can be updated with this endpoint.
        """
        url = f"{self._endpoint_base_url}/update"
        return self._patch(url, data)

    def change_password(self, data):
        """
        ``PATCH /account/password``
        """
        url = f"{self._endpoint_base_url}/password"
        return self._patch(url, data)
