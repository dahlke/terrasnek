"""
Module for Terraform Cloud API Endpoint: Config Versions.
"""

from .endpoint import TFCEndpoint

class TFCConfigVersions(TFCEndpoint):
    """
    `Config Versions API Docs \
        <https://www.terraform.io/docs/cloud/api/configuration-versions.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"
        self._config_version_api_v2_base_url = f"{self._api_v2_base_url}/configuration-versions"

    def _required_entitlements(self):
        return []

    def list(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/configuration-versions``

        `Config Versions List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/configuration-versions.html#list-configuration-versions>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/configuration-versions.html#query-parameters>`_):
            - ``since`` (Optional)
            - ``page`` (Optional)
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/configuration-versions"
        return self._list(url, page=page, page_size=page_size)

    def show(self, config_version_id):
        """
        ``GET /configuration-versions/:configuration-id``

        `Config Versions Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/configuration-versions.html#show-a-configuration-version>`_
        """
        url = f"{self._config_version_api_v2_base_url}/{config_version_id}"
        return self._show(url)

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/configuration-versions``

        `Config Versions Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/configuration-versions.html#create-a-configuration-version>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/configuration-versions.html#sample-payload>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/configuration-versions"
        return self._create(url, payload)

    def upload(self, path_to_tarball, upload_url):
        """
        ``PUT https://archivist.terraform.io/v1/object/<UNIQUE OBJECT ID>``

        `Config Versions Upload API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/configuration-versions.html#upload-configuration-files>`_
        """
        data = None

        with open(path_to_tarball, 'rb') as data_bytes:
            data = data_bytes.read()

        return self._put(upload_url, data=data)
