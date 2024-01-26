"""
Module for Terraform Cloud API Endpoint: No Code Provisioning.
"""

from .endpoint import TFCEndpoint


class TFCNoCodeProvisioning(TFCEndpoint):
    """
    `No Code Provisioning API Docs \
        <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers,
                         well_known_paths, verify, log_level)
        self._org_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/no-code-modules"
        self._no_code_base_url = \
            f"{self._api_v2_base_url}/no-code-modules"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def enable(self, payload):
        """
        ``POST /organizations/:organization_name/no-code-modules``

        `No Code Provisioning Enable API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#allow-no-code-provisioning-of-a-module-within-an-organization>`_

        `Enable Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#sample-payload>`_
        """
        return self._post(self._org_base_url, data=payload)

    def update(self, module_id, payload):
        """
        ``PATCH /no-code-modules/:id``

        `No Code Modules Update API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#update-no-code-provisioning-settings-for-a-module>`_

        `Update Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#sample-payload-1>`_
        """
        url = f"{self._no_code_base_url}/{module_id}"
        return self._patch(url, payload)

    def show(self, module_id):
        """
        ``GET /no-code-modules/:id``

        `No Code Modules Read Properties API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#read-a-no-code-module-s-properties>`_
        """
        url = f"{self._no_code_base_url}/{module_id}"
        return self._show(url)

    def deploy(self, module_id, payload):
        """
        ``POST /no-code-modules/:id/workspaces``

        `No Code Modules Create Workspace and Deploy Resources API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#create-a-workspace-and-deploy-resources>`_

        `Deploy Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#sample-payload-2>`_
        """
        url = f"{self._no_code_base_url}/{module_id}/workspaces"
        return self._post(url, data=payload)

    def update_settings_upgrade(self, module_id, workspace_id, payload):
        """
        ``POST /no-code-modules/:no_code_module_id/workspaces/:id``

        `No Code Module Update Settings for Upgrade API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#initiate-a-workspace-update-to-new-no-code-provisioning-settings>`_

        `Update Settings and Upgrade Sample Payload \
        <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#sample-payload-3>`_
        """
        url = f"{self._org_base_url}/{module_id}/workspaces/{workspace_id}"
        return self._post(url, data=payload)

    def read_upgrade_status(self, module_id, workspace_id, upgrade_id):
        """
        ``GET /no-code-modules/:no_code_module_id/workspaces/:workspace_id/upgrade/:id``

        `No Code Modules Read Upgrade Status API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#read-workspace-upgrade-plan-status>`_
        """
        url = f"{self._org_base_url}/{module_id}/workspaces/{workspace_id}/upgrade/{upgrade_id}"
        return self._get(url)

    def confirm_apply_upgrade(self, module_id, workspace_id, upgrade_id):
        """
        ``POST /no-code-modules/:no_code_module_id/workspaces/:workspace_id/upgrade/:id``

        `No Code Modules Confirm Apply and Upgrade API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/no-code-provisioning#confirm-and-apply-a-workspace-upgrade-plan>`_
        """
        url = f"{self._org_base_url}/{module_id}/workspaces/{workspace_id}/upgrade/{upgrade_id}"
        return self._post(url)
