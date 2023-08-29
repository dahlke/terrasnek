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
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]
        self._variable_test_key = "terrasnek_unittest_key"
        self._variable_test_value = "terrasnek_unittest_value"

        self._project = self._api.projects.create(self._get_project_create_payload())
        self._project_id = self._project["data"]["id"]

    def tearDown(self):
        self._api.workspaces.destroy(
            workspace_name=self._ws["data"]["attributes"]["name"])

    def test_var_sets(self):
        """
        Test the Variable Sets API endpoints.
        """

        # List all the varsets in the org, confirm there are none
        listed_org_var_sets = self._api.var_sets.list_for_org()["data"]
        self.assertEqual(len(listed_org_var_sets), 0)

        all_listed_org_var_sets = self._api.var_sets.list_all_for_org()["data"]
        self.assertEqual(len(all_listed_org_var_sets), 0)

        # Setup a create payload that has no workspaces or variables attached.
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
        new_var_set_name = "terrasnek-varset-updated"
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

        # Add a variable to the created variable set, confirm it's been added
        add_var_to_varset_payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": self._variable_test_key,
                    "value": self._variable_test_value,
                    "description": "foo",
                    "sensitive": False,
                    "category": "terraform",
                    "hcl": False
                }
            }
        }
        added_var = self._api.var_sets.add_var_to_varset(created_var_set_id, add_var_to_varset_payload)["data"]
        added_var_id = added_var["id"]
        self.assertEqual(added_var["attributes"]["key"], self._variable_test_key)

        # List the variables in the variable set, confirm the one that was just added is present
        listed_vars = self._api.var_sets.list_vars_in_varset(created_var_set_id)["data"]
        self.assertEqual(listed_vars[0]["attributes"]["key"], self._variable_test_key)

        # Update the value of the variable that was just added, confirm that the update took place
        updated_value = "foo"
        update_var_in_varset_payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": self._variable_test_key,
                    "value": updated_value,
                    "description": "new cheeeese",
                    "sensitive": False,
                    "category": "terraform",
                    "hcl": False
                }
            }
        }
        updated_var = self._api.var_sets.update_var_in_varset(\
            created_var_set_id, added_var_id, update_var_in_varset_payload)["data"]
        self.assertEqual(updated_var["attributes"]["value"], updated_value)

        # Apply the variable set to the workspace
        apply_varset_ws_payload = {
            "data": [
                {
                    "type": "workspaces",
                    "id": self._ws_id
                }
            ]
        }
        # There is no response when we apply a varset to a workspace
        self._api.var_sets.apply_varset_to_workspace(created_var_set_id, apply_varset_ws_payload)

        # Confirm the applied variable set is present on the workspace
        listed_workspace_varsets = self._api.var_sets.list_for_workspace(self._ws_id)["data"]
        self.assertEqual(listed_workspace_varsets[0]["id"], created_var_set_id)

        all_listed_workspace_varsets = self._api.var_sets.list_all_for_workspace(self._ws_id)["data"]
        self.assertEqual(all_listed_workspace_varsets[0]["id"], created_var_set_id)

        # Remove the variable set from the workspace
        remove_varset_payload = {
            "data": [
                {
                    "type": "workspaces",
                    "id": self._ws_id
                }
            ]
        }
        # There is no response when we remove a varset from a workspace
        self._api.var_sets.remove_varset_from_workspace(created_var_set_id, remove_varset_payload)

        # Confirm that there are no longer any varsets attached to the workspace
        listed_workspace_varsets = self._api.var_sets.list_for_workspace(self._ws_id)["data"]
        self.assertEqual(len(listed_workspace_varsets), 0)

        # Delete the variable added from the variable set and confirm it's gone
        self._api.var_sets.delete_var_from_varset(created_var_set_id, added_var_id)

        # Apply the variable set to a project
        varset_proj_payload = {
            "data": [
                {
                    "type": "projects",
                    "id": self._project_id
                }
            ]
        }
        self._api.var_sets.apply_varset_to_project(created_var_set_id, varset_proj_payload)
        # Confirm the variable set is attached to the project
        shown_var_set = self._api.var_sets.show(created_var_set_id)["data"]
        self.assertEqual(len(shown_var_set["relationships"]["projects"]["data"]), 1)
        # Remove the variable set from the project
        self._api.var_sets.remove_varset_from_project(created_var_set_id, varset_proj_payload)
        # Confirm the variable set is no longer attached to the project
        shown_var_set = self._api.var_sets.show(created_var_set_id)["data"]
        self.assertEqual(len(shown_var_set["relationships"]["projects"]["data"]), 0)

        # Destroy the variable set that was created earlier
        # There is no response when we destroy a variable set
        self._api.var_sets.destroy(created_var_set_id)

        # Confirm we no longer have any varsets
        listed_var_sets = self._api.var_sets.list_for_org()["data"]
        self.assertEqual(len(listed_var_sets), 0)
