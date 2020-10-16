"""
Module for testing the Terraform Cloud API Endpoint: IP Ranges.
"""

from .base import TestTFCBaseTestCase


class TestTFCIPRanges(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: IP Ranges.
    """

    _unittest_name = "iprang"
    _endpoint_being_tested = "ip_ranges"

    def test_ip_ranges(self):
        """
        Test the IP Ranges API endpoints.
        """
        ip_ranges = self._api.ip_ranges.list()

        self.assertIn("notifications", ip_ranges)
        self.assertIn("sentinel", ip_ranges)
        self.assertIn("vcs", ip_ranges)
