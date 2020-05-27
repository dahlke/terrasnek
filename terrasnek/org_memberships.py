"""
Module for Terraform Cloud API Endpoint: Org Memberships.
"""

from .endpoint import TFCEndpoint

class TFCOrgMemberships(TFCEndpoint):
    """
    The Org Memberships API is used to invite to organizations, to
    list memberships for an organization, to list a user's own memberships,
    to show a memberships, and to remove users from organizations.

    https://www.terraform.io/docs/cloud/api/organization-memberships.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/organization-memberships"
        self._org_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/organization-memberships"

    def required_entitlements(self):
        return []

    def invite(self, payload):
        """
        ``POST /organizations/:organization_name/organization-memberships``

        This endpoint invites a user to join an organization.
        """
        return self._create(self._org_base_url, payload)

    def list_for_org(self, query=None, filters=None, page=None, page_size=None):
        """
        ``GET /organizations/:organization_name/organization-memberships``

        This endpoint retrieves all the users in the active organization.

        PARAMS:
            https://www.terraform.io/docs/cloud/api/organization-memberships.html#query-parameters
        """
        return self._list(\
            self._org_base_url, query=query, filters=filters, page=page, page_size=page_size)

    def list_for_user(self):
        """
        ``GET /organization-memberships``

        This endpoint retrieves all the organizations for the active user.
        """
        return self._list(self._endpoint_base_url)

    def show(self, org_membership_id):
        """
        ``GET /organization-memberships/:organization_membership_id``

        This endpoint shows organization membership details for the
        specified organization membership ID.
        """
        url = f"{self._endpoint_base_url}/{org_membership_id}"
        return self._show(url)

    def remove(self, org_membership_id):
        """
        ``DELETE /organization-memberships/:organization_membership_id``

        This endpoint removes a user from an organization using the
        specified organization membership ID.
        """
        url = f"{self._endpoint_base_url}/{org_membership_id}"
        return self._destroy(url)
