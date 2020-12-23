"""
Module for Terraform Cloud API Endpoint: SSH Keys.
"""

from .endpoint import TFCEndpoint

class TFCSSHKeys(TFCEndpoint):
    """
    `SSH Keys API Docs \
        <https://www.terraform.io/docs/cloud/api/ssh-keys.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/ssh-keys"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/ssh-keys"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/ssh-keys``

        `SSH Keys Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/ssh-keys.html#create-an-ssh-key>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/ssh-keys.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self):
        """
        ``GET /organizations/:organization_name/ssh-keys``

        `SSH Keys List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/ssh-keys.html#list-ssh-keys>`_
        """
        return self._list(self._org_api_v2_base_url)

    def show(self, ssh_key_id):
        """
        ``GET /ssh-keys/:ssh_key_id``

        `SSH Keys Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/ssh-keys.html#get-an-ssh-key>`_
        """
        url = f"{self._endpoint_base_url}/{ssh_key_id}"
        return self._show(url)

    def update(self, ssh_key_id, payload):
        """
        ``PATCH /ssh-keys/:ssh_key_id``

        `SSH Keys Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/ssh-keys.html#update-an-ssh-key>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/ssh-keys.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{ssh_key_id}"
        return self._update(url, payload)

    def destroy(self, ssh_key_id):
        """
        ``DELETE /ssh-keys/:ssh_key_id``

        `SSH Keys Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/ssh-keys.html#delete-an-ssh-key>`_
        """
        url = f"{self._endpoint_base_url}/{ssh_key_id}"
        return self._destroy(url)
