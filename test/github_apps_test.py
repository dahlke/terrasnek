"""
Module for testing the Terraform Cloud API Endpoint: GitHub Apps.
"""

from .base import TestTFCBaseTestCase


class TestTFCGitHubApps(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: GitHub Apps.
    """

    _unittest_name = "gitap"
    _endpoint_being_tested = "github_apps"

    def test_github_apps(self):
        """
        Test the GitHub Apps API endpoints.
        """
        listed_gh_apps = self._api.github_apps.list()["data"]
        gh_app_id = listed_gh_apps[0]["id"]
        self.assertTrue(len(listed_gh_apps) > 0)

        shown_gh_app = self._api.github_apps.show(gh_app_id)["data"]
        self.assertEqual(gh_app_id, shown_gh_app["id"])
