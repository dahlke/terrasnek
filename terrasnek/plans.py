"""
Module for Terraform Cloud API Endpoint: Plans.
"""

from .endpoint import TFCEndpoint
from._constants import Entitlements

class TFCPlans(TFCEndpoint):
    """
    A plan represents the execution plan of a Run in a Terraform workspace.

    https://www.terraform.io/docs/cloud/api/plans.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/plans"
        self._runs_base_url = f"{self._api_v2_base_url}/runs"

    def required_entitlements(self):
        return [Entitlements.OPERATIONS]

    def show(self, plan_id):
        """
        ``GET /plans/:id``

        Show the plan by it's ID. There is no endpoint to list plans. You can find the ID for
        a plan in the relationships.plan property of a run object.
        """
        url = f"{self._endpoint_base_url}/{plan_id}"
        return self._show(url)

    def download_json(self, target_path, plan_id=None, run_id=None):
        """
        ``GET [TODO: does not yet work] /plans/:id/json-output``
        ``GET /runs/:id/plan/json-output``

        Show the plan in JSON format, by either the plan ID itself, or through the run itself.

        These endpoints generate a temporary authenticated URL to the location of the JSON
        formatted execution plan. When successful, this endpoint responds with a temporary
        redirect that should be followed.

        If using a client that can follow redirects, you can use this endpoint to save
        the .json file locally without needing to save the temporary URL.

        This temporary URL provided by the redirect has a life of 1 minute, and should not be
        relied upon beyond the initial request. If you need repeat access, you should use
        this endpoint to generate a new URL each time.
        """
        if plan_id is not None:
            url = f"{self._endpoint_base_url}/{plan_id}/json-output"
            self._logger.error(f"This endpoint ({url}) does not yet work.")
        elif run_id is not None:
            url = f"{self._runs_base_url}/{run_id}/plan/json-output"
        else:
            self._logger.error("Arguments plan_id or run_id must be defined")

        results = self._get(url, return_raw=True, allow_redirects=True)

        with open(target_path, 'wb') as target_file:
            target_file.write(results)
