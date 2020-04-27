"""
Module for Terraform Cloud API Endpoint: Policies.
"""

import requests
import json

from .endpoint import TFCEndpoint

class TFCPolicies(TFCEndpoint):
    """
        Policies are configured on a per-organization level and are organized
        and grouped into policy sets, which define the workspaces on which
        policies are enforced during runs. In these workspaces, the plan's changes
        are validated against the relevant policies after the plan step.

        https://www.terraform.io/docs/cloud/api/policies.html
    """
    def __init__(self, base_url, organization_name, headers, verify):
        super().__init__(base_url, organization_name, headers, verify)
        self._base_url = f"{base_url}/policies"
        self._org_base_url = f"{base_url}/organizations/{organization_name}/policies"

    def create(self, payload):
        """
        This creates a new policy object for the organization, but does not upload
        the actual policy code

        POST /organizations/:organization_name/policies
        """
        return self._create(self._org_base_url, payload)

    def lst(self):
        """
        GET /organizations/:organization_name/policies
        """
        return self._ls(self._org_base_url)

    def show(self, policy_id):
        """
        GET /policies/:policy_id
        """
        url = f"{self._base_url}/{policy_id}"
        return self._show(url)

    def update(self, policy_id, payload):
        """
        PATCH /policies/:policy_id
        """
        url = f"{self._base_url}/{policy_id}"
        return self._update(url, payload)

    def upload(self, policy_id, payload):
        """
        PUT /policies/:policy_id/upload
        """
        url = f"{self._base_url}/{policy_id}/upload"
        return self._put(url, octet=True, data=payload)

    def destroy(self, policy_id):
        """
        DELETE /policies/:policy_id
        """
        url = f"{self._base_url}/{policy_id}"
        return self._destroy(url)
