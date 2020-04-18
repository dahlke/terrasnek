"""
Module for Terraform Cloud API Endpoint: Organization Memberships.
"""

import json
import requests

from .endpoint import TFCEndpoint

class TFCOrganizationMemberships(TFCEndpoint):
    """
    The Organization Memberships API is used to invite to organizations, to
    list memberships for an organization, to list a user's own memberships,
    to show a memberships, and to remove users from organizations.

    https://www.terraform.io/docs/cloud/api/organization-memberships.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._base_url = f"{base_url}/organization-memberships"
        self._org_base_url = f"{base_url}/organizations/{organization_name}/organization-memberships"

    def invite(self, payload):
        """
        POST /organizations/:organization_name/organization-memberships

        This endpoint invites a user to join an organization.
        """
        return self._create(self._org_base_url, payload)

    def lst_for_org(self):
        """
        GET /organizations/:organization_name/organization-memberships
        """
        return self._ls(self._org_base_url)

    def lst_for_user(self):
        """
        GET /organization-memberships
        """
        return self._ls(self._base_url)

    def show(self, organization_membership_id):
        """
        GET /organization-memberships/:organization_membership_id
        """
        url = f"{self._base_url}/{organization_membership_id}"
        return self._show(url)

    def remove(self, organization_membership_id):
        """
        DELETE /organization-memberships/:organization_membership_id
        """
        url = f"{self._base_url}/{organization_membership_id}"
        return self._destroy(url)