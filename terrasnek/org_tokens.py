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

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/organizations/{org_name}/authentication-token"

    def create(self):
        """
        POST /organizations/:org_name/authentication-token

        This endpoint creates an org token for the active org.
        """
        return self._create(self._base_url, None)

    def destroy(self):
        """
        DELETE /organizations/:organization/authentication-token

        This endpoint deletes the org token for the active org.
        """
        url = f"{self._base_url}"
        return self._destroy(url)
