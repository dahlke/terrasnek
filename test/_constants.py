import os

TFE_URL = os.getenv("TFE_URL", None)
TFE_TOKEN = os.getenv("TFE_TOKEN", None)

GH_TOKEN = os.getenv("GH_TOKEN", None)
GH_SECRET = os.getenv("GH_SECRET", None)

TEST_EMAIL = os.getenv("TEST_EMAIL", None)
TEST_ORG_NAME = os.getenv("TEST_ORG_NAME", None)
TEST_ORG_NAME_PAID = os.getenv("TEST_ORG_NAME_PAID", None)
TEST_USERNAME = os.getenv("TEST_USERNAME", None)
TEST_TEAM_NAME = os.getenv("TEST_TEAM_NAME", None)

HEADERS = {
    "Authorization": f"Bearer {TFE_TOKEN}",
    "Content-Type": "application/vnd.api+json"
}
