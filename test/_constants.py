"""
Constants for default values in the TFC API implementation testing.
"""

import os
import sys

TFC_HOSTNAME = os.getenv("TFC_HOSTNAME", None)
TFC_TOKEN = os.getenv("TFC_TOKEN", None)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)

SSL_VERIFY = os.getenv("SSL_VERIFY", "").lower() != "false"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
GITHUB_SECRET = os.getenv("GITHUB_SECRET", None)

TEST_EMAIL = os.getenv("TEST_EMAIL", None)
TEST_ORG_NAME = os.getenv("TEST_ORG_NAME", None)
TEST_USERNAME = os.getenv("TEST_USERNAME", None)
TEST_TEAM_NAME = os.getenv("TEST_TEAM_NAME", None)
TEST_PASSWORD = os.getenv("TEST_PASSWORD", None)

if TFC_HOSTNAME is None:
    sys.exit("Environment variable TFC_HOSTNAME must be set.")

if TFC_TOKEN is None:
    sys.exit("Environment variable TFC_TOKEN must be set.")

if AWS_ACCESS_KEY_ID is None:
    sys.exit("Environment variable AWS_ACCESS_KEY_ID must be set.")

if AWS_SECRET_ACCESS_KEY is None:
    sys.exit("Environment variable AWS_SECRET_ACCESS_KEY must be set.")

if GITHUB_TOKEN is None:
    sys.exit("Environment variable GITHUB_TOKEN must be set.")

if GITHUB_SECRET is None:
    sys.exit("Environment variable GITHUB_SECRET must be set.")

if TEST_EMAIL is None:
    sys.exit("Environment variable TEST_EMAIL must be set.")

if TEST_ORG_NAME is None:
    sys.exit("Environment variable TEST_ORG_NAME must be set.")

if TEST_USERNAME is None:
    sys.exit("Environment variable TEST_USERNAME must be set.")

if TEST_TEAM_NAME is None:
    sys.exit("Environment variable TEST_TEAM_NAME must be set.")

if TEST_PASSWORD is None:
    sys.exit("Environment variable TEST_PASSWORD must be set.")
