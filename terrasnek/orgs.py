"""
Module for Terraform Cloud API Endpoint: Orgs.
"""

from .endpoint import TFCEndpoint

class TFCOrgs(TFCEndpoint):
    """
    The Orgs API is used to list, show, create, update, and destroy organizations.

    https://www.terraform.io/docs/cloud/api/organizations.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._org_base_url = f"{base_url}/organizations"

    def create(self, payload):
        """
        POST /organizations
        """
        return self._create(self._org_base_url, payload)

    def destroy(self, org_name):
        """
        DELETE /organizations/:org_name
        """
        url = f"{self._org_base_url}/{org_name}"
        return self._destroy(url)

    def entitlements(self, org_name):
        """
        GET /organizations/:org_name/entitlement-set

        This endpoint shows the entitlements for an organization.
        """
        url = f"{self._org_base_url}/{org_name}/entitlement-set"
        return self._get(url)

    def list(self):
        """
        GET /organizations
        """
        return self._list(self._org_base_url)

    def show(self, org_name):
        """
        GET /organizations/:org_name
        """
        url = f"{self._org_base_url}/{org_name}"
        return self._show(url)

    def update(self, org_name, payload):
        """
        PATCH /organizations/:org_name
        """
        url = f"{self._org_base_url}/{org_name}"
        return self._update(url, payload)
