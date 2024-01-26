"""
Module for Terraform Cloud API Endpoint: Run Tasks Stages and Results.
"""

from .endpoint import TFCEndpoint

class TFCRunTasksStagesResults(TFCEndpoint):
    """
    `Run Tasks Stages and Results API Docs \
        <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-task-stages-and-results>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._runs_base_url = f"{self._api_v2_base_url}/runs"
        self._task_stages_base_url = f"{self._api_v2_base_url}/task-stages"
        self._task_results_base_url = f"{self._api_v2_base_url}/task-results"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def list_stages(self, run_id, page=None, page_size=None):
        """
        ``GET /runs/:run_id/task-stages``

        `Run Tasks List Stages API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-task-stages-and-results>`_

        `Query Parameter(s) Details \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-task-stages-and-results#query-parameters>`__
        """
        url = f"{self._runs_base_url}/{run_id}/task-stages"
        return self._list(url, page=page, page_size=page_size)

    def show_stage(self, task_stage_id):
        """
        ``GET /task-stages/:task_stage_id``

        `Run Tasks Show Stage API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-task-stages-and-results#show-a-run-task-stage>`_
        """
        url = f"{self._task_stages_base_url}/{task_stage_id}"
        return self._show(url)

    def show_result(self, task_result_id):
        """
        ``GET /task-results/:task_result_id``

        `Run Tasks Show Result API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-task-stages-and-results#show-a-run-task-result>`_
        """
        url = f"{self._task_results_base_url}/{task_result_id}"
        return self._show(url)

    def override_stage(self, task_stage_id):
        """
        ``POST /task-stages/:task_stage_id/actions/override``

        `Run Tasks Override Task Stage API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run-tasks/run-task-stages-and-results#override-a-task-stage>`_
        """
        url = f"{self._task_stages_base_url}/{task_result_id}/actions/override"
        return self._post(url)
