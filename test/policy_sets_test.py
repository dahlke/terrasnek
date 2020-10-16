"""
Module for testing the Terraform Cloud API Endpoint: Policy Sets.
"""

import time
from .base import TestTFCBaseTestCase


class TestTFCPolicySets(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policy Sets.
    """

    _unittest_name = "pol-sets"
    _endpoint_being_tested = "policy_sets"

    def setUp(self):
        # Set up a workspace to attach a policy set to
        workspace = self._api.workspaces.create(self._get_ws_without_vcs_create_payload())["data"]
        self._ws_id = workspace["id"]
        self._ws_name = workspace["attributes"]["name"]

        # Set up a policy to add and remove from the set
        policy = self._api.policies.create(self._get_policy_create_payload())["data"]
        self._policy_id = policy["id"]

    def tearDown(self):
        # Destroy the workspace and policy we created
        self._api.workspaces.destroy(
            workspace_name=self._ws_name)
        self._api.policies.destroy(self._policy_id)

    def test_policy_sets(self):
        """
        Test the Policy Sets API endpoints.
        """
        # List all the policy sets, confirm there are none
        all_policy_sets = self._api.policy_sets.list()["data"]
        self.assertEqual(len(all_policy_sets), 0)

        # Add a policy set to TFC
        created_policy_set = self._api.policy_sets.create(self._get_policy_create_payload())["data"]
        created_policy_set_id = created_policy_set["id"]
        created_policy_set_name = created_policy_set["attributes"]["name"]

        # Check that we now have one policy set, use the query options to ensure
        # that they work.
        test_filters = [
            {
                "keys": ["versioned"],
                "value": "false"
            }
        ]
        all_policy_sets = self._api.policy_sets.list(\
            filters=test_filters, page=0, page_size=50, \
            include="policies", search=created_policy_set_name)["data"]
        self.assertEqual(len(all_policy_sets), 1)

        # Update the policy set, confirm the update took place
        desc_to_update_to = "foo"
        update_payload = {
            "data": {
                "attributes": {
                    "description": desc_to_update_to
                },
                "type": "policy-sets"
            }
        }
        updated_policy_set = self._api.policy_sets.update( \
            created_policy_set_id, update_payload)["data"]
        self.assertEqual(desc_to_update_to, updated_policy_set["attributes"]["description"])

        # Add the policy we created in the set up to the policy set
        add_remove_policy_payload = {
            "data": [
                {
                    "id": self._policy_id, "type": "policies"
                },
            ]
        }
        self._api.policy_sets.add_policies_to_set(created_policy_set_id, add_remove_policy_payload)
        shown_policy_set = self._api.policy_sets.show(created_policy_set_id)["data"]
        shown_policies_in_set = shown_policy_set["relationships"]["policies"]["data"]
        self.assertEqual(len(shown_policies_in_set), 1)

        # Attach the policy set to the workspace we created, confirm it's attached
        attach_detach_to_workspace_payload = {
            "data": [
                {
                    "id": self._ws_id, "type": "workspaces"
                },
            ]
        }
        self._api.policy_sets.attach_policy_set_to_workspaces(\
            created_policy_set_id, attach_detach_to_workspace_payload)
        shown_policy_set = self._api.policy_sets.show(created_policy_set_id)["data"]
        shown_workspaces_attached_to = \
            shown_policy_set["relationships"]["workspaces"]["data"]
        self.assertEqual(len(shown_workspaces_attached_to), 1)

        # Detach the policy set from the workspace we created, confirm it's not attached
        self._api.policy_sets.detach_policy_set_from_workspaces(\
            created_policy_set_id, attach_detach_to_workspace_payload)
        shown_policy_set = self._api.policy_sets.show(created_policy_set_id)["data"]
        self.assertEqual(len(shown_policy_set["relationships"]["workspaces"]["data"]), 0)

        # Remove the policy from the set and confirm it has been removed
        self._api.policy_sets.remove_policies_from_set(\
            created_policy_set_id, add_remove_policy_payload)
        shown_policy_set = self._api.policy_sets.show(created_policy_set_id)["data"]
        shown_policies_in_set = shown_policy_set["relationships"]["policies"]["data"]
        self.assertEqual(len(shown_policies_in_set), 0)

        # Delete the policy set, confirm it's been deleted
        self._api.policy_sets.destroy(created_policy_set_id)
        all_policy_sets = self._api.policy_sets.list()["data"]
        self.assertEqual(len(all_policy_sets), 0)


    def test_policy_sets_versions(self):
        """
        Test the Policy Sets Versions API endpoints.
        """
        # Create a new policy set and policy set version, without being attached to VCS.
        created_policy_set = self._api.policy_sets.create(self._get_policy_create_payload())["data"]
        created_policy_set_id = created_policy_set["id"]
        pol_set_version = self._api.policy_sets.create_policy_set_version(\
            created_policy_set_id)["data"]
        pol_set_version_id = pol_set_version["id"]

        # Upload the policy set tarball from testdata
        self._api.policy_sets.upload(
            self._policy_set_upload_tarball_path, pol_set_version_id)
        shown_pol_set_version = self._api.policy_sets.show_policy_set_version(\
            pol_set_version["id"])["data"]

        # Confirm the upload is completed and the policy set is ready to use
        time.sleep(5)
        ready_or_pending = \
            shown_pol_set_version["attributes"]["status"] in ["pending", "ready"]
        self.assertTrue(ready_or_pending)
        self._api.policy_sets.destroy(created_policy_set_id)
