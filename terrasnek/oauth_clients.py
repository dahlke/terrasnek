"""
Module for Terraform Cloud API Endpoint: OAuth Clients.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCOAuthClients(TFCEndpoint):
    """
    An OAuth Client represents the connection between an organization and a VCS provider.

    https://www.terraform.io/docs/cloud/api/oauth-clients.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_api_v2_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/oauth-clients"
        self._oauth_clients_api_v2_base_url = f"{self._api_v2_base_url}/oauth-clients"

    def required_entitlements(self):
        return [Entitlements.VCS_INTEGRATIONS]

    def list(self):
        """
        ``GET /organizations/:organization_name/oauth-clients``

        This endpoint allows you to list VCS connections between an organization and a VCS
        provider (GitHub, Bitbucket, or GitLab) for use when creating or setting up workspaces.
        """
        return self._list(self._org_api_v2_base_url)

    def show(self, client_id):
        """
        ``GET /oauth-clients/:id``
        """
        url = f"{self._oauth_clients_api_v2_base_url}/{client_id}"
        return self._show(url)

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/oauth-clients``

        This endpoint allows you to create a VCS connection between an organization and a VCS
        provider (GitHub or GitLab) for use when creating or setting up workspaces. By using
        this API endpoint, you can provide a pre-generated OAuth token string instead of going
        through the process of creating a GitHub or GitLab OAuth Application.
        """
        return self._create(self._org_api_v2_base_url, payload)

    def update(self, client_id, payload):
        """
        ``PATCH /oauth-clients/:id``

        Use caution when changing attributes with this endpoint; editing an OAuth client that
        workspaces are currently using can have unexpected effects.
        """
        url = f"{self._oauth_clients_api_v2_base_url}/{client_id}"
        return self._update(url, payload)

    def destroy(self, client_id):
        """
        ``DELETE /oauth-clients/:id``

        This endpoint allows you to remove an existing connection between an organization and a
        VCS provider (GitHub, Bitbucket, or GitLab).

        Note: Removing the OAuth Client will unlink workspaces that use this connection
        from their repositories, and these workspaces will need to be manually linked to
        another repository.
        """
        url = f"{self._oauth_clients_api_v2_base_url}/{client_id}"
        return self._destroy(url)
