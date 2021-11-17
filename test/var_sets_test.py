"""
Module for testing the Terraform Cloud API Endpoint: Variable Sets.
"""

from .base import TestTFCBaseTestCase


class TestTFCVarSets(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Variable Sets.
    """

    _unittest_name = "vset"
    _endpoint_being_tested = "var_sets"

    def setUp(self):
        # self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        # self._ws_id = self._ws["data"]["id"]
        # self._ws_name = self._ws["data"]["attributes"]["name"]
        # self._variable_test_key = "terrasnek_unittest_key"
        # self._variable_test_value = "terrasnek_unittest_value"
        pass

    def tearDown(self):
        # self._api.workspaces.destroy(
            # workspace_name=self._ws["data"]["attributes"]["name"])
        pass

    def test_var_sets(self):
        """
        Test the Variable Sets API endpoints.
        """

        # List all the varsets in the org, confirm there are none
        listed_org_var_sets = self._api.var_sets.list_for_org()["data"]
        self.assertEqual(len(listed_org_var_sets), 0)

        # Setup a create payload that has no workspaces or variables attached.
        # TODO: purge all varsets from the test org.
        # TODO: create
        var_set_name = "terrasnek-unittest"
        create_payload = {
            "data": {
                "type": "varsets",
                "attributes": {
                    "name": var_set_name,
                    "description": "",
                    "is-global": False
                },
                "relationships": {
                    "workspaces": {
                        "data": [
                        ]
                    },
                    "vars": {
                        "data": [
                        ]
                    }
                }
            }
        }
        created_var_set = self._api.var_sets.create(create_payload)["data"]
        created_var_set_id = created_var_set["id"]
        self.assertEqual(var_set_name, created_var_set["attributes"]["name"])

        # Update the variable set and compare the names
        new_var_set_name = "terrasnek-unittest-updated"
        update_payload = {
            "data": {
                "type": "varsets",
                "attributes": {
                    "name": new_var_set_name,
                    "description": "",
                    "is-global": False
                },
                "relationships": {
                    "vars": {
                        "data": [
                        ]
                    }
                }
            }
        }
        updated_var_set = self._api.var_sets.update(created_var_set_id, update_payload)["data"]
        self.assertEqual(new_var_set_name, updated_var_set["attributes"]["name"])

        # Show the variable set and compare the names
        shown_var_set = self._api.var_sets.show(created_var_set_id)["data"]
        self.assertEqual(new_var_set_name, shown_var_set["attributes"]["name"])

        # TODO: add_var_to_varset

        # TODO: list_vars_in_varset

        # TODO: update_var_in_varset

        # TODO: show_var_in_varset

        # TODO: apply_varset_to_workspace

        # TODO: remove_varset_from_workspace

        # TODO: delete_var_from_varset

        # TODO: show

        # TODO: destroy

