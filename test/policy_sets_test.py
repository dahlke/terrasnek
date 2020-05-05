"""
Module for testing the Terraform Cloud API Endpoint: Policy Sets.
"""

from .base import TestTFCBaseTestCase

POLICY_SETS_LIST_INCLUDE = "policies"

class TestTFCPolicySets(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policy Sets.
    """

    def setUp(self):
        # Set up a workspace to attach a policy set to
        self._ws = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("pol-set"))
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

        # Set up a policy to add and remove from the set
        create_payload = self._get_policy_create_payload()
        create_resp = self._api.policies.create(create_payload)
        policy = create_resp["data"]
        self._policy_id = policy["id"]

    def tearDown(self):
        # Destroy the workspace and policy we created
        self._api.workspaces.destroy(
            workspace_name=self._ws_name)
        self._api.policies.destroy(self._policy_id)

    def test_policy_sets_lifecycle(self):
        """
        Test the Policy Set API endpoints: create, list, show,
        update, destroy, add_policies_to_set, remove_policies_from_set,
        attach_policy_set_to_workspaces, detach_policy_set_from_workspaces
        """

        sets_resp = self._api.policy_sets.list()
        policy_sets = sets_resp["data"]
        self.assertEqual(len(policy_sets), 0)

        # Add a policy set to TFC
        create_payload = self._get_policy_set_create_payload()
        create_resp = self._api.policy_sets.create(create_payload)
        created_policy_set = create_resp["data"]
        created_policy_set_id = created_policy_set["id"]
        created_policy_set_name = created_policy_set["attributes"]["name"]

        # Check that we now have one policy set, use the query options to ensure
        # that they work.
        test_filters = [
            {
                "keys": ["versioned"],
                "value": False
            }
        ]
        sets_resp = self._api.policy_sets.list(\
            filters=test_filters, page=0, page_size=50, \
            include=POLICY_SETS_LIST_INCLUDE, search=created_policy_set_name)
        policy_sets = sets_resp["data"]
        self.assertEqual(len(policy_sets), 1)

        # Update the policy set
        desc_to_update_to = "foo"
        update_payload = {
            "data": {
                "attributes": {
                    "description": desc_to_update_to
                },
                "type": "policy-sets"
            }
        }
        update_resp = self._api.policy_sets.update(created_policy_set_id, update_payload)
        updated_policy_set = update_resp["data"]
        updated_desc = updated_policy_set["attributes"]["description"]
        self.assertEqual(desc_to_update_to, updated_desc)

        # Add the policy we created in the set up to the policy set
        add_remove_policy_payload = {
            "data": [
                {
                    "id": self._policy_id, "type": "policies"
                },
            ]
        }
        self._api.policy_sets.add_policies_to_set(created_policy_set_id, add_remove_policy_payload)
        shown_policy_set_resp = self._api.policy_sets.show(created_policy_set_id)
        shown_policies_in_set = shown_policy_set_resp["data"]["relationships"]["policies"]["data"]
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
        shown_policy_set_resp = self._api.policy_sets.show(created_policy_set_id)
        shown_workspaces_attached_to = \
            shown_policy_set_resp["data"]["relationships"]["workspaces"]["data"]
        self.assertEqual(len(shown_workspaces_attached_to), 1)

        # Detach the policy set from the workspace we created, confirm it's not attached
        self._api.policy_sets.detach_policy_set_from_workspaces(\
            created_policy_set_id, attach_detach_to_workspace_payload)
        shown_policy_set_resp = self._api.policy_sets.show(created_policy_set_id)
        shown_workspaces_attached_to = \
            shown_policy_set_resp["data"]["relationships"]["workspaces"]["data"]
        self.assertEqual(len(shown_workspaces_attached_to), 0)

        # Remove the policy from the set and confirm it has been removed
        self._api.policy_sets.remove_policies_from_set(\
            created_policy_set_id, add_remove_policy_payload)
        shown_policy_set_resp = self._api.policy_sets.show(created_policy_set_id)
        shown_policies_in_set = shown_policy_set_resp["data"]["relationships"]["policies"]["data"]
        self.assertEqual(len(shown_policies_in_set), 0)

        # Delete the policy set
        self._api.policy_sets.destroy(created_policy_set_id)

        # Check that we now have zero policy sets again
        sets_resp = self._api.policy_sets.list()
        policy_sets = sets_resp["data"]
        self.assertEqual(len(policy_sets), 0)


    def test_policy_sets_versions(self):
        """
        Test the Policy Set API endpoints: create_policy_set_version,
        show_policy_set_version.
        """
        # TODO
