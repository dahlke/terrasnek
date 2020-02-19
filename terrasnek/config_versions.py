"""
Module for Terraform Cloud API Endpoint: Config Versions.
"""

import json
import requests

from .endpoint import TFCEndpoint

class TFCConfigVersions(TFCEndpoint):
    """
    A configuration version (configuration-version) is a resource used to reference the
    uploaded configuration files. It is associated with the run to use the uploaded configuration
    files for performing the plan and apply.

    https://www.terraform.io/docs/cloud/api/configuration-versions.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._ws_base_url = f"{base_url}/workspaces"
        self._config_version_base_url = f"{base_url}/configuration-versions"

    def lst(self, workspace_id, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/configuration-versions

        This endpoint supports pagination with standard URL query parameters; remember to
        percent-encode.
        """
        url = f"{self._ws_base_url}/{workspace_id}/configuration-versions"

        filters = []
        if page_number is not None:
            filters.append(f"page[number]={page_number}")

        if page_size is not None:
            filters.append(f"page[size]={page_size}")

        if filters:
            url += "?" + "&".join(filters)

        return self._ls(url)

    def show(self, config_version_id):
        """
        GET /configuration-versions/:configuration-config_version_id
        """
        url = f"{self._config_version_base_url}/{config_version_id}"
        return self._show(url)

    def create(self, workspace_id, payload):
        """
        POST /workspaces/:workspace_id/configuration-versions

        This POST endpoint requires a JSON object with the following properties as a request
        payload.

        Properties without a default value are required.
        """
        url = f"{self._ws_base_url}/{workspace_id}/configuration-versions"
        return self._create(url, payload)

    def upload(self, path_to_tarball, config_version_id):
        """
        PUT {derived_config_version_upload_url}
        """
        results = None
        # TODO: Validate the path to tarball a bit
        upload_url = self.show(config_version_id)["data"]["attributes"]["upload-url"]

        # TODO: Exception and error handling
        req = None
        with open(path_to_tarball, 'rb') as data:
            req = requests.put(upload_url, data=data, headers=self._headers)

        if req.status_code == 200:
            self._logger.debug("Config version successfully uploaded.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results
