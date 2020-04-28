"""
Module containing all of the exception classes used for this API client.
"""

# https://docs.python.org/3/tutorial/errors.html

class TFCError(Exception):
    """Base class for Terraform Cloud errors."""


class TFCUnauthorizedError(Exception):
    """Terraform Cloud authentication error. (401)
    """


class TFCResourceNotFoundOrUnauthorized(Exception):
    """Terraform Cloud resource not found error. (404)

    Resource not found or user unauthorized.
    """


class TFCMalformedRequestError(Exception):
    """Terraform Cloud malformed request error. (422)

    Malformed request body (missing attributes, wrong types, etc.)
    """
