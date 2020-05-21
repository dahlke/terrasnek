"""
Module containing all of the exception classes used for this API client.
"""

# https://docs.python.org/3/tutorial/errors.html


class TFCError(Exception):
    """Base class for Terraform Cloud errors."""

class InvalidTFCTokenException(TFCError):
    """Cannot instantiate TFC API class without a valid TFC_TOKEN."""

class TFCUnauthorizedError(TFCError):
    """Terraform Cloud authentication error. (401)"""

class TFCResourceNotFoundOrUnauthorized(TFCError):
    """Terraform Cloud resource not found error. (404)

    Resource not found or user unauthorized.
    """

class TFCMalformedRequestError(TFCError):
    """Terraform Cloud malformed request error. (422)

    Malformed request body (missing attributes, wrong types, etc.)
    """

class TFCDeprecatedWontFix(TFCError):
    """Terraform Cloud deprecated endpoint. Won't be fixed, use another endpoint."""
