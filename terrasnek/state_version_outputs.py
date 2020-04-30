"""
Module for Terraform Cloud API Endpoint: State Version Outputs.
"""

from .endpoint import TFCEndpoint

class TFCStateVersionOutputs(TFCEndpoint):
    """
    State version outputs are the output values from a Terraform state file. They include the
    name and value of the output, as well as a sensitive boolean if the value should be hidden
    by default in UIs.

    https://www.terraform.io/docs/cloud/api/state-version-outputs.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/state-version-outputs"

    def show(self, state_version_output_id):
        """
        GET /state-version-outputs/:state_version_output_id

        State version output IDs must be obtained from a state version object. When requesting a
        state version, you can optionally add ?include=outputs to include full details for all of
        that state version's outputs.
        """
        url = f"{self._base_url}/{state_version_output_id}"
        return self._show(url)
