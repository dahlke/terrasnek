"""
Module for Terraform Cloud API Endpoint: Workspace Variables.
"""

from .endpoint import TFCEndpoint

class TFCWorkspaceVars(TFCEndpoint):
    """
    `Workspace Vars API Docs \
        <https://www.terraform.io/docs/cloud/api/workspace-variables.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/vars``

        `Workspace Vars Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspace-variables.html#create-a-variable>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspace-variables.html#sample-payload>`_
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/"
        return self._create(url, payload)

    def list(self, workspace_id):
        """
        ``GET /workspaces/:workspace_id/vars``

        `Workspace Vars List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspace-variables.html#list-variables>`_
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/"
        return self._list(url)

    def update(self, workspace_id, variable_id, payload):
        """
        ``PATCH /workspaces/:workspace_id/vars/:variable_id``

        `Workspace Vars Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspace-variables.html#update-variables>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/workspace-variables.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/{variable_id}"
        return self._update(url, payload)

    def destroy(self, workspace_id, variable_id):
        """
        ``DELETE /workspaces/:workspace_id/vars/:variable_id``

        `Workspace Vars Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/workspace-variables.html#delete-variables>`_
        """
        url = f"{self._endpoint_base_url}/{workspace_id}/vars/{variable_id}"
        return self._destroy(url)
