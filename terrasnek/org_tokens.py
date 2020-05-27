"""
Module for Terraform Cloud API Endpoint: Org Tokens.
"""

from .endpoint import TFCEndpoint

class TFCOrgTokens(TFCEndpoint):
    """
    The Org Tokens API is used to generate and revoke Org
    tokens. Each organization can only have one token.

    https://www.terraform.io/docs/cloud/api/organization-tokens.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/authentication-token"

    def required_entitlements(self):
        return []

    def create(self):
        """
        ``POST /organizations/:organization_name/authentication-token``

        This endpoint creates an org token for the active org.
        """
        return self._create(self._endpoint_base_url, None)

    def destroy(self):
        """
        ``DELETE /organizations/:organization/authentication-token``

        This endpoint deletes the org token for the active org.
        """
        url = f"{self._endpoint_base_url}"
        return self._destroy(url)
