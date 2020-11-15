"""
Module for Terraform Cloud API Endpoint: Orgs.
"""

from .endpoint import TFCEndpoint

class TFCOrgs(TFCEndpoint):
    """
    `Orgs API Docs \
        <https://www.terraform.io/docs/cloud/api/organizations.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations"

    def _required_entitlements(self):
        return []

    def create(self, payload):
        """
        ``POST /organizations``

        `Orgs Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organizations.html#create-an-organization>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/organizations.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def destroy(self, org_name):
        """
        ``DELETE /organizations/:organization_name``

        `Orgs Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organizations.html#destroy-an-organization>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._destroy(url)

    def entitlements(self, org_name):
        """
        ``GET /organizations/:organization_name/entitlement-set``

        `Orgs Entitlements API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organizations.html#show-the-entitlement-set>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}/entitlement-set"
        return self._get(url)

    def list(self):
        """
        ``GET /organizations``

        `Orgs List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organizations.html#list-organizations>`_
        """
        return self._list(self._org_api_v2_base_url)

    def show(self, org_name):
        """
        ``GET /organizations/:organization_name``

        `Orgs Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organizations.html#show-an-organization>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._show(url)

    def update(self, org_name, payload):
        """
        ``PATCH /organizations/:organization_name``

        `Orgs Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organizations.html#update-an-organization>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/organizations.html#sample-payload-1>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._update(url, payload)
