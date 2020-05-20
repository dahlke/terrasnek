"""
Module for Terraform Cloud API Endpoint: Registry Modules.
"""

import time

from .base import TestTFCBaseTestCase


# TODO: standardize and move to constants file
MAX_ATTEMPTS = 30
TFE_MODULE_PROVIDER_TYPE = "tfe"

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

        # TODO: comments
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

        # Give some time for the module to be created properly
        listed_modules_resp = self._api.registry_modules.list()

        # TODO: standardize this timeout behavior
        attempt_num = 0
        while not listed_modules_resp:
            listed_modules_resp = self._api.registry_modules.list()
            attempt_num += 1
            if attempt_num >= MAX_ATTEMPTS:
                break
            time.sleep(1)

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

        # Get the module, compare to the published module name
        gotten_module = \
            self._api.registry_modules.get(\
                published_module_name, TFE_MODULE_PROVIDER_TYPE, listed_version)
        self.assertEqual(published_module_name, gotten_module["name"])

        self._api.registry_modules.destroy(\
            published_module_name, TFE_MODULE_PROVIDER_TYPE, listed_version)
        gotten_module = \
            self._api.registry_modules.get(\
                published_module_name, TFE_MODULE_PROVIDER_TYPE, listed_version)
        self.assertIsNone(gotten_module)
