"""
Module for Terraform Cloud API Endpoint: Registry Modules.
"""

import time
import os
import timeout_decorator

from terrasnek.exceptions import TFCDeprecatedWontFix
from .base import TestTFCBaseTestCase
from ._constants import TFE_MODULE_PROVIDER_TYPE, MAX_TEST_TIMEOUT

class TestTFCRegistryModules(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Registry Modules.
    """

    _unittest_name = "reg-mod"
    _endpoint_being_tested = "registry_modules"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        oauth_client = self._api.oauth_clients.create(\
            self._get_oauth_client_create_payload())["data"]
        self._oauth_client_id = oauth_client["id"]
        self._oauth_token_id = \
            oauth_client["relationships"]["oauth-tokens"]["data"][0]["id"]

    def tearDown(self):
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_registry_modules_vcs_publish(self):
        """
        Test the Registry Modules API endpoint: ``publish_from_vcs``, ``list``,
        ``search``, ``list_versions``, ``list_latest_version_all_providers``,
        ``list_latest_version_specific_provider``, ``get``.
        """

        # Publish a module from the VCS provider, using the oauth token generated
        # in the class setup. Assert that we got the expected response back.
        publish_payload = {
            "data": {
                "attributes": {
                    "vcs-repo": {
                        "identifier": "dahlke/terraform-tfe-terrasnek-unittest",
                        "oauth-token-id": self._oauth_token_id,
                        "display_identifier": "dahlke/terraform-tfe-terrasnek-unittest"
                    }
                },
                "type":"registry-modules"
            }
        }
        published_module = \
            self._api.registry_modules.publish_from_vcs(publish_payload)["data"]
        published_module_name = published_module["attributes"]["name"]
        self.assertEqual("registry-modules", published_module["type"])


        # Test the listing of the modules, time out if it takes too long.
        @timeout_decorator.timeout(MAX_TEST_TIMEOUT)
        def listed_modules_timeout():
            listed_modules_resp = self._api.registry_modules.list()
            while not listed_modules_resp:
                listed_modules_resp = self._api.registry_modules.list()
                time.sleep(1)
            return listed_modules_resp
        listed_modules_resp = listed_modules_timeout()

        # List all the modules for this org, confirm we found the one we
        # published.
        listed_modules = listed_modules_resp["modules"]
        found_module = False
        for module in listed_modules:
            if module["name"] == published_module_name:
                found_module = True
                break
        self.assertTrue(found_module)

        # Search for the module by name, confirm we got it back in the results.
        search_modules_resp = self._api.registry_modules.search(published_module_name)
        search_modules = search_modules_resp["modules"]
        found_module = False
        for module in search_modules:
            if module["name"] == published_module_name:
                found_module = True
                break
        self.assertTrue(found_module)

        # List the module versions, confirm that we got an expected response.
        listed_versions_resp = \
            self._api.registry_modules.list_versions(\
                published_module_name, TFE_MODULE_PROVIDER_TYPE)
        self.assertIn("modules", listed_versions_resp)
        listed_version = listed_modules_resp["modules"][0]["version"]

        # List the latest version for all providers, compare to the
        # published module version
        listed_latest_version_all_providers = \
            self._api.registry_modules.list_versions(\
                published_module_name, TFE_MODULE_PROVIDER_TYPE)
        latest_all_providers = listed_latest_version_all_providers["modules"][0]
        self.assertEqual(listed_version, latest_all_providers["versions"][0]["version"])

        # List the latest version for a specific provider, compare to the
        # published module version
        listed_latest_version_specific_provider = \
            self._api.registry_modules.list_versions(\
                published_module_name, TFE_MODULE_PROVIDER_TYPE)
        latest_specific_provider = listed_latest_version_specific_provider["modules"][0]
        self.assertEqual(listed_version, latest_specific_provider["versions"][0]["version"])

        # Download the source for a specific version of the module, confirm the file
        # was downloaded to the correct path (and then remove it).
        self._api.registry_modules.download_version_source(\
            published_module_name, TFE_MODULE_PROVIDER_TYPE, listed_version, \
            self._module_version_source_tarball_target_path)
        self.assertTrue(os.path.exists(self._module_version_source_tarball_target_path))
        if os.path.exists(self._module_version_source_tarball_target_path):
            os.remove(self._module_version_source_tarball_target_path)

        # Download the source for the latest version of the module, confirm the file
        # was downloaded to the correct path (and then remove it).
        self._api.registry_modules.download_latest_source(\
            published_module_name, TFE_MODULE_PROVIDER_TYPE, \
            self._module_latest_source_tarball_target_path)
        self.assertTrue(os.path.exists(self._module_latest_source_tarball_target_path))
        if os.path.exists(self._module_latest_source_tarball_target_path):
            os.remove(self._module_latest_source_tarball_target_path)

        # Get the module, compare to the published module name
        gotten_module = \
            self._api.registry_modules.get(\
                published_module_name, TFE_MODULE_PROVIDER_TYPE, listed_version)
        self.assertEqual(published_module_name, gotten_module["name"])

        # List all the provider versions for the module, confirm they are as expected.
        expected_provider = "tfe"
        latest_version_all_providers = \
            self._api.registry_modules.list_latest_version_all_providers(published_module_name)
        tfe_provider_data = latest_version_all_providers["modules"][0]
        self.assertEqual(tfe_provider_data["version"], "0.0.1")
        self.assertEqual(tfe_provider_data["provider"], expected_provider)

        # Confirm the latest version for specific providers endpoint works as expected
        latest_version_tfe_provider = \
            self._api.registry_modules.list_latest_version_specific_provider(\
                published_module_name, expected_provider)
        self.assertEqual(latest_version_tfe_provider["version"], "0.0.1")
        self.assertEqual(latest_version_tfe_provider["provider"], expected_provider)

        # Deleted the published module, confirm that it's gone.
        self._api.registry_modules.destroy(\
            published_module_name, TFE_MODULE_PROVIDER_TYPE, listed_version)
        gotten_module = \
            self._api.registry_modules.get(\
                published_module_name, TFE_MODULE_PROVIDER_TYPE, listed_version)
        self.assertIsNone(gotten_module)

        with self.assertRaises(TFCDeprecatedWontFix):
            self._api.registry_modules.create()

        with self.assertRaises(TFCDeprecatedWontFix):
            self._api.registry_modules.create_version()

        with self.assertRaises(TFCDeprecatedWontFix):
            self._api.registry_modules.upload_version()
