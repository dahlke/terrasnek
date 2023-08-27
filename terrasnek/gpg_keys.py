"""
Module for Terraform Cloud API Endpoint: GPG Keys.
"""

from .endpoint import TFCEndpoint

class TFCGPGKeys(TFCEndpoint):
    """
    `GPG Keys API Docs \
        <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        # NOTE: eventually, these should be configurable below, but today they are not to be changed.
        self._namespace = self._org_name
        self._registry_name = "private"
        self._gpg_keys_base_url = f"{self._instance_url}/api/registry/{self._registry_name}/v2/gpg-keys"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        # TODO: once it's released in TFE
        return False

    def create(self, payload):
        """
        ``POST /api/registry/:registry_name/v2/gpg-keys``

        `GPG Keys Create API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys#add-a-gpg-key>`_
        """
        return self._create(self._gpg_keys_base_url, payload)

    def list(self, page=None, page_size=None, filters=None):
        """
        ``GET /api/registry/:registry_name/v2/gpg-keys``

        `GPG Keys List API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys#list-gpg-keys>`_

        `Query Parameter(s) Details \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys#query-parameters>`__
        """
        if filters is None:
            filters = [
                {
                    "keys": ["namespace"],
                    "value": self._namespace
                }
            ]
        return self._list(self._gpg_keys_base_url, page=page, page_size=page_size, filters=filters)

    def list_all(self, filters=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every workspace in an organization.

        Returns an object with two arrays of objects.
        """
        if filters is None:
            filters = [
                {
                    "keys": ["namespace"],
                    "value": self._namespace
                }
            ]
        return self._list_all(self._gpg_keys_base_url, filters=filters)

    def show(self, key_id):
        """
        ``GET /api/registry/:registry_name/v2/gpg-keys/:namespace/:key_id``

        `GPG Keys Show API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys#get-gpg-key>`_
        """
        url = f"{self._gpg_keys_base_url}/{key_id}"
        return self._show(url)

    def update(self, key_id, payload=None):
        """
        ``PATCH /api/registry/:registry_name/v2/gpg-keys/:namespace/:key_id``

        `GPG Keys Update API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys#update-a-gpg-key>`_

        `Update Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys#sample-payload-1>`_
        """
        url = f"{self._gpg_keys_base_url}/v2/gpg-keys/{self._namespace}/{key_id}"
        return self._update(url, payload)

    def destroy(self, key_id):
        """
        ``DELETE /api/registry/:registry_name/v2/gpg-keys/:namespace/:key_id``

        `GPG Keys Destroy API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys#delete-a-gpg-key>`_
        """
        url = f"{self._gpg_keys_base_url}/{self._namespace}/{key_id}"
        return self._destroy(url)
