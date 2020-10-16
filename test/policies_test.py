"""
Module for testing the Terraform Cloud API Endpoint: Policies.
"""

from .base import TestTFCBaseTestCase


class TestTFCPolicies(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policies.
    """

    _unittest_name = "pol"
    _endpoint_being_tested = "policies"

    def test_policies(self):
        """
        Test the Policies API endpoints.
        """

        # Confirm we have no policies.
        all_policies = self._api.policies.list()["data"]
        self.assertEqual(len(all_policies), 0)

        # Add a policy to TFC
        created_policy = self._api.policies.create(self._get_policy_create_payload())["data"]
        created_policy_id = created_policy["id"]
        created_policy_name = created_policy["attributes"]["name"]

        # List all the policies, search the policy we just created so
        # we can test out the list params
        all_policies = self._api.policies.list(\
            page=0, page_size=50, search=created_policy_name)["data"]

        found_pol = False
        for pol in all_policies:
            if created_policy_id == pol["id"]:
                found_pol = True
                break
        self.assertTrue(found_pol)

        # Upload the policy
        policy_payload = "main = rule { true }"
        self._api.policies.upload(created_policy_id, policy_payload)

        # Show the policy we just created
        shown_policy = self._api.policies.show(created_policy_id)["data"]
        shown_policy_id = shown_policy["id"]

        # Make sure the IDs are the same
        self.assertEqual(shown_policy_id, created_policy_id)

        # And make sure our upload took effect
        self.assertIn("upload", shown_policy["links"])

        # Update the policy
        desc_to_update_to = "foo"
        update_payload = {
            "data": {
                "attributes": {
                    "description": desc_to_update_to
                },
                "type":"policies"
            }
        }
        updated_policy = self._api.policies.update(created_policy_id, update_payload)["data"]
        updated_desc = updated_policy["attributes"]["description"]
        self.assertEqual(desc_to_update_to, updated_desc)

        # Delete the policy we just updated
        self._api.policies.destroy(created_policy_id)

        # Check that we now have zero policies again
        all_policies = self._api.policies.list()["data"]
        self.assertEqual(len(all_policies), 0)
