"""
Module for testing the Terraform Cloud API Endpoint: Invoices.
"""

from .base import TestTFCBaseTestCase


class TestTFCInvoices(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Invoices.
    """

    _unittest_name = "invoi"
    _endpoint_being_tested = "invoices"

    def test_invoices(self):
        """
        Test the Invoices API endpoints.
        """
        # NOTE / TODO: this will fail since we don't have any billing info associated with the test org.
        invoices = self._api.invoices.list()
        self.assertIsNotNone(invoices)
