"""
Module for Terraform Cloud API Endpoint: Applies.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCApplies(TFCEndpoint):
    """
    `Applies API Docs \
        <https://www.terraform.io/docs/cloud/api/applies.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/applies"

    def required_entitlements(self):
        return [Entitlements.OPERATIONS]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def show(self, apply_id):
        """
        ``GET /applies/:id``

        `Applies Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/applies.html#show-an-apply>`_
        """
        url = f"{self._endpoint_base_url}/{apply_id}"
        return self._show(url)

    def errored_state(self, apply_id):
        """
        ``GET /applies/:id/errored-state``

        `Applies Recover Failed State Upload API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies#recover-a-failed-state-upload-after-applying>`_
        """
        url = f"{self._endpoint_base_url}/{apply_id}/errored-state"
        return self._get(url)
