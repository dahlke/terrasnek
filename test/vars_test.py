"""
Module for testing the Terraform Cloud API Endpoint: Variables.
"""

from .base import TestTFCBaseTestCase


class TestTFCVars(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Variables.
    """

    _unittest_name = "vars"
    _endpoint_being_tested = "vars"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]
        self._variable_test_key = "terrasnek_unittest_key"
        self._variable_test_value = "terrasnek_unittest_value"

    def tearDown(self):
        self._api.workspaces.destroy(
            workspace_name=self._ws["data"]["attributes"]["name"])

    def test_vars(self):
        """
        Test the Variables API endpoints.
        """

        create_variable_payload = self._get_variable_create_payload(
            self._variable_test_key, self._variable_test_value, self._ws_id)

        # Create the variable and assert the key/value pair is the same as defined
        variable = self._api.vars.create(create_variable_payload)["data"]
        variable_value = variable["attributes"]["value"]
        self.assertEqual(self._variable_test_key,
                         variable["attributes"]["key"])
        self.assertEqual(self._variable_test_value, variable_value)

        # List the variables and make sure they match the updated payload
        original_variable_id = variable["id"]
        variables = self._api.vars.list(self._ws_name)["data"]
        self.assertEqual(original_variable_id, variables[0]["id"])

        # Now change the value of that variable
        updated_value = "changed"
        update_variable_payload = {
            "data": {
                "id": original_variable_id,
                "attributes": {
                    "key": self._variable_test_key,
                    "value": updated_value,
                    "category": "terraform",
                    "hcl": False,
                    "sensitive": False
                },
                "type": "vars"
            }
        }
        updated_variable = self._api.vars.update(
            original_variable_id, update_variable_payload)["data"]
        self.assertEqual(
            updated_variable["attributes"]["value"], updated_value)

        # Delete the variable and confirm it's gone
        self._api.vars.destroy(original_variable_id)
        variables = self._api.vars.list(self._ws_name)["data"]
        self.assertEqual(len(variables), 0)
