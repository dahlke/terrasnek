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

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/account"

    def required_entitlements(self):
        return []

    def show(self):
        """
        ``GET /account/details``
        """
        url = f"{self._base_url}/details"
        return self._show(url)

    def update(self, data):
        """
        ``PATCH /account/update``

        Your username and email address can be updated with this endpoint.
        """
        url = f"{self._base_url}/update"
        return self._patch(url, data)

    def change_password(self, data):
        """
        ``PATCH /account/password``
        """
        url = f"{self._base_url}/password"
        return self._patch(url, data)
