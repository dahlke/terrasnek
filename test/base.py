import unittest
from ._constants import \
    TFE_URL, TFE_TOKEN, HEADERS, TEST_EMAIL, TEST_ORG_NAME, \
        TEST_ORG_NAME_PAID, TEST_USERNAME, TEST_TEAM_NAME, \
            GH_TOKEN, GH_SECRET

from tfepy.api import TFE

class TestTFEBaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
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

        """
        # NOTE: It's not possible to create a user with the API yet.

        self._user_create_payload = {
            "data": {
                "type": "teams",
                "attributes": {
                    "name": "team-creation-test",
                    "organization-access": {
                        "manage-workspaces": True,
                        "manage-policies": True,
                        "manage-vcs-settings": True
                    }
                }
            }
        }
        """
