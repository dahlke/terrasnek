import os
import sys

TFE_URL = os.getenv("TFE_URL", None)
TFE_TOKEN = os.getenv("TFE_TOKEN", None)

GH_TOKEN = os.getenv("GH_TOKEN", None)
GH_SECRET = os.getenv("GH_SECRET", None)

TEST_EMAIL = os.getenv("TEST_EMAIL", None)
TEST_ORG_NAME = os.getenv("TEST_ORG_NAME", None)
TEST_ORG_NAME_PAID = os.getenv("TEST_ORG_NAME_PAID", None)
TEST_USERNAME = os.getenv("TEST_USERNAME", None)
TEST_TEAM_NAME = os.getenv("TEST_TEAM_NAME", None)

# TODO: Handle this all much more cleanly
if TFE_URL is None:
    sys.exit("Environment variable TFE_URL must be set.")

if TFE_TOKEN is None:
    sys.exit("Environment variable TFE_TOKEN must be set.")

if GH_TOKEN is None:
    sys.exit("Environment variable GH_TOKEN must be set.")

if GH_SECRET is None:
    sys.exit("Environment variable GH_SECRET must be set.")

if TEST_EMAIL is None:
    sys.exit("Environment variable TEST_EMAIL must be set.")

if TEST_ORG_NAME is None:
    sys.exit("Environment variable TEST_ORG_NAME must be set.")

if TEST_ORG_NAME_PAID is None:
    sys.exit("Environment variable TEST_ORG_NAME_PAID must be set.")

if TEST_USERNAME is None:
    sys.exit("Environment variable TEST_USERNAME must be set.")

if TEST_TEAM_NAME is None:
    sys.exit("Environment variable TEST_TEAM_NAME must be set.")

HEADERS = {
    "Authorization": f"Bearer {TFE_TOKEN}",
    "Content-Type": "application/vnd.api+json"
}
