"""
Module for Terraform Cloud API Endpoint: Account.
"""

from .endpoint import TFCEndpoint

class TFCAccount(TFCEndpoint):
    """
    `API Docs \
        <https://www.terraform.io/docs/cloud/api/account.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/account"

    def required_entitlements(self):
        return []

    def show(self):
        """
        ``GET /account/details``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/account.html#get-your-account-details>`_
        """
        url = f"{self._endpoint_base_url}/details"
        return self._show(url)

    def update(self, payload):
        """
        ``PATCH /account/update``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/account.html#update-your-account-info>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/account.html#sample-payload>`_
        """
        url = f"{self._endpoint_base_url}/update"
        return self._patch(url, payload)

    def change_password(self, data):
        """
        ``PATCH /account/password``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/account.html#change-your-password>`_

        `Sample Payload \
            <https://www.terraform.io/docs/cloud/api/account.html#sample-payload>`_
        """
        url = f"{self._endpoint_base_url}/password"
        return self._patch(url, data)
