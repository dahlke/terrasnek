"""
Module for Terraform Cloud API Endpoint: Invoices.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCInvoices(TFCEndpoint):
    """
    `Invoices API Docs \
        <https://www.terraform.io/docs/cloud/api/invoices.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/invoices"

    def required_entitlements(self):
        return [Entitlements.SELF_SERVE_BILLING]

    def terraform_cloud_only(self):
        # NOTE: This is a TFC-only endpoint
        return True

    def terraform_enterprise_only(self):
        return False

    def list(self):
        """
        ``GET /organizations/:organization_name/invoices``

        `Invoices List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/invoices.html#list-invoices>`_
        """
        # TODO: cursor pagination
        return self._list(self._org_base_url)

    def next(self):
        """
        ``GET /organizations/:organization_name/invoices/next``

        `Invoices Get Next API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/invoices.html#get-next-invoice>`_
        """
        url = f"{self._org_base_url}/next"
        return self._get(url)
