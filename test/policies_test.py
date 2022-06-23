"""
Module for testing the Terraform Cloud API Endpoint: Policies.
"""

from .base import TestTFCBaseTestCase
from ._constants import PAGE_START, PAGE_SIZE


class TestTFCPolicies(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policies.
    """

    _unittest_name = "pol"
    _endpoint_being_tested = "policies"

    def setUp(self):
        created_policy_set = self._api.policy_sets.create(self._get_policy_create_payload())["data"]
        self._created_policy_set_id = created_policy_set["id"]
        self._created_policy_set_name = created_policy_set["attributes"]["name"]

    def tearDown(self):
        self._api.policy_sets.destroy(self._created_policy_set_id)

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

        add_remove_policy_payload = {
            "data": [
                {
                    "id": created_policy_id,
                    "type": "policies"
                },
            ]
        }
        self._api.policy_sets.add_policies_to_set(\
            self._created_policy_set_id, add_remove_policy_payload)

        search_payload = {
            "name": created_policy_name
        }

        # List all the policies, search the policy we just created so
        # we can test out the list params
        some_policies_raw = self._api.policies.list(\
            page=PAGE_START, page_size=PAGE_SIZE, search=search_payload, include=["policy-sets"])

        # Confirm that included resources are present
        self.assertIn("included", some_policies_raw)

        some_policies = some_policies_raw["data"]

        found_pol = False
        for pol in some_policies:
            if created_policy_id == pol["id"]:
                found_pol = True
                break
        self.assertTrue(found_pol)

        all_policies = self._api.policies.list_all(\
            search=search_payload, include=["policy-sets"])
        self.assertIn("included", all_policies)

        found_pol = False
        for pol in all_policies["data"]:
            if created_policy_id == pol["id"]:
                found_pol = True
                break
        self.assertTrue(found_pol)

        # Upload the policy
        policy_payload = "main = rule { true }"
        self._api.policies.upload(created_policy_id, policy_payload)

        # Show the policy we just created
        shown_policy_raw = self._api.policies.show(created_policy_id, include=["policy-sets"])

        # Confirm that included resources are present
        self.assertIn("included", shown_policy_raw)

        shown_policy = shown_policy_raw["data"]
        shown_policy_id = shown_policy["id"]

        # Get the text of the policy we just created
        policy_text = self._api.policies.get_policy_text(created_policy_id)
        self.assertEqual(policy_text, policy_payload)

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
        some_policies = self._api.policies.list()["data"]
        self.assertEqual(len(some_policies), 0)
