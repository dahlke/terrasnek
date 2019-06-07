import os

TFE_SAAS_URL = "https://app.terraform.io"
TOKEN = os.getenv("TFE_TOKEN", None)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/vnd.api+json"
}

TEST_EMAIL = "neil@hashicorp.com"
TEST_ORG_NAME = "terrasnek_unittest_org"
TEST_ORG_NAME_PAID = "terrasnek_unittest_org_paid"
TEST_USERNAME = "terrasnek_unittest"
TEST_TEAM_NAME = "terrasnek_unittest_team"