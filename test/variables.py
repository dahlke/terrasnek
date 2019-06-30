import unittest
import os
from .base import TestTFEBaseTestCase

from tfepy.api import TFE


class TestTFEVariables(TestTFEBaseTestCase):

    @classmethod
    def setUpClass(self):
        super(TestTFEVariables, self).setUpClass()
        # TODO: How to manage VCS OAuth and create w/ VCS payload?
        self._ws = self._api.workspaces.create(self._ws_create_without_vcs_payload)
        self._variable_test_key = "terrasnek_unittest_key"
        self._variable_test_value = "terrasnek_unittest_value"

    @classmethod
    def tearDownClass(self):
        self._api.workspaces.destroy(workspace_name=self._ws["data"]["attributes"]["name"])

    def test_variables_lifecycle(self):
        ws_id = self._ws["data"]["id"]
        ws_name = self._ws["data"]["attributes"]["name"]

        create_variable_payload = self._get_create_variable_payload(self._variable_test_key, self._variable_test_value, ws_id)

        # Create the variable and assert the key/value pair is the same as defined
        variable = self._api.variables.create(create_variable_payload)["data"]
        variable_value = variable["attributes"]["value"]
        self.assertEqual(self._variable_test_key, variable["attributes"]["key"])
        self.assertEqual(self._variable_test_value, variable_value)

        # List the variables and make sure they match the updated payload
        original_variable_id = variable["id"]
        variables = self._api.variables.ls(ws_name)["data"]
        self.assertEqual(original_variable_id, variables[0]["id"])

        # Now change the value of that variable
        updated_value = "changed"
        # TODO: Make dicts return values of functions of the base test
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
        updated_variable = self._api.variables.update(original_variable_id, update_variable_payload)["data"]
        self.assertEqual(updated_variable["attributes"]["value"], updated_value)

        # Delete the variable and confirm it's gone
        self._api.variables.destroy(original_variable_id)
        variables = self._api.variables.ls(ws_name)["data"]
        self.assertEqual(len(variables), 0)