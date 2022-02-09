"""
Module for testing the Terraform Cloud API Endpoint: Org Tags.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrgTags(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Org Tags.
    """

    _unittest_name = "org-tag"
    _endpoint_being_tested = "org_tags"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]
        self._ws_name = self._ws["data"]["attributes"]["name"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_name)

    def test_org_tags(self):
        """
        Test the Org Tags API endpoints.
        """

        # Add tags to the workspace created in setup
        _ws_add_payload = {
            "data": [
                {
                    "type": "tags",
                    "attributes": {
                        "name": "foo"
                    }
                }
            ]
        }

        self._api.workspaces.add_tags(self._ws_id, _ws_add_payload)

        # Get the tags that were added, confirm both were created.
        org_tags = self._api.org_tags.list_tags()["data"]
        tag_id = org_tags[0]["id"]
        self.assertEqual(len(org_tags), len(_ws_add_payload["data"]))

        # Add one of the tags to workspace 1, confirm it has been attached.
        add_ws_to_tag_payload = {
            "data": [
                {
                    "type": "workspaces",
                    "id": self._ws_id
                }
            ]
        }
        self._api.org_tags.add_workspaces_to_tag(tag_id, add_ws_to_tag_payload)
        ws_tags = self._api.workspaces.list_tags(self._ws_id)["data"]
        self.assertEqual(len(ws_tags), 1)

        # Delete both of the tags and confirm that workspace 0 no longer has the tags.
        delete_tags_payload = {
            "data": [
                {
                    "type": "tags",
                    "id": tag_id
                }
            ]
        }
        self._api.org_tags.delete_tags(delete_tags_payload)
        ws_tags = self._api.workspaces.list_tags(self._ws_id)["data"]
        self.assertEqual(len(ws_tags), 0)
