"""
Module for testing the Terraform Cloud API Endpoint: Run Triggers.
"""

from .base import TestTFCBaseTestCase

RUN_TRIGGER_TYPE = "inbound"

class TestTFCRunTriggers(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Run Triggers.
    """

    _unittest_name = "run-trig"
    _endpoint_being_tested = "run_triggers"

    def setUp(self):
        self._source_ws = self._api.workspaces.create(self._get_ws_without_vcs_create_payload())
        self._source_ws_id = self._source_ws["data"]["id"]
        self._source_ws_name = self._source_ws["data"]["attributes"]["name"]

        self._target_ws = self._api.workspaces.create(self._get_ws_without_vcs_create_payload())
        self._target_ws_id = self._target_ws["data"]["id"]
        self._target_ws_name = self._target_ws["data"]["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(
            workspace_name=self._source_ws_name)
        self._api.workspaces.destroy(
            workspace_name=self._target_ws_name)

    def test_run_triggers(self):
        """
        Test the Run Triggers API endpoints.
        """

        test_filters = [
            {
                "keys": ["run-trigger", "type"],
                "value": RUN_TRIGGER_TYPE
            }
        ]

        # List the triggers and confirm there are none
        all_triggers = self._api.run_triggers.list(self._target_ws_id, filters=test_filters)["data"]
        self.assertEqual(len(all_triggers), 0)

        # Create a trigger
        create_payload = {
            "data": {
                "relationships": {
                    "sourceable": {
                        "data": {
                            "id": self._source_ws_id,
                            "type": "workspaces"
                        }
                    }
                }
            }
        }
        created_trigger = self._api.run_triggers.create(self._target_ws_id, create_payload)["data"]
        created_trigger_id = created_trigger["id"]

        # List the triggers again and confirm there is one
        all_triggers = self._api.run_triggers.list(self._target_ws_id, filters=test_filters)["data"]
        self.assertEqual(len(all_triggers), 1)

        # Show the run trigger by id, compare to our created ID
        shown_trigger = self._api.run_triggers.show(created_trigger_id)["data"]
        shown_trigger_id = shown_trigger["id"]
        self.assertEqual(shown_trigger_id, created_trigger_id)

        # Destroy the run trigger, confirm that we have zero run triggers again
        self._api.run_triggers.destroy(created_trigger_id)
        all_triggers = self._api.run_triggers.list(self._target_ws_id, filters=test_filters)["data"]
        self.assertEqual(len(all_triggers), 0)
