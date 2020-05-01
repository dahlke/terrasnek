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

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/organization-memberships"
        self._org_base_url = \
            f"{base_url}/organizations/{org_name}/organization-memberships"

    def invite(self, payload):
        """
        POST /organizations/:org_name/organization-memberships

        This endpoint invites a user to join an organization.
        """
        return self._create(self._org_base_url, payload)

    def list_for_org(self, query=None, filters=None, page=None, page_size=None):
        """
        GET /organizations/:org_name/organization-memberships

        This endpoint retrieves all the users in the active organization.

        PARAMS:
            https://www.terraform.io/docs/cloud/api/organization-memberships.html#query-parameters
        """
        return self._list(\
            self._org_base_url, query=query, filters=filters, page=page, page_size=page_size)

    def list_for_user(self):
        """
        GET /organization-memberships

        This endpoint retrieves all the organizations for the active user.
        """
        return self._list(self._base_url)

    def show(self, org_membership_id):
        """
        GET /organization-memberships/:org_membership_id

        This endpoint shows organization membership details for the
        specified organization membership ID.
        """
        url = f"{self._base_url}/{org_membership_id}"
        return self._show(url)

    def remove(self, org_membership_id):
        """
        DELETE /organization-memberships/:org_membership_id

        This endpoint removes a user from an organization using the
        specified organization membership ID.
        """
        url = f"{self._base_url}/{org_membership_id}"
        return self._destroy(url)
