import logging
import hashlib
import base64
import unittest
import os
import binascii

from ._constants import \
    TFE_HOSTNAME, TFE_TOKEN, HEADERS, TEST_EMAIL, TEST_ORG_NAME, \
    TEST_ORG_NAME_PAID, TEST_USERNAME, TEST_TEAM_NAME, \
    GITHUB_TOKEN, GITHUB_SECRET

from terrasnek.api import TFE


class TestTFEBaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        # TODO: some validation on the inputs / env vars
        self._api = TFE(TFE_TOKEN)
        self._test_username = TEST_USERNAME
        self._test_email = TEST_EMAIL
        self._test_team_name = TEST_TEAM_NAME

        # TODO: rename this to be more explicitly for ephemeral testing, and the other stable and not to be deleted
        self._test_org_name = TEST_ORG_NAME
        self._test_org_name_paid = TEST_ORG_NAME_PAID

        # TODO: make these env vars?
        self._test_state_path = "./test/testdata/terraform/terrasnek_unittest.tfstate"
        self._config_version_upload_tarball_path = "./test/testdata/terraform/terrasnek_unittest_config_version.tar.gz"
        self._plan_export_tarball_target_path = "/tmp/terrasnek_unittest.tar.gz"

        self._api.set_organization(self._test_org_name_paid)

    def _name_with_random(self, name):
        random_hex = binascii.b2a_hex(os.urandom(8)).decode("ascii")
        return f"terrasnek-unittest-test-{name}-{random_hex}"

    def _get_org_create_payload(self):
        return {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": self._test_org_name,
                    "email": self._test_email
                }
            }
        }

    def _get_team_create_payload(self):
        return {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": self._test_team_name,
                    "organization-access": {
                        "manage-workspaces": True,
                        "manage-policies": True,
                        "manage-vcs-settings": True
                    }
                }
            }
        }

    def _get_oauth_client_create_payload(self, name):
        name = self._name_with_random(name)

        return {
            "data": {
                "type": "oauth-clients",
                "attributes": {
                    "name": name,
                    "service-provider": "github",
                    "http-url": "https://github.com",
                    "api-url": "https://api.github.com",
                    "secret": GITHUB_SECRET,
                    "oauth-token-string": GITHUB_TOKEN
                }
            }
        }

    def _get_config_version_create_payload(self):
        return {
            "data": {
                "type": "configuration-versions",
                "attributes": {
                    "auto-queue-runs": False
                }
            }
        }

    def _get_user_token_create_payload(self):
        return {
            "data": {
                "type": "authentication-tokens",
                "attributes": {
                    "description": "api"
                }
            }
        }

    def _get_ws_with_vcs_create_payload(self, name, oauth_token_id):
        name = self._name_with_random(name)

        return {
            "data": {
                "attributes": {
                    "name": name,
                    "terraform_version": "0.11.1",
                    "working-directory": "test/testdata/terraform/src",
                    "vcs-repo": {
                        "identifier": "dahlke/terrasnek",
                        "oauth-token-id": oauth_token_id,
                        "branch": "test-fix-and-optimize"
                    }
                },
                "type": "workspaces"
            }
        }

    def _get_ws_without_vcs_create_payload(self, name):
        name = self._name_with_random(name)

        return {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name": name
                }
            }
        }

    def _get_run_create_payload(self, workspace_id):
        return {
            "data": {
                "attributes": {
                    "is-destroy": False,
                    "message": "test"
                },
                "type": "runs",
                "relationships": {
                    "workspace": {
                        "data": {
                            "type": "workspaces",
                            "id": workspace_id
                        }
                    }
                }
            }
        }

    def _get_variable_create_payload(self, key, value, workspace_id):
        return {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": key,
                    "value": value,
                    "category": "terraform",
                    "hcl": False,
                    "sensitive": False
                },
                "relationships": {
                    "workspace": {
                        "data": {
                            "id": workspace_id,
                            "type": "workspaces"
                        }
                    }
                }
            }
        }

    def _get_plan_export_create_payload(self, plan_id):
        return {
            "data": {
                "type": "plan-exports",
                "attributes": {
                    "data-type": "sentinel-mock-bundle-v0"
                },
                "relationships": {
                    "plan": {
                        "data": {
                            "id": plan_id,
                            "type": "plans"
                        }
                    }
                }
            }
        }

    def _get_state_version_create_payload(self):
        # Go Example: https://github.com/hashicorp/go-tfe/blob/4ca75c88c51753c622df5bf4446e69eff6c885d6/state_version_test.go#L105
        raw_state_bytes = None

        with open(self._test_state_path, "rb") as f:
            raw_state_bytes = f.read()

        state_hash = hashlib.md5()
        state_hash.update(raw_state_bytes)
        state_md5 = state_hash.hexdigest()

        state_b64 = base64.b64encode(raw_state_bytes).decode("utf-8")

        return {
            "data": {
                "type":"state-versions",
                "attributes": {
                    "serial": 1,
                    "md5": state_md5,
                    "state": state_b64
                }
            }
        }
