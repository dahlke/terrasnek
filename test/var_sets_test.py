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

    def tearDown(self):
        self._api.workspaces.destroy(
            workspace_name=self._ws["data"]["attributes"]["name"])

    def test_var_sets(self):
        """
        Test the Variable Sets API endpoints.
        """
        # list_for_org
        listed_org_var_sets = self._api.var_sets.list_for_org()
        print(listed_org_var_sets)

        # create

        # list_for_org

        # update

        # show

        # add_var_to_varset

        # list_vars_in_varset

        # update_var_in_varset

        # show_var_in_varset

        # apply_varset_to_workspace

        # remove_varset_from_workspace

        # delete_var_from_varset

        # show

        # destroy

