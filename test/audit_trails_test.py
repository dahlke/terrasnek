"""
Module for testing the Terraform Cloud API Endpoint: Audit Trails.
"""

from .base import TestTFCBaseTestCase


class TestTFCAuditTrails(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Audit Trails.
    """

    _unittest_name = "audtrl"
    _endpoint_being_tested = "audit_trails"

    def setUp(self):
        # Create a user token with the API so that something shows in the audit logs for the org
        logged_in_user = self._api.account.show()["data"]
        logged_in_user_id = logged_in_user["id"]

        desc_to_update_to = self._unittest_random_name()
        create_payload = {
            "data": {
                "type": "authentication-tokens",
                "attributes": {
                    "description": desc_to_update_to
                }
            }
        }
        self._created_token = \
            self._api.user_tokens.create(logged_in_user_id, create_payload)["data"]
        self._created_token_id = self._created_token["id"]

    def tearDown(self):
        self._api.user_tokens.destroy(self._created_token_id)

    def test_audit_trails(self):
        """
        Test the Audit Trails API endpoints.
        """

        # List the audit trails. This deviates from the standard JSON spec
        # we use across the API, so we'll just assert no response, which
        # means it completed successfully for now.

        audit_trails = self._api.audit_trails.list()["data"]
        self.assertEqual(len(audit_trails), 0)

        all_audit_trails = self._api.audit_trails.list_all()
        self.assertEqual(len(all_audit_trails["data"]), 0)
