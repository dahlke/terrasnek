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

    def test_audit_trails(self):
        """
        Test the Audit Trails API endpoints.
        """

        # List the audit trails. This deviates from the standard JSON spec
        # we use across the API, so we'll just assert no response, which
        # means it completed successfully for now.

        audit_trails = self._api.audit_trails.list()["data"]
        self.assertEqual(len(audit_trails), 0)
