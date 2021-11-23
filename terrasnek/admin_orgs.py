"""
Module for Terraform Cloud API Endpoint: Admin Orgs.
"""

from .endpoint import TFCEndpoint

class TFCAdminOrgs(TFCEndpoint):
    """
    `Admin Orgs API Docs \
        <https://www.terraform.io/docs/cloud/api/admin/organizations.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/admin/organizations"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return True

    def destroy(self, org_name):
        """
        ``DELETE /admin/organizations/:name``

        `Admin Destroy Org API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#delete-an-organization>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._destroy(url)

    def list(self, include=None):
        """
        ``GET /api/v2/admin/organizations``

        `Admin List Orgs API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#list-all-organizations>`_

        This endpoint lists all organizations in the Terraform Cloud installation.
        """
        return self._list(self._org_api_v2_base_url, include=include)

    def list_org_module_consumers(self, org_name, page=None, page_size=None):
        """
        ``GET /api/v2/admin/organizations/:name/relationships/module-consumers``

        `Admin List Module Consumers for an Organization API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#list-module-consumers-for-an-organization>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#query-parameters-1>`__
        """
        url = f"{self._org_api_v2_base_url}/{org_name}/relationships/module-consumers"
        return self._list(url, page=page, page_size=page_size)

    def show(self, org_name, include=None):
        """
        ``GET /api/v2/admin/organizations/:name``

        `Admin Show Org API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#show-an-organization>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._show(url, include=include)

    def update(self, org_name, payload):
        """
        ``PATCH /admin/organizations/:name``

        `Admin Orgs Update API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#update-an-organization>`_

        `Update Sample Payload \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#sample-payload>`_
        """
        url = f"{self._org_api_v2_base_url}/{org_name}"
        return self._update(url, payload)

    def update_org_module_consumers(self, org_name, payload):
        """
        ``PATCH /admin/organizations/:name/relationships/module-consumers``

        `Admin Orgs Update Module Consumers API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#update-an-organization-39-s-module-consumers>`_

        `Update Org Module Consumers Sample Payload \
            <https://www.terraform.io/docs/cloud/api/admin/organizations.html#sample-payload-1>`_
        """

        url = f"{self._org_api_v2_base_url}/{org_name}/relationships/module-consumers"

        return self._update(url, payload)
