"""
Module for testing the Terraform Cloud API Endpoint: Registry Providers.
"""

from .base import TestTFCBaseTestCase


class TestTFCRegistryProviders(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Registry Providers.
    """

    _unittest_name = "prov"
    _endpoint_being_tested = "registry_providers"

    def test_providers(self):
        """
        Test the Registry Providers API endpoints.
        """

        # List all the providers in the org, confirm there are none
        listed_providers = self._api.registry_providers.list()["data"]
        self.assertEqual(len(listed_providers), 0)

        # Create a provider, confirm there is one provider
        create_payload = {
            "data": {
                "type": "registry-providers",
                "attributes": {
                    "name": "aws",
                    "namespace": "hashicorp",
                    "registry-name": "public"
                }
            }
        }
        created_provider = self._api.registry_providers.create(create_payload)["data"]
        created_provider_id = created_provider["id"]
        created_provider_registry_name = created_provider["attributes"]["registry-name"]
        created_provider_namespace = created_provider["attributes"]["namespace"]
        created_provider_name = created_provider["attributes"]["name"]

        # Confirm there is one provider after creating one
        listed_providers = self._api.registry_providers.list()["data"]
        self.assertEqual(len(listed_providers), 1)

        # Confirm there is one provider after creating one with list all
        all_listed_providers = self._api.registry_providers.list_all()["data"]
        self.assertEqual(len(all_listed_providers), 1)

        # Show the provider
        shown_provider = self._api.registry_providers.show(\
            created_provider_registry_name, created_provider_namespace, created_provider_name)["data"]
        # Confirm the shown provider matches the created provider ID
        self.assertEqual(shown_provider["id"], created_provider_id)

        # Destroy the created provider
        self._api.registry_providers.destroy(\
            created_provider_registry_name, created_provider_namespace, created_provider_name)

        # List the providers and confirm there are none
        listed_providers = self._api.registry_providers.list()["data"]
        self.assertEqual(len(listed_providers), 0)
