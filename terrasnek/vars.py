"""
Module for Terraform Cloud API Endpoint: Variables.
"""

from .endpoint import TFCEndpoint

class TFCVars(TFCEndpoint):
    """
    This set of APIs covers create, update, list and delete operations on variables.

    https://www.terraform.io/docs/cloud/api/variables.html
    """

    def __init__(self, instance_url, org_name, headers, verify):
        super().__init__(instance_url, org_name, headers, verify)
        self._api_v2_base_url = f"{self._api_v2_base_url}/vars"

    def required_entitlements(self):
        return []

    def create(self, payload):
        """
        ``POST /vars``
        """
        return self._create(self._api_v2_base_url, payload)

    def list(self, workspace_name=None):
        """
        ``GET /vars``
        """
        url = f"{self._api_v2_base_url}?filter[organization][name]={self._org_name}"

        if workspace_name is not None:
            url += f"&filter[workspace][name]={workspace_name}"

        return self._list(url)

    def update(self, variable_id, payload):
        """
        ``PATCH /vars/:variable_id``
        """
        url = f"{self._api_v2_base_url}/{variable_id}"
        return self._update(url, payload)

    def destroy(self, variable_id):
        """
        ``DELETE /vars/:variable_id``
        """
        url = f"{self._api_v2_base_url}/{variable_id}"
        return self._destroy(url)
