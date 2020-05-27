"""
Module for Terraform Cloud API Endpoint: SSH Keys.
"""

from .endpoint import TFCEndpoint

class TFCSSHKeys(TFCEndpoint):
    """
    The ssh-key object represents an SSH key which includes a name and the SSH
    private key. An organization can have multiple SSH keys available.

    SSH keys can be used in two places:

        They can be assigned to VCS provider integrations (available in the
        API as oauth-tokens). Bitbucket Server requires an SSH key; other
        providers only need an SSH key if your repositories include submodules
        that are only accessible via SSH (instead of your VCS provider's API).

        They can be assigned to workspaces and used when Terraform needs to
        clone modules from a Git server. This is only necessary when your
        configurations directly reference modules from a Git server; you do
        not need to do this if you use Terraform Cloud's private module
        registry.

        https://www.terraform.io/docs/cloud/api/ssh-keys.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/ssh-keys"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/ssh-keys"

    def required_entitlements(self):
        return []

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/ssh-keys``
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self):
        """
        ``GET /organizations/:organization_name/ssh-keys``
        """
        return self._list(self._org_api_v2_base_url)

    def show(self, ssh_key_id):
        """
        ``GET /ssh-keys/:ssh_key_id``
        """
        url = f"{self._endpoint_base_url}/{ssh_key_id}"
        return self._show(url)

    def update(self, ssh_key_id, payload):
        """
        ``PATCH /ssh-keys/:ssh_key_id``
        """
        url = f"{self._endpoint_base_url}/{ssh_key_id}"
        return self._update(url, payload)

    def destroy(self, ssh_key_id):
        """
        ``DELETE /ssh-keys/:ssh_key_id``
        """
        url = f"{self._endpoint_base_url}/{ssh_key_id}"
        return self._destroy(url)
