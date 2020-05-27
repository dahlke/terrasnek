"""
Module for Terraform Cloud API Endpoint: Orgs.
"""

from .endpoint import TFCEndpoint

class TFCOrgs(TFCEndpoint):
    """
    The Orgs API is used to list, show, create, update, and destroy organizations.

    https://www.terraform.io/docs/cloud/api/organizations.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations"

    def required_entitlements(self):
        return []

    def create(self, payload):
        """
        ``POST /organizations``
        """
        return self._create(self._org_api_v2_base_url, payload)

    def destroy(self, org_name):
        """
        ``DELETE /organizations/:organization_name``
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._destroy(url)

    def entitlements(self, org_name):
        """
        ``GET /organizations/:organization_name/entitlement-set``

        This endpoint shows the entitlements for an organization.
        """
        url = f"{self._org_api_v2_base_url}/{org_name}/entitlement-set"
        return self._get(url)

    def list(self):
        """
        ``GET /organizations``
        """
        return self._list(self._org_api_v2_base_url)

    def show(self, org_name):
        """
        ``GET /organizations/:organization_name``
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._show(url)

    def update(self, org_name, payload):
        """
        ``PATCH /organizations/:organization_name``
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._update(url, payload)
