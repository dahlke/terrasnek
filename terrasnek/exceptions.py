"""
Module containing all of the exception classes used for this API client.
"""

# https://docs.python.org/3/tutorial/errors.html


class TFCError(Exception):
    """Base class for Terraform Cloud errors."""

class TFCUnauthorizedError(Exception):
    """Terraform Cloud authentication error. (401)"""

class TFCResourceNotFoundOrUnauthorized(Exception):
    """Terraform Cloud resource not found error. (404)

    Resource not found or user unauthorized.
    """

class TFCMalformedRequestError(Exception):
    """Terraform Cloud malformed request error. (422)

    Malformed request body (missing attributes, wrong types, etc.)
    """

class TFCDeprecatedWontFix(Exception):
    """Terraform Cloud deprecated endpoint. Won't be fixed, use another endpoint."""

class TFCRequiresEntitlementStateStorage(Exception):
    """Missing Terraform Cloud Entitlement: State Storage.

    https://www.terraform.io/docs/cloud/api/index.html#feature-entitlements
    """

class TFCRequiresEntitlementOperations(Exception):
    """Missing Terraform Cloud Entitlement: Operations.

    https://www.terraform.io/docs/cloud/api/index.html#feature-entitlements
    """

class TFCRequiresEntitlementVCSIntegrations(Exception):
    """Missing Terraform Cloud Entitlement: VCS Integrations.

    https://www.terraform.io/docs/cloud/api/index.html#feature-entitlements
    """

class TFCRequiresEntitlementSentinel(Exception):
    """Missing Terraform Cloud Entitlement: Sentinel.

    https://www.terraform.io/docs/cloud/api/index.html#feature-entitlements
    """

class TFCRequiresEntitlementPrivateModuleRegistry(Exception):
    """Missing Terraform Cloud Entitlement: Private Module Registry.

    https://www.terraform.io/docs/cloud/api/index.html#feature-entitlements
    """

class TFCRequiresEntitlementTeams(Exception):
    """Missing Terraform Cloud Entitlement: Teams.

    https://www.terraform.io/docs/cloud/api/index.html#feature-entitlements
    """
