"""
Module for Terraform Cloud API Endpoint: Plans.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPlans(TFCEndpoint):
    """
    `Plans API Docs \
        <https://www.terraform.io/docs/cloud/api/plans.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/plans"
        self._runs_base_url = f"{self._api_v2_base_url}/runs"

    def required_entitlements(self):
        return [Entitlements.OPERATIONS]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def show(self, plan_id):
        """
        ``GET /plans/:id``

        `Plans Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/plans.html#show-a-plan>`_
        """
        url = f"{self._endpoint_base_url}/{plan_id}"
        return self._show(url)

    def download_json(self, target_path, plan_id=None, run_id=None):
        """
        ``GET /plans/:id/json-output``
        ``GET /runs/:id/plan/json-output``

        `Plans Download JSON API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/plans.html#retrieve-the-json-execution-plan>`_
        """
        if plan_id is not None:
            url = f"{self._endpoint_base_url}/{plan_id}/json-output"
        elif run_id is not None:
            url = f"{self._runs_base_url}/{run_id}/plan/json-output"
        else:
            self._logger.error("Arguments plan_id or run_id must be defined")

        results = self._get(url, return_raw=True, allow_redirects=True)

        with open(target_path, 'wb') as target_file:
            target_file.write(results)
