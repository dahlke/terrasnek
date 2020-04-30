"""
Module for testing the Terraform Cloud API Endpoint: Org Memberships.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrgMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Org Memberships.
    """

    # TODO: create a user with the admin API here if possible.

    def test_org_memberships_lifecycle(self):
        """
        Test the Org Memberships API endpoints: invite, list_for_org,
        list_for_user, show, remove.
        """
        # Get the existing org memberships for the logged in user
        orgs_for_user = self._api.org_memberships.list_for_user()
        num_org_memberships = len(orgs_for_user["data"])
        self.assertEqual(num_org_memberships, 1)
        # TODO: need to change the user that I run the tests with in TFC,
        # as my personal user is already in 2 orgs
        # self.assertEqual(num_org_memberships, 2)

        # Get teams for the base org
        teams = self._api.teams.list()
        owners_team = teams["data"][0]
        owners_team_id = owners_team["id"]

        # Invite a user
        invite_payload = self._get_org_membership_invite_payload(owners_team_id)
        invite = self._api.org_memberships.invite(invite_payload)
        invited_user_email = invite["data"]["attributes"]["email"]
        self.assertEqual(invited_user_email, self._test_email)

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
            q=truncated_test_username, filters=test_filters, page=0, page_size=50)
        num_users_in_org = len(users_for_org["data"])
        self.assertEqual(num_users_in_org, 1)


        # Remove the user
        removal = self._api.org_memberships.remove(org_membership_id)
        users_for_org = self._api.org_memberships.list_for_org()
        num_users_in_org = len(users_for_org["data"])
        self.assertEqual(num_users_in_org, 1)