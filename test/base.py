"""
Base module for all of the Terraform Cloud API modules.

Contains many of the defaults and payload generators.
"""

import logging
import hashlib
import base64
import unittest
import os
import binascii

from terrasnek.api import TFC

from ._constants import \
    TFC_TOKEN, TFC_HOSTNAME, TEST_EMAIL, \
    TEST_ORG_NAME, TEST_USERNAME, TEST_TEAM_NAME, \
    GITHUB_TOKEN, GITHUB_SECRET, \
    SSL_VERIFY


class TestTFCBaseTestCase(unittest.TestCase):
    """
    Base class for providing common test utilities across API endpoints. It
    includes helpers to generate create payloads for common endpoints used in
    many tests.
    """

    @classmethod
    def setUpClass(cls):
        cls._logger = logging.getLogger(cls.__class__.__name__)
        cls._logger.setLevel(logging.INFO)
        cls._api = TFC(\
            TFC_TOKEN, url=TFC_HOSTNAME, verify=SSL_VERIFY)
        cls._test_username = TEST_USERNAME
        cls._test_email = TEST_EMAIL
        cls._test_team_name = TEST_TEAM_NAME
        cls._test_org_name = TEST_ORG_NAME
        cls._test_api_token = TEST_ORG_NAME

        cls._test_state_path = "./test/testdata/terraform/terrasnek_unittest.tfstate"
        cls._config_version_upload_tarball_path = \
            "./test/testdata/terraform/terrasnek_unittest_config_version.tar.gz"
        cls._plan_export_tarball_target_path = "/tmp/terrasnek_unittest.tar.gz"

        cls._api.set_org(cls._test_org_name)

    @staticmethod
    def _name_with_random(name):
        random_hex = binascii.b2a_hex(os.urandom(8)).decode("ascii")
        return f"terrasnek-test-{name}-{random_hex}"

    @ staticmethod
    def _get_config_version_create_payload():
        return {
            "data": {
                "type": "configuration-versions",
                "attributes": {
                    "auto-queue-runs": False
                }
            }
        }


    @staticmethod
    def _get_user_token_create_payload():
        return {
            "data": {
                "type": "authentication-tokens",
                "attributes": {
                    "description": "api"
                }
            }
        }

    @staticmethod
    def _get_run_create_payload(workspace_id):
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

    @staticmethod
    def _get_variable_create_payload(\
        key, value, workspace_id, category="terraform", sensitive=False):
        return {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": key,
                    "value": value,
                    "category": category,
                    "hcl": False,
                    "sensitive": sensitive
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

    def _get_state_version_create_payload(self):
        # Go Example:
        # https://github.com/hashicorp/go-tfe/blob/4ca75c88c51753c622df5bf4446e69eff6c885d6/state_version_test.go#L105
        raw_state_bytes = None

        with open(self._test_state_path, "rb") as infile:
            raw_state_bytes = infile.read()

        state_hash = hashlib.md5()
        state_hash.update(raw_state_bytes)
        state_md5 = state_hash.hexdigest()

        state_b64 = base64.b64encode(raw_state_bytes).decode("utf-8")

        return {
            "data": {
                "type": "state-versions",
                "attributes": {
                    "serial": 1,
                    "md5": state_md5,
                    "state": state_b64
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
                    "working-directory": "test/testdata/terraform/src/tfe",
                    "vcs-repo": {
                        "identifier": "dahlke/terrasnek",
                        "oauth-token-id": oauth_token_id,
                        "branch": "master"
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

    def _get_ssh_key_create_payload(self):
        name = self._name_with_random("ssh-key")

        return {
            "data": {
                "type": "ssh-keys",
                "attributes": {
                    "name": name,
                    "value": "-----BEGIN RSA PRIVATE KEY-----\nfoo..."
                }
            }
        }

    def _get_policy_create_payload(self):
        name = self._name_with_random("policy")

        # https://www.terraform.io/docs/cloud/api/policies.html#sample-payload
        return {
            "data": {
                "attributes": {
                    "enforce": [
                        {
                            "path": "terransek-example-policy.sentinel",
                            "mode": "hard-mandatory"
                        }
                    ],
                    "name": name,
                    "description": "terrasnek example policy"
                },
                "relationships": {
                    "policy-sets": {
                        "data": []
                    }
                },
                "type": "policies"
            }
        }

    def _get_policy_set_create_payload(self):
        name = self._name_with_random("pol-set")

        # https://www.terraform.io/docs/cloud/api/policies.html#sample-payload
        return {
            "data": {
                "type": "policy-sets",
                "attributes": {
                    "name": name,
                    "description": "terrasnek unittest",
                    "global": False
                },
                "relationships": {
                    "policies": {
                        "data": []
                    },
                    "workspaces": {
                        "data": []
                    }
                }
            }
        }

    def _get_org_create_payload(self):
        name = self._name_with_random("org")
        return {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": name,
                    "email": self._test_email
                }
            }
        }

    def _get_org_membership_invite_payload(self):
        return {
            "data": {
                "attributes": {
                    "email": self._test_email,
                },
                "relationships": {
                    "teams": {
                        "data": []
                    },
                },
                "type": "organization-memberships"
            }
        }

    def _get_team_create_payload(self):
        name = self._name_with_random("team")
        return {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": name,
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
