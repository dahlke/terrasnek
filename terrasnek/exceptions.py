"""
Module containing all of the exception classes used for this API client.
"""

class TFCError(Exception):
    """Base class for Terraform Cloud errors."""
    pass

class TFCAuthError(Exception):
    """Terraform Cloud authentication error."""
    pass

