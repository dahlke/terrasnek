"""
Module for testing the Terraform Cloud API Endpoint: Run Triggers.
"""

from .base import TestTFCBaseTestCase

RUN_TRIGGER_TYPE = "inbound"

class TestTFCRunTriggers(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Run Triggers.
    """

    def setUp(self):
        self._source_ws = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("run-trig"))
        self._source_ws_id = self._source_ws["data"]["id"]
        self._source_ws_name = self._source_ws["data"]["attributes"]["name"]

        self._target_ws = self._api.workspaces.create(
            self._get_ws_without_vcs_create_payload("run-trig"))
        self._target_ws_id = self._target_ws["data"]["id"]
        self._target_ws_name = self._target_ws["data"]["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(
            workspace_name=self._source_ws_name)
        self._api.workspaces.destroy(
            workspace_name=self._target_ws_name)

    def test_run_triggers_lifecycle(self):
        """
        Test the Run Triggers API endpoints: create, list, update, destroy.
        """

        test_filters = [
            {
                "keys": ["run-trigger", "type"],
                "value": RUN_TRIGGER_TYPE
            }
        ]

        # List the triggers and confirm there are none
        triggers_resp = self._api.run_triggers.list(self._target_ws_id, filters=test_filters)
        triggers = triggers_resp["data"]
        self.assertEqual(len(triggers), 0)

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

        created_trigger_resp = self._api.run_triggers.create(self._target_ws_id, create_payload)
        created_trigger_id = created_trigger_resp["data"]["id"]

        # List the triggers again and confirm there is one
        triggers_resp = self._api.run_triggers.list(self._target_ws_id, filters=test_filters)
        triggers = triggers_resp["data"]
        self.assertEqual(len(triggers), 1)

        # Show the run trigger by id, compare to our created ID
        shown_trigger_resp = self._api.run_triggers.show(created_trigger_id)
        shown_trigger = shown_trigger_resp["data"]
        shown_trigger_id = shown_trigger["id"]
        self.assertEqual(shown_trigger_id, created_trigger_id)

        # Destroy the run trigger, confirm that we have zero run triggers again
        self._api.run_triggers.destroy(created_trigger_id)
        triggers_resp = self._api.run_triggers.list(self._target_ws_id, filters=test_filters)
        triggers = triggers_resp["data"]
        self.assertEqual(len(triggers), 0)
