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
import time
import timeout_decorator

from terrasnek.api import TFC
from terrasnek._constants import Entitlements

from ._constants import \
    TFC_TOKEN, TFC_ORG_TOKEN, TFC_URL, TEST_EMAIL, \
    TEST_ORG_NAME, TEST_USERNAME, TEST_TEAM_NAME, \
    GITHUB_TOKEN, GITHUB_SECRET, \
    SSL_VERIFY, TEST_PASSWORD, MAX_TEST_TIMEOUT, \
    DEFAULT_VCS_WORKING_DIR, TFC_SAAS_HOSTNAME, API_LOG_LEVEL

class TestTFCBaseTestCase(unittest.TestCase):
    """
    Base class for providing common test utilities across API endpoints. It
    includes helpers to generate create payloads for common endpoints used in
    many tests.
    """

    _unittest_name = "base"
    _endpoint_being_tested = None

    @classmethod
    def setUpClass(cls):
        cls._logger = logging.getLogger(cls.__class__.__name__)
        cls._logger.setLevel(logging.INFO)
        cls._tfc_url = TFC_URL

        cls._test_api_token = TFC_TOKEN
        cls._test_api_org_token = TFC_ORG_TOKEN
        cls._api_log_level = API_LOG_LEVEL
        cls._ssl_verify = SSL_VERIFY

        cls._api = TFC(\
            cls._test_api_token, url=cls._tfc_url, \
                verify=cls._ssl_verify, log_level=cls._api_log_level)

        cls._test_username = TEST_USERNAME
        cls._test_email = TEST_EMAIL
        cls._test_team_name = TEST_TEAM_NAME
        cls._test_password = TEST_PASSWORD

        cls._test_state_path = "./test/testdata/terraform/terrasnek_unittest.tfstate"
        cls._config_version_upload_tarball_path = \
            "./test/testdata/terraform/terrasnek_unittest_config_version.tar.gz"
        cls._module_upload_tarball_path = \
            "./test/testdata/terraform/terrasnek_unittest_module.tar.gz"
        cls._policy_set_upload_tarball_path = \
            "./test/testdata/sentinel/terrasnek_unittest_sentinel.tar.gz"
        cls._plan_export_tarball_target_path = \
            "/tmp/terrasnek_unittest_plan_export.tar.gz"
        cls._plan_json_tarball_target_path = \
            "/tmp/terrasnek_unittest_plan_json.tar.gz"
        cls._module_version_source_tarball_target_path = \
            "/tmp/terrasnek_unittest_module_version_export.tar.gz"
        cls._module_latest_source_tarball_target_path = \
            "/tmp/terrasnek_unittest_module_latest_export.tar.gz"

        # If a test org is specified, use the specified org, otherwise create
        # a new one to run the testing in.
        if TEST_ORG_NAME:
            cls._test_org_name = TEST_ORG_NAME
        else:
            cls._test_org_name = cls._random_name()
            org_create_payload = {
                "data": {
                    "type": "organizations",
                    "attributes": {
                        "name": cls._test_org_name,
                        "email": cls._test_email
                    }
                }
            }
            cls._test_org = cls._api.orgs.create(org_create_payload)

        cls._api.set_org(cls._test_org_name)

        # Check to see if this test can be run with the current entitlments
        missing_entitlements = cls._get_missing_entitlements(cls._endpoint_being_tested)

        if missing_entitlements:
            raise unittest.SkipTest(\
                "Missing required Terraform Cloud Entitlments for test", \
                    cls._unittest_name, missing_entitlements)

        if TFC_SAAS_HOSTNAME in TFC_URL and "admin" in str(cls._endpoint_being_tested):
            raise unittest.SkipTest(\
                "Skipping Admin Test since we're testing against Terraform Cloud.")

        cls._purge_organization()

    @classmethod
    def tearDownClass(cls):
        # Only destroy the org if we auto generated it
        if not TEST_ORG_NAME:
            cls._api.orgs.destroy(cls._test_org_name)

    @classmethod
    def _purge_organization(cls):
        cls._logger.info(\
            f"Purging test org ({cls._test_org_name}) of all resources to start fresh...")

        cls._logger.info(f"Purging test org ({cls._test_org_name}) of workspaces...")
        workspaces = cls._api.workspaces.list()["data"]
        for workspace in workspaces:
            cls._api.workspaces.destroy(workspace_id=workspace["id"])
        cls._logger.debug(f"Workspaces purged from test org ({cls._test_org_name}).")

        cls._logger.debug(f"Purging test org ({cls._test_org_name}) of modules...")
        registry_modules = cls._api.registry_modules.list()["modules"]
        for registry_module in registry_modules:
            cls._api.registry_modules.destroy(registry_module["name"])
        cls._logger.debug(f"Modules purged from test org ({cls._test_org_name}).")

        cls._logger.debug(f"Purging test org ({cls._test_org_name}) of policies...")
        policies = cls._api.policies.list()["data"]
        for policy in policies:
            cls._api.policies.destroy(policy["id"])
        cls._logger.debug(f"Policies purged from test org ({cls._test_org_name}).")

        cls._logger.debug(f"Purging test org ({cls._test_org_name}) of policy sets...")
        policy_sets = cls._api.policy_sets.list()["data"]
        for policy_set in policy_sets:
            cls._api.policy_sets.destroy(policy_set["id"])
        cls._logger.debug(f"Policy sets purged from test org ({cls._test_org_name}).")

        # Delete all the VCS adjacent resources before the VCS client
        cls._logger.debug(f"Purging test org ({cls._test_org_name}) of OAuth clients...")
        oauth_clients = cls._api.oauth_clients.list()["data"]
        for oauth_client in oauth_clients:
            cls._api.oauth_clients.destroy(oauth_client["id"])
        cls._logger.debug(f"OAuth clients purged from test org ({cls._test_org_name}).")

        cls._logger.debug(f"Purging test org ({cls._test_org_name}) of SSH Keys...")
        ssh_keys = cls._api.ssh_keys.list()["data"]
        for ssh_key in ssh_keys:
            cls._api.ssh_keys.destroy(ssh_key["id"])
        cls._logger.debug(f"SSH keys purged from test org ({cls._test_org_name}).")

        # Deleting the teams will delete all team memberships, and team tokens
        cls._logger.debug(f"Purging test org ({cls._test_org_name}) of teams...")
        teams = cls._api.teams.list()["data"]
        for team in teams:
            team_name = team["attributes"]["name"]
            if team_name != "owners":
                cls._api.teams.destroy(team["id"])
        cls._logger.debug(f"Teams purged from test org ({cls._test_org_name}).")

        cls._logger.info(f"Test org ({cls._test_org_name}) purged of all resources.")

        # TODO: org tokens / org memberships / agents / agent pools

    @classmethod
    def _get_missing_entitlements(cls, endpoint_attr_name):
        endpoint = getattr(cls._api, endpoint_attr_name)
        required_entitlements = endpoint._required_entitlements()
        current_entitlements = cls._api.orgs.entitlements(cls._test_org_name)["data"]["attributes"]

        missing_entitlements = []
        for req_ent in required_entitlements:
            meets_sub_requirement = False

            for cur_ent_key in current_entitlements:
                ent_enabled = current_entitlements[cur_ent_key]
                cur_ent_key = cur_ent_key.replace("-", "_").upper()

                if Entitlements[cur_ent_key] == req_ent and ent_enabled:
                    meets_sub_requirement = True

            if not meets_sub_requirement:
                missing_entitlements.append(req_ent)

        return missing_entitlements

    @classmethod
    def _random_name(cls, ran_str_len=8):
        random_hex = binascii.b2a_hex(os.urandom(ran_str_len)).decode("ascii")
        return f"terrasnek-unittest-{random_hex}"

    @classmethod
    def _unittest_random_name(cls, ran_str_len=8):
        random_hex = binascii.b2a_hex(os.urandom(ran_str_len)).decode("ascii")
        return f"terrasnek-test-{cls._unittest_name}-{random_hex}"

    @staticmethod
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

    def _get_ws_with_vcs_create_payload(self, oauth_token_id, working_dir=DEFAULT_VCS_WORKING_DIR):
        # NB: Needs to be TF > v0.12 for Cost Estimation to work
        return {
            "data": {
                "attributes": {
                    "name": self._unittest_random_name(),
                    "terraform_version": "0.12.24",
                    "working-directory": working_dir,
                    "vcs-repo": {
                        "identifier": "dahlke/terrasnek-unittest-config",
                        "oauth-token-id": oauth_token_id,
                        "branch": "master"
                    }
                },
                "type": "workspaces"
            }
        }

    def _get_ws_without_vcs_create_payload(self):
        return {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name": self._unittest_random_name()
                }
            }
        }

    def _get_ssh_key_create_payload(self):
        return {
            "data": {
                "type": "ssh-keys",
                "attributes": {
                    "name": self._unittest_random_name(),
                    "value": "-----BEGIN RSA PRIVATE KEY-----\nfoo..."
                }
            }
        }

    def _get_policy_create_payload(self):
        # https://www.terraform.io/docs/cloud/api/policies.html#sample-payload
        return {
            "data": {
                "attributes": {
                    "enforce": [
                        {
                            "path": "terransek-example-policy.sentinel",
                            "mode": "soft-mandatory"
                        }
                    ],
                    "name": self._unittest_random_name(),
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

    def _get_policy_set_create_payload(self, oauth_token_id):
        # https://www.terraform.io/docs/cloud/api/policies.html#sample-payload
        return {
            "data": {
                "type": "policy-sets",
                "attributes": {
                    "name": self._unittest_random_name(),
                    "description": "terrasnek unittest",
                    "global": False,
                    "policies-path": "sentinel/",
                    "vcs-repo": {
                        "branch": "master",
                        "identifier": "dahlke/terrasnek-unittest-config",
                        "ingress-submodules": False,
                        "oauth-token-id": oauth_token_id
                    }
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
        # https://www.terraform.io/docs/cloud/api/organizations.html#sample-payload
        return {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": self._unittest_random_name(),
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
        return {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": self._unittest_random_name(),
                    "organization-access": {
                        "manage-workspaces": True,
                        "manage-policies": True,
                        "manage-vcs-settings": True
                    }
                }
            }
        }

    def _get_oauth_client_create_payload(self):
        return {
            "data": {
                "type": "oauth-clients",
                "attributes": {
                    "name": self._unittest_random_name(),
                    "service-provider": "github",
                    "http-url": "https://github.com",
                    "api-url": "https://api.github.com",
                    "secret": GITHUB_SECRET,
                    "oauth-token-string": GITHUB_TOKEN
                }
            }
        }

    @timeout_decorator.timeout(MAX_TEST_TIMEOUT)
    def _created_run_timeout(self, run_id):
        """
        While running the tests, it's possible that a run gets queued, which
        would cause the test suite to stall indefinitely until the queue is cleared.
        This function is meant to keep that to a minimum, and just fail the test
        if we are waiting too long.
        """
        created_run = self._api.runs.show(run_id)["data"]
        while not created_run["attributes"]["actions"]["is-confirmable"]:
            self._logger.debug("Waiting on plan to execute...")
            created_run = self._api.runs.show(run_id)["data"]
            self._logger.debug("Waiting for created run to finish planning...")
            time.sleep(1)
        self._logger.debug("Plan successful.")
        return created_run
