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
        return True

    def terraform_enterprise_only(self):
        # TODO: Change this once it's released for TFE
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
