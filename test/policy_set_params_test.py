"""
Module for testing the Terraform Cloud API Endpoint: Policy Sets.
"""

from .base import TestTFCBaseTestCase


class TestTFCPolicySetParams(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Policy Set Params.
    """

    _unittest_name = "pol-set-params"
    _endpoint_being_tested = "policy_set_params"

    def setUp(self):
        oauth_client = self._api.oauth_clients.create(\
            self._get_oauth_client_create_payload())["data"]
        self._oauth_client_id = oauth_client["id"]
        oauth_token_id = oauth_client["relationships"]["oauth-tokens"]["data"][0]["id"]

        # Create a temp policy set to manipulate in the test, store the ID
        created_policy_set = self._api.policy_sets.create(\
            self._get_policy_set_create_payload(oauth_token_id))["data"]
        self._created_policy_set_id = created_policy_set["id"]

    def tearDown(self):
        # Destroy the workspace and policy we created
        self._api.policy_sets.destroy(self._created_policy_set_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_policy_sets(self):
        """
        Test the Policy Set Params API endpoints.
        """

        # List the params, confirm that there are none to start.
        all_params = self._api.policy_set_params.list(self._created_policy_set_id)["data"]
        self.assertEqual(len(all_params), 0)

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
        created_param = self._api.policy_set_params.create(\
            self._created_policy_set_id, create_payload)["data"]
        created_param_id = created_param["id"]
        all_params = self._api.policy_set_params.list(self._created_policy_set_id)["data"]
        self.assertEqual(len(all_params), 1)

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
        update_params = self._api.policy_set_params.update(\
            self._created_policy_set_id, created_param_id, update_payload)["data"]
        updated_value = update_params["attributes"]["value"]
        self.assertEqual(updated_value, value_to_update_to)

        # Delete the variable and confirm there are none left
        self._api.policy_set_params.destroy(self._created_policy_set_id, created_param_id)
        all_params = self._api.policy_set_params.list(self._created_policy_set_id)["data"]
        self.assertEqual(len(all_params), 0)
