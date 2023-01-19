"""
Module for Terraform Cloud API Endpoint: Policy Checks.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicyChecks(TFCEndpoint):
    """
    `Policy Checks API Docs \
        <https://www.terraform.io/docs/cloud/api/policy-checks.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policy-checks"
        self._task_stages_url = f"{self._api_v2_base_url}/task-stages"
        self._pol_evals_url = f"{self._api_v2_base_url}/policy-evaluations"
        self._pol_outcomes_url = f"{self._api_v2_base_url}/policy-set-outcomes"
        self._runs_api_v2_base_url = f"{self._api_v2_base_url}/runs"

    def required_entitlements(self):
        # NOTE: Entitlements.SENTINEL has been deprecated, using Policy Enforcement instead.
        return [Entitlements.POLICY_ENFORCEMENT]

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def show(self, policy_check_id):
        """
        ``GET /policy-checks/:id``

        `Policy Checks Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-checks.html#show-policy-check>`_
        """
        url = f"{self._endpoint_base_url}/{policy_check_id}"
        return self._show(url)

    def list(self, run_id):
        """
        ``GET /runs/:run_id/policy-checks``

        `Policy Checks List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-checks.html#list-policy-checks>`_
        """
        url = f"{self._runs_api_v2_base_url}/{run_id}/policy-checks"
        return self._list(url)

    def override(self, policy_check_id):
        """
        ``POST /policy-checks/:id/actions/override``

        `Policy Checks Override API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policy-checks.html#override-policy>`_
        """
        url = f"{self._endpoint_base_url}/{policy_check_id}/actions/override"
        return self._post(url)

    def list_policy_evals_in_task_stage(self, task_stage_id):
        """
        ``GET /task-stages/:task_stage_id/policy-evaluations``

        `Policy Checks List Policy Evaluations API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-checks#list-policy-evaluations-in-the-task-stage>`_
        """
        url = f"{self._task_stages_url}/{task_stage_id}/policy-checks"
        return self._list(url)

    def list_policy_outcomes(self, policy_eval_id):
        """
        ``GET /policy-evaluations/:policy_evaluation_id/policy-set-outcomes``

        `Policy Checks List Policy Outcomes API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-checks#list-policy-outcomes>`_
        """
        url = f"{self._pol_evals_url}/{policy_eval_id}/policy-set-outcomes"
        return self._list(url)

    def show_policy_outcome(self, policy_set_outcome_id):
        """
        ``GET /policy-set-outcomes/:policy_set_outcome_id``

        `Policy Checks Show Policy Outcome API Doc Reference \
            <https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-checks#list-policy-outcomes>`_
        """
        url = f"{self._pol_outcomes_url}/{policy_set_outcome_id}/policy-set-outcomes"
        return self._show(url)
