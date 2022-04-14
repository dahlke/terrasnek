"""
Module for testing the Terraform Cloud API Endpoint: Comments.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCComments(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Comments.
    """

    _unittest_name = "comme"
    _endpoint_being_tested = "comments"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = oauth_client["data"]["id"]
        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a workspace using that token ID, save the workspace ID
        ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id)
        workspace = self._api.workspaces.create(ws_payload)["data"]
        self._ws_id = workspace["id"]
        self._temp_org_name = self._random_name()

        # Configure the required variables on the workspace
        variable_payloads = [
            self._get_variable_create_payload(
                "email", self._test_email, self._ws_id),
            self._get_variable_create_payload(
                "org_name", self._temp_org_name, self._ws_id),
            self._get_variable_create_payload(
                "hostname", self._api.get_hostname(), self._ws_id),
            self._get_variable_create_payload(
                "TFE_TOKEN", self._test_api_token, self._ws_id, category="env", sensitive=True)
        ]
        for payload in variable_payloads:
            self._api.vars.create(payload)

        # Sleep for 1 second to give the WS time to create
        time.sleep(1)

        # Start the run, store the run ID
        create_run_payload = self._get_run_create_payload(self._ws_id)
        self._run = self._api.runs.create(create_run_payload)["data"]
        self._run_id = self._run["id"]


    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_comments(self):
        """
        Test the Comments API endpoints.
        """

        # Timeout if the plan doesn't reach confirmable, this can happen
        # if the run is queued.
        self._created_run_timeout(self._run_id)

        comment_text = "foo"

        # Apply the plan
        apply_payload = {
            "comment": comment_text
        }
        self._api.runs.apply(self._run_id, apply_payload)
        applied_run = self._api.runs.show(self._run_id)["data"]

        self._logger.debug("Waiting for apply to kick off...")
        while "applying-at" not in applied_run["attributes"]["status-timestamps"]:
            applied_run = self._api.runs.show(self._run_id)["data"]
            time.sleep(1)
        self._logger.debug("Apply kicked off.")

        comments = self._api.comments.list_for_run(self._run_id)["data"]
        self.assertEqual(comments[0]["attributes"]["body"], "foo")

        new_comment_text = "bar"
        create_payload = {
            "data": {
                "attributes": {
                    "body": new_comment_text,
                },
                "type": "comments"
            }
        }

        created_comment = self._api.comments.create_for_run(self._run_id, create_payload)["data"]
        created_comment_id = created_comment["id"]
        self.assertEqual(new_comment_text, created_comment["attributes"]["body"])

        shown_comment = self._api.comments.show(created_comment_id)["data"]
        self.assertEqual(created_comment_id, shown_comment["id"])
