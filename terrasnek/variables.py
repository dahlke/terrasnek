"""
Module for Terraform Cloud API Endpoint: Variables.
"""

from .endpoint import TFCEndpoint

class TFCVariables(TFCEndpoint):
    """
    This set of APIs covers create, update, list and delete operations on variables.

    https://www.terraform.io/docs/cloud/api/variables.html
    """
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._base_url = f"{base_url}/vars"

    def create(self, payload):
        """
        POST /vars
        """
        return self._create(self._base_url, payload)

    def lst(self, workspace_name=None):
        """
        GET /vars
        """
        url = f"{self._base_url}?filter[organization][name]={self._organization_name}"

        if workspace_name is not None:
            url += f"&filter[workspace][name]={workspace_name}"

        return self._ls(url)

    def update(self, variable_id, payload):
        """
        PATCH /vars/:variable_id
        """
        url = f"{self._base_url}/{variable_id}"
        return self._update(url, payload)

    def destroy(self, variable_id):
        """
        DELETE /vars/:variable_id
        """
        url = f"{self._base_url}/{variable_id}"
        return self._destroy(url)
