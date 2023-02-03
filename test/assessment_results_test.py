"""
Module for testing the Terraform Cloud API Endpoint: Assessment Results.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCAssessmentResults(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Assessment Results.
    """

    _unittest_name = "asr"
    _endpoint_being_tested = "assessment_results"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = oauth_client["data"]["id"]
        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        _ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id)

        # NOTE: this test requires that you enable data.attributes.assessments_enabled
        _ws_payload["data"]["attributes"]["assessments_enabled"] = True
        workspace = self._api.workspaces.create(_ws_payload)["data"]
        self._ws_id = workspace["id"]

        # Configure the required variables on the workspace
        variable_payloads = [
            self._get_variable_create_payload(
                "email", self._test_email, self._ws_id),
            self._get_variable_create_payload(
                "org_name", self._test_org_name, self._ws_id),
            self._get_variable_create_payload(
                "TFE_TOKEN", self._test_api_token, self._ws_id, category="env", sensitive=True)
        ]
        for payload in variable_payloads:
            self._api.vars.create(payload)

        # Sleep for 3 seconds to give the WS time to create, takes a bit longer
        # on small TFE instances.
        time.sleep(3)

        # Start the run, store the run ID
        create_run_payload = self._get_run_create_payload(self._ws_id)
        self._run = self._api.runs.create(create_run_payload)["data"]
        self._run_id = self._run["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_assessment_results(self):
        """
        Test the Assessment Results API endpoints.
        """

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        created_run = self._created_run_timeout(self._run_id)
        created_plan_id = created_run["relationships"]["plan"]["data"]["id"]

        # Confirm the shown plan's ID matches the ID from the run
        plan = self._api.plans.show(created_plan_id)["data"]
        self.assertEqual(created_plan_id, plan["id"])

        # TODO: Will have to add an includes to show plan to get the assessment result id once
        # the team has it finished. This will show the drift detection.
        # print(plan)

        # TODO: To get this to work
        # https://developer.hashicorp.com/terraform/cloud-docs/workspaces/health
        # Upgrade to TF 1.3.0
        # https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/organizations#health
        # Enable Health Assessments
