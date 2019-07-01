import unittest
import logging
import hashlib
import base64

from ._constants import \
    TFE_URL, TFE_TOKEN, HEADERS, TEST_EMAIL, TEST_ORG_NAME, \
    TEST_ORG_NAME_PAID, TEST_USERNAME, TEST_TEAM_NAME, \
    GH_TOKEN, GH_SECRET

from tfepy.api import TFE


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

        self._api.set_organization(self._test_org_name_paid)

        self._org_create_payload = {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": self._test_org_name,
                    "email": self._test_email
                }
            }
        }

        self._team_create_payload = {
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

        self._ws_create_without_vcs_payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name": "unittest"
                }
            }
        }

        self._oauth_client_create_payload = {
            "data": {
                "type": "oauth-clients",
                "attributes": {
                    "name": "python_unittest_test",
                    "service-provider": "github",
                    "http-url": "https://github.com",
                    "api-url": "https://api.github.com",
                    "secret": GH_SECRET,
                    "oauth-token-string": GH_TOKEN
                }
            }
        }

        self._config_version_create_payload = {
            "data": {
                "type": "configuration-versions",
                "attributes": {
                    "auto-queue-runs": False
                }
            }
        }

        # TODO: make these env vars?
        self._test_state_path = "./test/testdata/terrasnek_unittest.tfstate"
        self._config_version_upload_tarball_path = "./test/testdata/terrasnek_unittest_config_version.tar.gz"
        self._plan_export_tarball_target_path = "/tmp/terrasnek_unittest.tar.gz"
        

    @classmethod
    def _get_create_ws_with_vcs_payload(self, oauth_token_id):
        # TODO
        return {
            "data": {
                "attributes": {
                    "name": "terrasnek_unittest",
                    "terraform_version": "0.11.1",
                    "working-directory": "",
                    "vcs-repo": {
                        "identifier": "dahlke/tfe-demo",
                        "oauth-token-id": oauth_token_id,
                        "branch": "",
                        "working-directory": "terrasnek-unittest",
                        "default-branch": True
                    }
                },
                "type": "workspaces"
            }
        }

    def _get_create_variable_payload(self, k, v, workspace_id):
        return {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": k,
                    "value": v,
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

    def _get_create_run_payload(self, workspace_id):
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

    def _get_create_plan_export_payload(self, plan_id):
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

    def _get_create_state_version_payload(self):
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