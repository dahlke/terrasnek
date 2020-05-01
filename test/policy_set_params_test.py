"""
Module for testing the Terraform Cloud API Endpoint: Policy Sets.
"""

from .base import TestTFCBaseTestCase


class TestTFCPolicySetParams(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policy Set Params.
    """

    def setUp(self):
        create_payload = self._get_policy_set_create_payload()
        create_resp = self._api.policy_sets.create(create_payload)
        self._created_policy_set = create_resp["data"]
        self._created_policy_set_id = self._created_policy_set["id"]

    def tearDown(self):
        # Destroy the workspace and policy we created
        self._api.policy_sets.destroy(self._created_policy_set_id)

    def test_policy_sets_lifecycle(self):
        """
        Test the Policy Set Params API endpoints: create, list, update,
        destroy.
        """

        # Make sure we have no params to start
        params_resp = self._api.policy_set_params.list(self._created_policy_set_id)
        params = params_resp["data"]
        self.assertEqual(len(params), 0)

        # Create a variable and confirm it was added to the policy set
        create_payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": "terrasnek",
                    "value": "unittest",
                    "category": "policy-set",
                    "sensitive": False
                }
            }
        }
        create_resp = self._api.policy_set_params.create(\
            self._created_policy_set_id, create_payload)
        created_param_id = create_resp["data"]["id"]

        params_resp = self._api.policy_set_params.list(self._created_policy_set_id)
        params = params_resp["data"]
        self.assertEqual(len(params), 1)

        # Update the value and confirm the change
        value_to_update_to = "bar"
        update_payload = {
            "data": {
                "id": created_param_id,
                "attributes": {
                    "key": "foo",
                    "value": value_to_update_to,
                    "category": "policy-set",
                    "sensitive": False
                },
                "type": "vars"
            }
        }
        update_resp = self._api.policy_set_params.update(\
            self._created_policy_set_id, created_param_id, update_payload)
        updated_value = update_resp["data"]["attributes"]["value"]
        self.assertEqual(updated_value, value_to_update_to)

        # Delete the variable and confirm there is only 1 left
        self._api.policy_set_params.destroy(self._created_policy_set_id, created_param_id)
        params_resp = self._api.policy_set_params.list(self._created_policy_set_id)
        params = params_resp["data"]
        self.assertEqual(len(params), 0)
