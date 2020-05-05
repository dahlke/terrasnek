"""
Module for testing the Terraform Cloud API Endpoint: Org Memberships.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrgMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Org Memberships.
    """


    def test_org_memberships_lifecycle(self):
        """
        Test the Org Memberships API endpoints: invite, list_for_org,
        list_for_user, show, remove.
        """

        # TODO: User needs to be created ahead of time, and it can't be done with
        # the API currently.

        # Get the existing org memberships for the logged in user
        orgs_for_user = self._api.org_memberships.list_for_user()
        num_org_memberships = len(orgs_for_user["data"])
        self.assertEqual(num_org_memberships, 1)

        # Invite a user
        invite_payload = self._get_org_membership_invite_payload()
        invite = self._api.org_memberships.invite(invite_payload)
        invited_username = invite["included"][0]["attributes"]["username"]
        self.assertEqual(invited_username, self._test_username)

        # Show a user's org membership using the org membership ID
        org_membership_id = invite["data"]["id"]
        shown_membership = self._api.org_memberships.show(org_membership_id)
        shown_membership_id = shown_membership["data"]["id"]
        self.assertEqual(org_membership_id, shown_membership_id)

        # List the users in the org, but do some filtering to test out those features,
        # and only look for the user we just added
        test_filters = [
            {
                "keys": ["status"],
                "value": "inactive"
            }
        ]
        truncated_test_username = self._test_username[:5]
        users_for_org = self._api.org_memberships.list_for_org(\
            query=truncated_test_username, filters=test_filters, page=0, page_size=50)
        num_users_in_org = len(users_for_org["data"])
        self.assertEqual(num_users_in_org, 1)


        # Remove the user
        self._api.org_memberships.remove(org_membership_id)
        users_for_org = self._api.org_memberships.list_for_org()
        num_users_in_org = len(users_for_org["data"])
        self.assertEqual(num_users_in_org, 1)
