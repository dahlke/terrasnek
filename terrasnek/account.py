"""
Module for Terraform Cloud API Endpoint: Account.
"""

from .endpoint import TFCEndpoint

class TFCAccount(TFCEndpoint):
    """
    `Account API Docs \
        <https://www.terraform.io/docs/cloud/api/account.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/account"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def show(self):
        """
        ``GET /account/details``

        `Show Account API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/account.html#get-your-account-details>`_
        """
        url = f"{self._endpoint_base_url}/details"
        return self._show(url)

    def update(self, payload):
        """
        ``PATCH /account/update``

        `Update Account API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/account.html#update-your-account-info>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/account.html#sample-payload>`_
        """
        url = f"{self._endpoint_base_url}/update"
        return self._patch(url, payload)

    def change_password(self, data):
        """
        ``PATCH /account/password``

        `Change Account Password API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/account.html#change-your-password>`_

        `Change Password Sample Payload \
            <https://www.terraform.io/docs/cloud/api/account.html#sample-payload>`_
        """
        url = f"{self._endpoint_base_url}/password"
        return self._patch(url, data)
