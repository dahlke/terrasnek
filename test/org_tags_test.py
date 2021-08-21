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
        self._ws_0 = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_0_id = self._ws_0["data"]["id"]
        self._ws_0_name = self._ws_0["data"]["attributes"]["name"]

        self._ws_1 = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_1_id = self._ws_1["data"]["id"]
        self._ws_1_name = self._ws_1["data"]["attributes"]["name"]

        self._ws_0_add_tags_payload = {
            "data": [
                {
                    "type": "tags",
                    "attributes": {
                        "name": "foo"
                    }
                },
                {
                    "type": "tags",
                    "attributes": {
                        "name": "bar"
                    }
                }
            ]
        }

        self._api.workspaces.add_tags(self._ws_0_id, self._ws_0_add_tags_payload)

    def tearDown(self):
        self._api.workspaces.destroy(workspace_name=self._ws_0_name)
        self._api.workspaces.destroy(workspace_name=self._ws_1_name)

    def test_org_tags(self):
        """
        Test the Org Tags API endpoints.
        """
        # Get the tags that were added in the setup, confirm both were created.
        org_tags = self._api.org_tags.list_tags()["data"]
        tag_0_id = org_tags[0]["id"]
        tag_1_id = org_tags[1]["id"]
        self.assertEqual(len(org_tags), len(self._ws_0_add_tags_payload["data"]))

        # Add one of the tags to workspace 1, confirm it has been attached.
        add_ws_to_tag_payload = {
            "data": [
                {
                    "type": "workspaces",
                    "id": self._ws_1_id
                }
            ]
        }
        self._api.org_tags.add_workspaces_to_tag(tag_0_id, add_ws_to_tag_payload)
        ws_1_tags = self._api.workspaces.list_tags(self._ws_1_id)["data"]
        self.assertEqual(tag_0_id, ws_1_tags[0]["id"])

        """
        # FIXME: this isn't working properly, the tag is still present on the workspace
        # Remove that tag from workspace 1, confirm it has been removed.
        remove_ws_from_tag_payload = {
            "data": [
                {
                    "type": "workspaces",
                    "id": self._ws_1_id
                }
            ]
        }
        self._api.org_tags.remove_workspaces_from_tag(tag_0_id, remove_ws_from_tag_payload)
        ws_1_tags = self._api.workspaces.list_tags(self._ws_1_id)["data"]
        print(ws_1_tags)
        self.assertEqual(len(ws_1_tags), 0)
        """

        # Delete both of the tags and confirm that workspace 0 no longer has the tags.
        delete_tags_payload = {
            "data": [
                {
                    "type": "tags",
                    "id": tag_0_id
                },
                {
                    "type": "tags",
                    "id": tag_1_id
                }
            ]
        }
        self._api.org_tags.delete_tags(delete_tags_payload)
        ws_1_tags = self._api.workspaces.list_tags(self._ws_0_id)["data"]
        self.assertEqual(len(ws_1_tags), 0)
