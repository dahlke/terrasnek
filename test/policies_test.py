"""
Module for testing the Terraform Cloud API Endpoint: Policies.
"""

from .base import TestTFCBaseTestCase


class TestTFCPolicies(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policies.
    """

    def test_policies_lifecycle(self):
        """
        Test the Policies API endpoints: create, list, show,
        update, upload, destroy.
        """

        policies_resp = self._api.policies.list()
        policies = policies_resp["data"]
        self.assertEqual(len(policies), 0)

        # Add a policy to TFC
        create_payload = self._get_policy_create_payload()
        create_resp = self._api.policies.create(create_payload)
        created_policy = create_resp["data"]
        created_policy_id = created_policy["id"]
        created_policy_name = created_policy["attributes"]["name"]

        # List all the policies, search the policy we just created so
        # we can test out the list params
        policies_resp = self._api.policies.list(\
            page=0, page_size=50, search=created_policy_name)
        policies = policies_resp["data"]
        self.assertEqual(len(policies), 1)

        # Upload the policy
        policy_payload = "main = rule { true }"
        self._api.policies.upload(created_policy_id, policy_payload)

        # Show the policy we just created
        shown_resp = self._api.policies.show(created_policy_id)
        shown_policy = shown_resp["data"]
        shown_policy_id = shown_policy["id"]

        # Make sure the IDs are the same
        self.assertEqual(shown_policy_id, created_policy_id)

        # And make sure our upload took effect
        self.assertTrue("upload" in shown_policy["links"])

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
        update_resp = self._api.policies.update(created_policy_id, update_payload)
        updated_policy = update_resp["data"]
        updated_desc = updated_policy["attributes"]["description"]
        self.assertEqual(desc_to_update_to, updated_desc)

        # Delete the policy we just updated
        self._api.policies.destroy(created_policy_id)

        # Check that we now have zero policies again
        policies_resp = self._api.policies.list()
        policies = policies_resp["data"]
        self.assertEqual(len(policies), 0)
