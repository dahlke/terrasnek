"""
Module for Terraform Cloud API Endpoint: State Version Outputs.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCStateVersionOutputs(TFCEndpoint):
    """
    State version outputs are the output values from a Terraform state file. They include the
    name and value of the output, as well as a sensitive boolean if the value should be hidden
    by default in UIs.

    https://www.terraform.io/docs/cloud/api/state-version-outputs.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/state-version-outputs"

    def required_entitlements(self):
        return [Entitlements.STATE_STORAGE]

    def show(self, state_version_output_id):
        """
        ``GET /state-version-outputs/:state_version_output_id``

        State version output IDs must be obtained from a state version object. When requesting a
        state version, you can optionally add ?include=outputs to include full details for all of
        that state version's outputs.
        """
        url = f"{self._endpoint_base_url}/{state_version_output_id}"
        return self._show(url)
