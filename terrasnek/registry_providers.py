"""
Module for Terraform Cloud API Endpoint: Registry Providers.
"""

from .endpoint import TFCEndpoint

class TFCRegistryProviders(TFCEndpoint):
    """
    `Registry Providers API Docs \
        <https://www.terraform.io/docs/cloud/api/providers.html>`_
    """
    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_providers_base_url = f"{self._api_v2_base_url}/organizations/{self._org_name}/registry-providers"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/registry-providers``

        `Registry Providers Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/providers.html#create-a-provider>`_

        `Registry Providers Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/providers.html#sample-payload-public-provider->`_
        """
        return self._create(self._org_providers_base_url, payload)


    def list(self, page=None, page_size=None, filters=None):
        """
        ``GET /organizations/:organization_name/registry-providers``

        `Registry Providers List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/providers.html#list-public-terraform-registry-providers-for-an-organization>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/providers.html#query-parameters>`__
        """
        return self._list(self._org_providers_base_url, page=page, page_size=page_size, filters=filters)

    def list_all(self):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every run trigger for a workspace.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._org_providers_base_url)

    def show(self, registry_name, namespace, name):
        """
        ``GET /organizations/:organization_name/registry-providers/:registry_name/:namespace/:name``

        `Registry Providers Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/providers.html#get-a-provider>`_
        """
        url = f"{self._org_providers_base_url}/{registry_name}/{namespace}/{name}"
        return self._show(url)

    def destroy(self, registry_name, namespace, name):
        """
        ``DELETE /organizations/:organization_name/registry-providers/:registry_name/:namespace/:name``

        `Registry Providers Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/providers.html#delete-a-provider>`_
        """
        url = f"{self._org_providers_base_url}/{registry_name}/{namespace}/{name}"
        return self._destroy(url)
