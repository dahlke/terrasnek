"""
Module for Terraform Cloud API Endpoint: Assessment Results.
"""

from .endpoint import TFCEndpoint

class TFCAssessmentResults(TFCEndpoint):
    """
    `Assessment Results API Docs \
        <https://www.terraform.io/cloud-docs/api-docs/assessment-results>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/assessment-results"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def show(self, assessment_result_id):
        """
        ``GET api/v2/assessment-results/:assessment_result_id``

        `Show Assessment Results API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/assessment-results#show-assessment-result>`_
        """
        url = f"{self._endpoint_base_url}/{assessment_result_id}"
        return self._show(url)

    def get_json_plan(self, assessment_result_id):
        """
        ``GET api/v2/assessment-results/:assessment_result_id/json-output``

        `Show Assessment Results JSON Plan API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/assessment-results#json-plan>`_
        """
        url = f"{self._endpoint_base_url}/{assessment_result_id}/json-output"
        return self._get(url)

    def get_json_schema(self, assessment_result_id):
        """
        ``GET api/v2/assessment-results/:assessment_result_id/json-schema``

        `Show Assessment Results JSON Schema API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/assessment-results#json-schema-file>`_
        """
        url = f"{self._endpoint_base_url}/{assessment_result_id}/json-schema"
        return self._get(url)

    def get_json_log_output(self, assessment_result_id):
        """
        ``GET api/v2/assessment-results/assessment_result_id/log-output``

        `Show Assessment Results JSON Log Output API Doc Reference \
            <https://www.terraform.io/cloud-docs/api-docs/assessment-results#json-log-output>`_
        """
        url = f"{self._endpoint_base_url}/{assessment_result_id}/log-output"
        return self._get(url)
