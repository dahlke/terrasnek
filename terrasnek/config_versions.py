"""
Module for Terraform Cloud API Endpoint: Config Versions.
"""

from .endpoint import TFCEndpoint

class TFCConfigVersions(TFCEndpoint):
    """
    A configuration version a resource used to reference the uploaded
    configuration files. It is associated with the run to use the uploaded
    configuration files for performing the plan and apply.

    https://www.terraform.io/docs/cloud/api/configuration-versions.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"
        self._config_version_api_v2_base_url = f"{self._api_v2_base_url}/configuration-versions"

    def required_entitlements(self):
        return []

    def list(self, workspace_id, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/configuration-versions``
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/configuration-versions"
        return self._list(url, page=page, page_size=page_size)

    def show(self, config_version_id):
        """
        ``GET /configuration-versions/:configuration-id``
        """
        url = f"{self._config_version_api_v2_base_url}/{config_version_id}"
        return self._show(url)

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/configuration-versions``

        This POST endpoint requires a JSON object with the following properties as a request
        payload.

        Properties without a default value are required.
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/configuration-versions"
        return self._create(url, payload)

    def upload(self, path_to_tarball, config_version_id):
        """
        ``PUT https://archivist.terraform.io/v1/object/<UNIQUE OBJECT ID>``

        The above URL is derived.
        """
        url = self.show(config_version_id)["data"]["attributes"]["upload-url"]
        data = None

        with open(path_to_tarball, 'rb') as data_bytes:
            data = data_bytes.read()

        return self._put(url, data=data)
