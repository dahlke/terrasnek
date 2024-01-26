"""
Module for Terraform Cloud API Endpoint: Registry Modules.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements


class TFCRegistryModules(TFCEndpoint):
    """
    `Registry Modules API Docs (Private Registry) \
        <https://www.terraform.io/docs/cloud/api/modules.html>`_

    `Registry Modules API Docs (Public Registry) \
        <https://www.terraform.io/docs/registry/api.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        # Helper vars to help clarify how the URLs translate to docs below
        self._namespace = self._org_name
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations"
        self._mods_v2_base_url = f"{self._org_api_v2_base_url}/{self._org_name}/registry-modules"
        """
        https://app.terraform.io/api/registry/v1/modules/terrasnek-unittest/terrasnek-unittest/tfe/versions
        True
        /api/v2/organizations/terrasnek-unittest/registry-modules/private/terrasnek-unittest/terrasnek-unittest/tfe
        {self._org_api_v2_base_url}/{reg_name}/{self._org_name}/{MOD NAME}/{PROVIDER}
        """

    def required_entitlements(self):
        return [Entitlements.PRIVATE_MODULE_REGISTRY]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    # Public Registry API Endpoints
    def list(self, offset=None, page=None, page_size=None, limit=None, \
        provider=None, verified=None, filters=None):
        """
        ``GET /organizations/:organization_name/registry-modules``

        `Registry Modules List API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#list-modules>`_

        `Query Parameter(s) Details \
            <https://www.terraform.io/docs/cloud/api/modules.html#query-parameters>`__
        """
        return self._list(\
            self._mods_v2_base_url, page=page, page_size=page_size, offset=offset, \
                limit=limit, provider=provider, verified=verified, filters=filters)

    def list_all(self):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every audit trail in an organization.

        Returns an object with two arrays of objects.
        """
        return self._list_all(self._mods_v2_base_url)


    def search(self, query, offset=None, limit=None, provider=None, verified=None):
        """
        ``GET <base_url>/search``

        `Registry Modules Search API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#search-modules>`_
        """
        url = f"{self._mods_v1_base_url}/search"
        return self._list(url, \
            query=query, offset=offset, limit=limit, provider=provider,\
            verified=verified)

    def show(self, module_name, provider, reg_name="private"):
        """
        ``GET /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider``

        **NOTE: Deprecated**
        ``GET /registry-modules/show/:organization_name/:name/:provider``

        `Registry Modules Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#show-a-module>`_
        """
        # NOTE: Future - this may be modded to support non-private registries.
        # NOTE: File a GH issue if you need non-private registry support.
        url = f"{self._mods_v2_base_url}/{reg_name}/{self._namespace}/{module_name}/{provider}"

        return self._show(url)

    def list_versions(self, name, provider): # reg_name="private"
        """
        ``GET <base_url>/:namespace/:name/:provider/versions``

        `Registry Modules List Versions API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#list-available-versions-for-a-specific-module>`_
        """
        url = f"{self._mods_v1_base_url}/{self._org_name}/{name}/{provider}/versions"
        return self._get(url)

    def list_latest_version_all_providers(self, name, offset=None, limit=None):
        """
        ``GET <base_url>/:namespace/:name``

        `Registry Modules List Latest Version All Providers API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#list-latest-version-of-module-for-all-providers>`_
        """
        url = f"{self._mods_v1_base_url}/{self._org_name}/{name}"
        return self._list(url, offset=offset, limit=limit)

    def list_latest_version_specific_provider(self, name, provider):
        """
        ``GET <base_url>/:namespace/:name/:provider``

        `Registry Modules List Latest Version Specific Provider API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#latest-version-for-a-specific-module-provider>`_
        """
        url = f"{self._mods_v1_base_url}/{self._org_name}/{name}/{provider}"
        return self._get(url)

    def get(self, name, provider, version):
        """
        ``GET <base_url>/:namespace/:name/:provider/:version``

        `Registry Modules Get API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#get-a-specific-module>`_
        """
        url = f"{self._mods_v1_base_url}/{self._org_name}/{name}/{provider}/{version}"
        return self._get(url)

    def download_version_source(self, name, provider, version, target_path):
        """
        ``GET <base_url>/:namespace/:name/:provider/:version/download``

        `Registry Modules Download Version Source API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#download-source-code-for-a-specific-module-version>`_
        """
        url = f"{self._mods_v1_base_url}/{self._org_name}/{name}/{provider}/{version}/download"
        return self._download(url, target_path, header_with_url="X-Terraform-Get")

    def download_latest_source(self, name, provider, target_path):
        """
        ``GET <base_url>/:namespace/:name/:provider/download``

        `Registry Modules Download Latest Source API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#download-the-latest-version-of-a-module>`_
        """
        url = f"{self._mods_v1_base_url}/{self._org_name}/{name}/{provider}/download"
        return self._download(\
            url, target_path, header_with_url="X-Terraform-Get", allow_redirects=True)

    # Private Registry API Endpoints
    def publish_from_vcs(self, payload):
        """
        ``POST /organizations/:organization_name/registry-modules/vcs``

        `Registry Modules Publish a Private Module From VCS API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#publish-a-private-module-from-a-vcs>`_

        `Publish From VCS Sample Payload \
            <https://www.terraform.io/docs/cloud/api/modules.html#sample-payload>`_
        """
        with_vcs_url = f"{self._mods_v2_base_url}/vcs"
        return self._post(with_vcs_url, data=payload)

    def destroy(self, module_name, reg_name="private", provider=None, version=None):
        """
        ``DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider/:version``
        ``DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider``
        ``DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name``

        **NOTE: Deprecated**
        ``POST /registry-modules/actions/delete/:organization_name/:name/:provider/:version``
        ``POST /registry-modules/actions/delete/:organization_name/:name/:provider``
        ``POST /registry-modules/actions/delete/:organization_name/:name``

        `Registry Modules Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#delete-a-module>`_
        """
        # NOTE: Namespace param is the org name for a private registry, and we only support private registries (for now)
        url = f"{self._mods_v2_base_url}/{reg_name}/{self._namespace}/{module_name}/"

        if provider:
            url += f"/{provider}"
            if version:
                url += f"/{version}"

        return self._destroy(url)

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/registry-modules``

        `Registry Modules Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#create-a-module>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/modules.html#request-body-1>`_
        """

        url = f"{self._org_api_v2_base_url}/{self._org_name}/registry-modules"
        return self._post(url, data=payload)

    def update(self, module_name, provider, payload, reg_name="private"):
        """
        ``PATCH /organizations/:organization_name/registry-modules/private/:namespace/:name/:provider/``

        `Registry Modules Update API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/modules#update-a-private-registry-module>`_

        `Update Sample Payload \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/modules#sample-payload-2>`_
        """

        url = f"{self._mods_v2_base_url}/{reg_name}/{self._namespace}/{module_name}/{provider}"
        return self._patch(url, data=payload)

    def create_version(self, module_name, provider, payload, reg_name="private"):
        """
        ``POST /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider/versions``

        `Registry Modules Create Version API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#create-a-module-version>`_

        `Create Version Sample Payload \
            <https://www.terraform.io/docs/cloud/api/modules.html#request-body-2>`_
        """
        # NOTE: In the future, this may be modified to support non-private registries. File an issue if you need this.
        url = f"{self._mods_v2_base_url}/{reg_name}/{self._namespace}/{module_name}/{provider}/versions"
        return self._post(url, data=payload)

    def upload_version(self, path_to_tarball, upload_url):
        """
        ``PUT https://archivist.terraform.io/v1/object/<UNIQUE OBJECT ID>``

        `Registry Modules Upload Version API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#upload-a-module-version>`_
        """
        data = None

        with open(path_to_tarball, 'rb') as data_bytes:
            data = data_bytes.read()

        return self._put(upload_url, data=data)
