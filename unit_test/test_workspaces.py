"""
Unit tests for the workspaces module.
"""
import json
from unittest import TestCase, mock
from unittest.mock import patch, call, PropertyMock
from terrasnek.api import TFC


class TestWorkspaces(TestCase):
    """
    Unit tests for the workspaces module.
    """

    def setUp(self) -> None:
        self.api = TFC("test_token", verify=True)  # type: ignore
        self.api.set_org("test_org")
        self.common_args = {
            "headers": {
                "Authorization": "Bearer test_token",
                "User-Agent": "terrasnek-0.1.10",
                "Content-Type": "application/vnd.api+json",
            },
            "verify": True,
        }

    def test_workspace_create(self):
        """
        Test the workspaces create API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps(
                {}
            )  # we just need json.loads() to not raise an exception
            mock_requests.post.return_value = mock_response

            self.api.workspaces.create(
                {"data": {"attributes": {"name": "test_workspace"}}}
            )

            mock_requests.post.assert_called_once_with(
                "https://app.terraform.io/api/v2/organizations/test_org/workspaces",
                **self.common_args,
                data=json.dumps({"data": {"attributes": {"name": "test_workspace"}}}),
            )

    def test_workspace_destroy(self):
        """
        Test the workspaces destroy API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.delete.return_value = mock_response

            self.api.workspaces.destroy("test_workspace_id")

            mock_requests.delete.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/test_workspace_id",
                **self.common_args,
                data=json.dumps(None),
            )

    def test_workspace_force_unlock(self):
        """
        Test the workspace force unlock API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.post.return_value = mock_response

            self.api.workspaces.force_unlock("test_workspace_id")

            mock_requests.post.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/test_workspace_id/actions/force-unlock",
                **self.common_args,
                data=json.dumps(None),
            )

    def test_workspace_lock(self):
        """
        Test the workspace lock API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.post.return_value = mock_response

            self.api.workspaces.lock(
                "test_workspace_id", {"data": {"attributes": {"reason": "test_reason"}}}
            )

            mock_requests.post.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/test_workspace_id/actions/lock",
                **self.common_args,
                data=json.dumps({"data": {"attributes": {"reason": "test_reason"}}}),
            )

    def test_workspace_list(self):
        """
        Test the workspaces API endpoints.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            self.common_args["allow_redirects"] = False

            self.api.workspaces.list()
            mock_requests.get.assert_called_once_with(
                "https://app.terraform.io/api/v2/organizations/test_org/workspaces",
                **self.common_args,
            )

    def test_workspace_list_all(self):
        """
        Test the workspaces list all API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            self.common_args["allow_redirects"] = False

            mock_response_content = PropertyMock(
                side_effect=[
                    # json.dumps() on a dict is less error-prone than hand-crafting a string
                    json.dumps(
                        {
                            "meta": {
                                "pagination": {
                                    "current-page": 1,
                                    "next-page": 2,
                                    "prev-page": None,
                                    "total-pages": 2,
                                    "total-count": 2,
                                },
                            },
                            "data": [
                                {
                                    "id": "ws-123456",
                                    "type": "workspaces",
                                    "attributes": {
                                        "name": "test_workspace",
                                        "created-at": "2020",
                                    },
                                }
                            ],
                        },
                    ),
                    json.dumps(
                        {
                            "meta": {
                                "pagination": {
                                    "current-page": 2,
                                    "next-page": None,
                                    "prev-page": 1,
                                    "total-pages": 2,
                                    "total-count": 2,
                                },
                            },
                            "data": [
                                {
                                    "id": "ws-123457",
                                    "type": "workspaces",
                                    "attributes": {
                                        "name": "test_workspace",
                                        "created-at": "2020",
                                    },
                                }
                            ],
                        },
                    ),
                ]
            )

            mock_response = mock.Mock()
            mock_response.status_code = 200
            type(mock_response).content = mock_response_content
            mock_requests.get.return_value = mock_response

            self.api.workspaces.list_all()
            mock_requests.get.assert_has_calls(
                [
                    call(
                        "https://app.terraform.io/api/v2/organizations/test_org/workspaces?page[number]=1&page["
                        "size]=100",
                        **self.common_args,
                    ),
                    call(
                        "https://app.terraform.io/api/v2/organizations/test_org/workspaces?page[number]=2&page["
                        "size]=100",
                        **self.common_args,
                    ),
                ],
                any_order=True,
            )

    def test_workspace_show(self):
        """
        Test the workspaces show API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            self.common_args["allow_redirects"] = False

            self.api.workspaces.show("test_workspace_id")
            mock_requests.get.assert_called_once_with(
                "https://app.terraform.io/api/v2/organizations/test_org/workspaces/test_workspace_id",
                **self.common_args,
            )

    def test_workspace_unlock(self):
        """
        Test the workspace unlock API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.post.return_value = mock_response

            self.api.workspaces.unlock("test_workspace_id")

            mock_requests.post.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/test_workspace_id/actions/unlock",
                **self.common_args,
                data=json.dumps(None),
            )

    def test_workspace_update(self):
        """
        Test the workspaces update API endpoint using workspace_id.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.patch.return_value = mock_response

            self.api.workspaces.update(
                payload={"data": {"attributes": {"name": "test_workspace"}}},
                workspace_id="ws-123456",
            )

            mock_requests.patch.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456",
                **self.common_args,
                data=json.dumps({"data": {"attributes": {"name": "test_workspace"}}}),
            )

    def test_workspace_update_workspace_name(self):
        """
        Test the workspaces update API endpoint using workspace_name.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.patch.return_value = mock_response

            self.api.workspaces.update(
                payload={"data": {"attributes": {"name": "test_workspace"}}},
                workspace_name="test_workspace",
            )

            mock_requests.patch.assert_called_once_with(
                "https://app.terraform.io/api/v2/organizations/test_org/workspaces/test_workspace",
                **self.common_args,
                data=json.dumps({"data": {"attributes": {"name": "test_workspace"}}}),
            )

    def test_assign_ssh_key(self):
        """
        Test the assign ssh key API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.patch.return_value = mock_response

            self.api.workspaces.assign_ssh_key(
                workspace_id="ws-123456",
                payload={
                    "data": {
                        "attributes": {"id": "sshkey-123456"},
                        "type": "workspaces",
                    },
                },
            )

            mock_requests.patch.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/ssh-key",
                **self.common_args,
                data=json.dumps(
                    {
                        "data": {
                            "attributes": {"id": "sshkey-123456"},
                            "type": "workspaces",
                        },
                    }
                ),
            )

    def test_unassign_ssh_key(self):
        """
        Test the unassign ssh key API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.patch.return_value = mock_response

            self.api.workspaces.unassign_ssh_key(
                workspace_id="ws-123456",
                payload={
                    "data": {
                        "attributes": {
                            "id": None,
                        },
                        "type": "workspaces",
                    },
                },
            )

            mock_requests.patch.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/ssh-key",
                **self.common_args,
                data=json.dumps(
                    {"data": {"attributes": {"id": None}, "type": "workspaces"}}
                ),
            )

    def test_get_remote_state_consumers(self):
        """
        Test the get remote state consumers API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            self.common_args["allow_redirects"] = False

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.get.return_value = mock_response

            self.api.workspaces.get_remote_state_consumers(
                workspace_id="ws-123456",
            )

            mock_requests.get.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/remote-state-consumers",
                **self.common_args,
            )

    def test_replace_remote_state_consumers(self):
        """
        Test the replace remote state consumers API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.patch.return_value = mock_response

            self.api.workspaces.replace_remote_state_consumers(
                workspace_id="ws-123456",
                payload={
                    "data": [
                        {
                            "id": "ws-123456",
                            "type": "workspaces",
                        }
                    ]
                },
            )

            mock_requests.patch.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/remote-state-consumers",
                **self.common_args,
                data=json.dumps(
                    {
                        "data": [
                            {
                                "id": "ws-123456",
                                "type": "workspaces",
                            }
                        ]
                    }
                ),
            )

    def test_delete_remote_state_consumers(self):
        """
        Test the delete remote state consumers API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.delete.return_value = mock_response

            self.api.workspaces.delete_remote_state_consumers(
                workspace_id="ws-123456",
                payload={
                    "data": [
                        {
                            "id": "ws-123456",
                            "type": "workspaces",
                        }
                    ]
                },
            )

            mock_requests.delete.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/remote-state-consumers",
                **self.common_args,
                data=json.dumps(
                    {
                        "data": [
                            {
                                "id": "ws-123456",
                                "type": "workspaces",
                            }
                        ]
                    }
                ),
            )

    def test_list_tags(self):
        """
        Test the list tags API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.get.return_value = mock_response

            self.api.workspaces.list_tags(
                workspace_id="ws-123456",
            )

            mock_requests.get.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/tags",
                **self.common_args,
                allow_redirects=False,
            )

    def test_list_all_tags(self):
        """
        Test the list all tags API endpoint.
        """
        pass

    def test_add_tags(self):
        """
        Test the add tags API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.post.return_value = mock_response

            self.api.workspaces.add_tags(
                workspace_id="ws-123456",
                payload={
                    "data": [
                        {
                            "id": "tag-123456",
                            "type": "tags",
                        }
                    ]
                },
            )

            mock_requests.post.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/tags",
                **self.common_args,
                data=json.dumps(
                    {
                        "data": [
                            {
                                "id": "tag-123456",
                                "type": "tags",
                            }
                        ]
                    }
                ),
            )

    def test_remove_tags(self):
        """
        Test the remove tags API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.content = json.dumps({})

            mock_requests.delete.return_value = mock_response

            self.api.workspaces.remove_tags(
                workspace_id="ws-123456",
                payload={
                    "data": [
                        {
                            "id": "tag-123456",
                            "type": "tags",
                        }
                    ]
                },
            )

            mock_requests.delete.assert_called_once_with(
                "https://app.terraform.io/api/v2/workspaces/ws-123456/relationships/tags",
                **self.common_args,
                data=json.dumps(
                    {
                        "data": [
                            {
                                "id": "tag-123456",
                                "type": "tags",
                            }
                        ]
                    }
                ),
            )

    def test_list_all_resources(self):
        """
        Test the list all resources API endpoint.
        """

        # patch the requests module in the endpoint
        with patch.object(self.api.workspaces, "_session") as mock_requests:

            # mock response to return "status_code" 200 and "json" data
            mock_response = mock.Mock()
            mock_response.status_code = 200
            # We should test that pagination is working at some point.
            mock_response.content = json.dumps(
                {
                    "meta": {
                        "pagination": {
                            "current-page": 1,
                            "next-page": 2,
                            "prev-page": None,
                            "total-pages": 2,
                            "total-count": 2,
                        },
                    },
                    "data": [
                        {
                            "id": "ws-123456",
                            "type": "workspaces",
                            "attributes": {
                                "name": "default",
                                "description": "Default workspace",
                                "created-at": "2019-01-01T00:00:00.000Z",
                            },
                        },
                        {
                            "id": "ws-123457",
                            "type": "workspaces",
                            "attributes": {
                                "name": "dev",
                                "description": "Development workspace",
                                "created-at": "2019-01-01T00:00:00.000Z",
                            },
                        },
                    ],
                }
            )

            mock_requests.get.return_value = mock_response

            resp = self.api.workspaces.list_all_resources(
                workspace_id="ws-123456",
            )

            mock_requests.get.assert_has_calls(
                [
                    mock.call(
                        "https://app.terraform.io/api/v2/workspaces/ws-123456/resources?page[number]=1&page[size]=100",
                        **self.common_args,
                        allow_redirects=False,
                    ),
                    mock.call(
                        "https://app.terraform.io/api/v2/workspaces/ws-123456/resources?page[number]=2&page[size]=100",
                        **self.common_args,
                        allow_redirects=False,
                    ),
                ]
            )
