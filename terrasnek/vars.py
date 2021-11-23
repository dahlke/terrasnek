"""
Module for Terraform Cloud API Endpoint: Variables.
"""

from .endpoint import TFCEndpoint

class TFCVars(TFCEndpoint):
    """
    `Vars API Docs \
        <https://www.terraform.io/docs/cloud/api/variables.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/vars"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /vars``

        `Vars Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variables.html#create-a-variable>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variables.html#sample-payload>`_
        """
        return self._create(self._endpoint_base_url, payload)

    def list(self, workspace_name=None):
        """
        ``GET /vars``

        `Vars List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variables.html#list-variables>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/variables.html#query-parameters>`__
        """
        url = f"{self._endpoint_base_url}?filter[organization][name]={self._org_name}"

        if workspace_name is not None:
            url += f"&filter[workspace][name]={workspace_name}"

        return self._list(url)

    def update(self, variable_id, payload):
        """
        ``PATCH /vars/:variable_id``

        `Vars Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variables.html#update-variables>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/variables.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{variable_id}"
        return self._update(url, payload)

    def destroy(self, variable_id):
        """
        ``DELETE /vars/:variable_id``

        `Vars Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/variables.html#delete-variables>`_
        """
        url = f"{self._endpoint_base_url}/{variable_id}"
        return self._destroy(url)
