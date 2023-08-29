"""
Constants for default values in the TFC API implementation testing.
"""

import os
import sys
import logging

# To Protect Against Malfeasance in the Test Suite
# NOTE: these may need to change if duplicate orgs are ever supported by some higher
# level RBAC mechanism in TFC/E.
UNTOUCHABLE_ORGS = ["eklhad", "terrasnek-unittest"]

# Test Defaults
TERRASNEK_LOG_LEVEL = logging.DEBUG

# Configurable Constants
TFC_URL = os.getenv("TFC_URL", None)
TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_ORG_TOKEN = os.getenv("TFC_ORG_TOKEN", None)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)

SSL_VERIFY = os.getenv("SSL_VERIFY", "").lower() != "false"

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", None)
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", None)

SMTP_HOST = os.getenv("SMTP_HOST", None)
SMTP_PORT = os.getenv("SMTP_PORT", None)
SMTP_USERNAME = os.getenv("SMTP_USERNAME", None)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", None)

GH_TOKEN = os.getenv("GH_TOKEN", None)

# NOTE: This is an optional env var, if not provided a random test org will be generated
TEST_ORG_NAME = os.getenv("TEST_ORG_NAME", None)

TEST_EMAIL = os.getenv("TEST_EMAIL", None)
TEST_USERNAME = os.getenv("TEST_USERNAME", None)
TEST_TEAM_NAME = os.getenv("TEST_TEAM_NAME", None)
TEST_PASSWORD = os.getenv("TEST_PASSWORD", None)

if TFC_URL is None:
    sys.exit("Environment variable TFC_URL must be set.")

if TFC_TOKEN is None:
    sys.exit("Environment variable TFC_TOKEN must be set.")

if AWS_ACCESS_KEY_ID is None:
    sys.exit("Environment variable AWS_ACCESS_KEY_ID must be set.")

if AWS_SECRET_ACCESS_KEY is None:
    sys.exit("Environment variable AWS_SECRET_ACCESS_KEY must be set.")

if TWILIO_ACCOUNT_SID is None:
    sys.exit("Environment variable TWILIO_ACCOUNT_SID must be set.")

if TWILIO_AUTH_TOKEN is None:
    sys.exit("Environment variable TWILIO_AUTH_TOKEN must be set.")

if SMTP_HOST is None:
    sys.exit("Environment variable SMTP_HOST must be set.")

if SMTP_PORT is None:
    sys.exit("Environment variable SMTP_PORT must be set.")

if SMTP_USERNAME is None:
    sys.exit("Environment variable SMTP_USERNAME must be set.")

if SMTP_PASSWORD is None:
    sys.exit("Environment variable SMTP_PASSWORD must be set.")

if GH_TOKEN is None:
    sys.exit("Environment variable GH_TOKEN must be set.")

if TEST_EMAIL is None:
    sys.exit("Environment variable TEST_EMAIL must be set.")

if TEST_USERNAME is None:
    sys.exit("Environment variable TEST_USERNAME must be set.")

if TEST_TEAM_NAME is None:
    sys.exit("Environment variable TEST_TEAM_NAME must be set.")

if TEST_PASSWORD is None:
    sys.exit("Environment variable TEST_PASSWORD must be set.")


# Non-Configurable Constants
TFE_MODULE_PROVIDER_TYPE = "tfe"
DEFAULT_VCS_WORKING_DIR = "tfe"
MAX_TEST_TIMEOUT = 300
PAGE_START = 0
PAGE_SIZE = 50
