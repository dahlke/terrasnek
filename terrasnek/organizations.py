"""
Module for Terraform Cloud API Endpoint: Organizations.
"""

import json
import requests

from .endpoint import TFCEndpoint

class TFCOrganizations(TFCEndpoint):
    """
    The Organizations API is used to list, show, create, update, and destroy organizations.

    https://www.terraform.io/docs/cloud/api/organizations.html
    """

    def __init__(self, base_url, organization_name, headers, verify):
        super().__init__(base_url, organization_name, headers, verify)
        self._org_base_url = f"{base_url}/organizations"

    def create(self, payload):
        """
        POST /organizations
        """
        return self._create(self._org_base_url, payload)

    def destroy(self, organization_name):
        """
        DELETE /organizations/:organization_name
        """
        url = f"{self._org_base_url}/{organization_name}"
        return self._destroy(url)

    def entitlements(self, organization_name):
        """
        GET /organizations/:organization_name/entitlement-set

        This endpoint shows the entitlements for an organization.
        """
        results = None
        url = f"{self._org_base_url}/{organization_name}/entitlement-set"
        req = self._get(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))["errors"][0]
            self._logger.error(err)

        return results

    def lst(self):
        """
        GET /organizations
        """
        return self._ls(self._org_base_url)

    def show(self, organization_name):
        """
        GET /organizations/:organization_name
        """
        url = f"{self._org_base_url}/{organization_name}"
        return self._show(url)

    def update(self, organization_name, payload):
        """
        PATCH /organizations/:organization_name
        """
        url = f"{self._org_base_url}/{organization_name}"
        return self._update(url, payload)
