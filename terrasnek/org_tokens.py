"""
Module for Terraform Cloud API Endpoint: Org Tokens.
"""

from .endpoint import TFCEndpoint

class TFCOrgTokens(TFCEndpoint):
    """
    `Org Tokens API Docs \
        <https://www.terraform.io/docs/cloud/api/organization-tokens.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/authentication-token"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self):
        """
        ``POST /organizations/:organization_name/authentication-token``

        `Org Tokens Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tokens.html#generate-a-new-organization-token>`_
        """
        return self._create(self._endpoint_base_url, None)

    def destroy(self):
        """
        ``DELETE /organizations/:organization/authentication-token``

        `Org Tokens Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tokens.html#delete-the-organization-token>`_
        """
        url = f"{self._endpoint_base_url}"
        return self._destroy(url)
