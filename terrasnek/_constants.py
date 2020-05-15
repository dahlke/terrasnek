"""
Constants for default values on the TFC API endpoints
"""

from enum import Enum

# TODO move these to a shared util class, should the HTTP codfes be enums too?
# Should enums have their own file?

# Default Config Items
TFC_SAAS_URL = "https://app.terraform.io"

# Common TFC API HTTP Codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_ACCEPTED = 202
HTTP_NO_CONTENT = 204

class Entitlements(Enum):
    """
    Enumeration of all the possible Terraform Cloud Entitlements, to be used
    on each endpoint to indicate the required entitlements to use that piece
    of the Terraform Cloud API.
    """

    COST_ESTIMATION = "COST_ESTIMATION"
    CONFIGURATION_DESIGNER = "CONFIGURATION_DESIGNER"
    OPERATIONS = "OPERATIONS"
    PRIVATE_MODULE_REGISTRY = "PRIVATE_MODULE_REGISTRY"
    SENTINEL = "SENTINEL"
    STATE_STORAGE = "STATE_STORAGE"
    TEAMS = "TEAMS"
    VCS_INTEGRATIONS = "VCS_INTEGRATIONS"
    USER_LIMIT = "USER_LIMIT"
    SELF_SERVE_BILLING = "SELF_SERVE_BILLING"