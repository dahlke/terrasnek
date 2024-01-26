"""
Module for testing the Terraform Cloud API Endpoint: Config Versions.
"""

import time

from .base import TestTFCBaseTestCase


class TestTFCConfigVersions(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Config Versions.
    """

    _unittest_name = "cnf-ver"
    _endpoint_being_tested = "config_versions"

    def setUp(self):
        self._ws = self._api.workspaces.create(self._get_ws_no_vcs_create_payload())
        self._ws_id = self._ws["data"]["id"]

        oauth_client = self._api.oauth_clients.create(self._get_oauth_client_create_payload())
        self._oauth_client_id = oauth_client["data"]["id"]
        oauth_token_id = oauth_client["data"]["relationships"]["oauth-tokens"]["data"][0]["id"]

        ws_payload = self._get_ws_with_vcs_create_payload(oauth_token_id, working_dir="tfe")
        self._ws_w_vcs = self._api.workspaces.create(ws_payload)
        self._ws_w_vcs_id = self._ws_w_vcs["data"]["id"]

    def tearDown(self):
        self._api.workspaces.destroy(workspace_id=self._ws_id)
        self._api.workspaces.destroy(workspace_id=self._ws_w_vcs_id)
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_config_versions(self):
        """
        Test the Config Versions API endpoints.
        """

        # two upload methods to test; use a different 1st positional argument for each test
        upload_tests = (
            (self._api.config_versions.upload, self._config_version_upload_tarball_path),
            (self._api.config_versions.upload_from_string, self._config_version_upload_string),
        )
        for upload_handle, source in upload_tests:

            with self.subTest():
                # Create a new config version
                created_config_version = self._api.config_versions.create(
                    self._ws_id, self._get_config_version_create_payload())["data"]
                cv_id = created_config_version["id"]

                # List all of the config versions for the workspace
                config_versions = self._api.config_versions.list(self._ws_id)["data"]

                # Confirm we found the newly created config version
                found_conf_ver = False
                for conf_ver in config_versions:
                    if cv_id == conf_ver["id"]:
                        found_conf_ver = True
                        break
                self.assertTrue(found_conf_ver)

                # Confirm the config version status is pending and the IDs match on show
                shown_config_version = self._api.config_versions.show(cv_id)["data"]
                self.assertEqual(shown_config_version["attributes"]["status"], "pending")
                self.assertEqual(shown_config_version["id"], cv_id)

                # Upload the .tf code and confirm it's been uploaded
                upload_url = created_config_version["attributes"]["upload-url"]
                upload_handle(source, upload_url)

                # Give 2 seconds for the upload to register
                time.sleep(2)
                config_versions = self._api.config_versions.list(self._ws_id)["data"]
                self.assertEqual(config_versions[0]["attributes"]["status"], "uploaded")

                all_config_versions = self._api.config_versions.list_all(self._ws_id)
                found_conf_ver = False
                for conf_ver in all_config_versions["data"]:
                    if cv_id == conf_ver["id"]:
                        found_conf_ver = True
                        break
                self.assertTrue(found_conf_ver)

                # Get the run that was created when we uploaded a config version
                run_id = self._api.runs.list(self._ws_id)["data"][0]["id"]
                self._created_run_timeout(run_id)

                download_config_version = \
                    self._api.config_versions.download_version_files(config_version_id=cv_id)
                self.assertIn("redirected", download_config_version)

                download_config_version_run = \
                    self._api.config_versions.download_version_files(run_id=run_id)
                self.assertIn("redirected", download_config_version_run)

                # TODO: archiving doesn't work with the string created config version, so this needs to be updated.
                """
                # Trigger an apply so we can get a config version ID
                print("start apply")
                apply_payload = {
                    "comment": "foo"
                }
                self._api.runs.apply(run_id, apply_payload)
                self._applied_run_timeout(run_id)
                print("end apply")

                # Create a second config version so that we can archive the first one
                self._api.config_versions.create(self._ws_id, self._get_config_version_create_payload())
                self._api.config_versions.archive_version(cv_id)
                config_versions = self._api.config_versions.list(self._ws_id)["data"]
                print(config_versions)

                self.assertEqual(config_versions[-1]["attributes"]["status"], "archived")
                """

    def test_config_versions_includes(self):
        """
        Test the related resources for the Config Versions API endpoints (requires VCS).
        """
        config_versions_raw = self._api.config_versions.list(self._ws_w_vcs_id, \
            include=["ingress-attributes"])
        self.assertIn("included", config_versions_raw)

        # Grab the config version ID from the list, and show it.
        cv_id = config_versions_raw["data"][0]["id"]
        shown_config_version_raw = self._api.config_versions.show(cv_id, \
            include=["ingress_attributes"])
        # Confirm we get the related resources.
        self.assertIn("included", shown_config_version_raw)

        # TODO: these are only available on the TFE API, so we can't test them yet
        # marked = self._api.config_versions.mark_for_garbage_collection(cv_id)["data"]
        # unmarked = self._api.config_versions.restore_marked_for_garbage_collection(cv_id)["data"]
        # permanently_deleted = self._api.config_versions.permanently_delete_config_version(cv_id)["data"]

        # Show the commit information for the config version
        shown_commit_info = self._api.config_versions.show_commit_info(cv_id)["data"]
        self.assertIn("github", shown_commit_info["attributes"]["commit-url"])

        all_config_versions_raw = self._api.config_versions.list_all(self._ws_w_vcs_id, \
            include=["ingress-attributes"])
        self.assertIn("included", all_config_versions_raw)
