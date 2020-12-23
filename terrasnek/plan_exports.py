"""
Module for Terraform Cloud API Endpoint: Plan Exports.
"""

from .endpoint import TFCEndpoint

class TFCPlanExports(TFCEndpoint):
    """
    `Plan Exports API Docs \
        <https://www.terraform.io/docs/cloud/api/plan-exports.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/plan-exports"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, payload):
        """
        ``POST /plan-exports``

        `Plan Exports Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/plan-exports.html#create-a-plan-export>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/plan-exports.html#sample-payload>`_
        """

        return self._create(self._endpoint_base_url, payload)

    def show(self, plan_export_id):
        """
        ``GET /plan-exports/:id``

        `Plan Exports Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/plan-exports.html#show-a-plan-export>`_
        """
        url = f"{self._endpoint_base_url}/{plan_export_id}"
        return self._show(url)

    def download(self, plan_export_id, target_path):
        """
        ``GET /plan-exports/:id/download``

        `Plan Exports Download API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/plan-exports.html#download-exported-plan-data>`_
        """
        url = f"{self._endpoint_base_url}/{plan_export_id}/download"
        results = self._get(url, return_raw=True, allow_redirects=True)
        with open(target_path, 'wb') as target_file:
            target_file.write(results)

    def destroy(self, plan_export_id):
        """
        ``DELETE /plan-exports/:id``

        `Plan Exports Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/plan-exports.html#delete-exported-plan-data>`_
        """
        url = f"{self._endpoint_base_url}/{plan_export_id}"
        return self._destroy(url)
