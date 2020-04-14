"""
Module containing all of the exception classes used for this API client.
"""


# https://docs.python.org/3/tutorial/errors.html

class TFCError(Exception):
    """Base class for Terraform Cloud errors."""
    pass


class TFCUnauthorizedError(Exception):
    """Terraform Cloud authentication error. (401)
    """
    pass


class TFCResourceNotFoundOrUnauthorized(Exception):
    """Terraform Cloud resource not found error. (404)

    Resource not found or user unauthorized.
    """
    pass


class TFCMalformedRequestError(Exception):
    """Terraform Cloud malformed request error. (422)

    Malformed request body (missing attributes, wrong types, etc.)
    """
    pass
