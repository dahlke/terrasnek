"""
Module for Terraform Cloud API Endpoint: State Version Outputs.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCStateVersionOutputs(TFCEndpoint):
    """
    `State Version Outputs API Docs \
        <https://www.terraform.io/docs/cloud/api/state-version-outputs.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/state-version-outputs"

    def _required_entitlements(self):
        return [Entitlements.STATE_STORAGE]

    def show(self, state_version_output_id):
        """
        ``GET /state-version-outputs/:state_version_output_id``

        `State Version Outputs Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/state-version-outputs.html#show-a-state-version-output>`_
        """
        url = f"{self._endpoint_base_url}/{state_version_output_id}"
        return self._show(url)
