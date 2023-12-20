"""
Module for testing the Terraform Cloud API Endpoint: No Code Provisioning.
"""

import time

from .base import TestTFCBaseTestCase
from ._constants import TFE_MODULE_PROVIDER_TYPE


class TestTFCNoCodeProvisioning(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: No Code Provisioning.
    """

    _unittest_name = "no-cde"
    _endpoint_being_tested = "no_code_provisioning"

    def setUp(self):
        # Create an OAuth client for the test and extract it's the token ID
        # Store the OAuth client ID to remove it at the end.
        oauth_client = self._api.oauth_clients.create(
            self._get_oauth_client_create_payload())["data"]
        self._oauth_client_id = oauth_client["id"]
        self._oauth_token_id = \
            oauth_client["relationships"]["oauth-tokens"]["data"][0]["id"]

    def tearDown(self):
        # Delete all the modules before deleting the OAuth client, otherwise
        ## you might not be able to delete it after the oauth client is purged.
        # TODO
        # self._purge_module_registry()
        self._api.oauth_clients.destroy(self._oauth_client_id)

    def test_no_code_provisioning(self):
        """
        Test the No Code Provisioning API endpoints.
        """

        # Publish a module from the VCS provider, using the OAuth token generated
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
                "type": "registry-modules"
            }
        }
        published_mod = \
            self._api.registry_modules.publish_from_vcs(publish_payload)["data"]
        published_mod_name = published_mod["attributes"]["name"]

        # Wait for the VCS and TFE to sync up and have "setup_complete" status on the module.
        self._setup_published_module_version_timeout(
            published_mod_name, TFE_MODULE_PROVIDER_TYPE)

        shown_reg_mod = \
            self._api.registry_modules.show(
                published_mod_name, TFE_MODULE_PROVIDER_TYPE)["data"]
        shown_reg_mod_id = shown_reg_mod["id"]
        latest_published_version = shown_reg_mod["attributes"]["version-statuses"][0]["version"]

        enable_payload = {
            "data": {
                "type": "no-code-modules",
                "attributes": {
                    "version-pin":  latest_published_version,
                    "enabled": True
                },
                "relationships": {
                    "registry-module": {
                        "data": {
                            "id": shown_reg_mod_id,
                            "type": "registry-module"
                        }
                    }
                }
            }
        }

        # Enable no code provisioning for the module and check it is marked as enabled
        enabled_mod = self._api.no_code_provisioning.enable(enable_payload)["data"]
        enabled_mod_id = enabled_mod["id"]
        self.assertTrue(enabled_mod["attributes"]["enabled"])

        # Update the no code module, and confirm the updates took, reuse the enable_payload
        updated_mod = self._api.no_code_provisioning.update(enabled_mod_id, enable_payload)["data"]
        updated_mod_id = updated_mod["id"]
        self.assertEqual(updated_mod_id, enabled_mod_id)

        # Show the no code module, and confirm it matches the module we updated
        shown_mod = self._api.no_code_provisioning.show(enabled_mod_id)["data"]
        shown_mod_id = shown_mod["id"]
        self.assertEqual(shown_mod_id, updated_mod_id)

        # Deploying the No Code Module, confirm the workspace is created
        # TODO: change the email address then compare them after updating
        deploy_payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name":  self._unittest_random_name(),
                    "description": "A workspace to demonstrate the No-Code provisioning workflow.",
                    "auto_apply": True
                },
                "relationships": {
                    "vars": {
                        "data": [
                            {
                                "type": "vars",
                                "attributes": {
                                    "key": "email",
                                    "value": "foo@bar.com",
                                    "category": "terraform",
                                    "hcl": False,
                                    "sensitive": False,
                                }
                            },
                            {
                                "type": "vars",
                                "attributes": {
                                    "key": "org_name",
                                    "value": self._test_org_name,
                                    "category": "terraform",
                                    "hcl": False,
                                    "sensitive": False,
                                }
                            },
                            {
                                "type": "vars",
                                "attributes": {
                                    "key": "TFE_TOKEN",
                                    "value": self._test_api_token,
                                    "category": "env",
                                    "hcl": False,
                                    "sensitive": True,
                                }
                            }
                        ]
                    }
                }
            }
        }
        deployed_mod_ws = self._api.no_code_provisioning.deploy(enabled_mod_id, deploy_payload)["data"]
        deployed_mod_ws_id = deployed_mod_ws["id"]
        self.assertIsNotNone(deployed_mod_ws_id)

        """
        # TODO: test update_settings_upgrade, read_upgrade_stats and confirm_apply_upgrade

        print("wait for the workspace to be created, sleep")
        time.sleep(60)
        print("done waiting for the workspace to be created")

        update_settings_payload = {
            "data": {
                "type": "workspaces",
                "relationships": {
                    "vars": {
                        "data": [
                            {
                                "type": "vars",
                                "attributes": {
                                    "key": "email",
                                    "value": "foo@baz.com",
                                    "category": "terraform",
                                    "hcl": False,
                                    "sensitive": False,
                                }
                            }
                        ]
                    }
                }
            }
        }
        print("update payload", update_settings_payload)
        updated_mod_ws = self._api.no_code_provisioning.update_settings_upgrade(enabled_mod_id, deployed_mod_ws_id, update_settings_payload)["data"]
        print("updated", updated_mod_ws)
        """

        self._api.workspaces.destroy(workspace_id=deployed_mod_ws_id)
