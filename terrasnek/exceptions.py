"""
Module containing all of the exception classes used for this API client.
"""

# https://docs.python.org/3/tutorial/errors.html

# Common Exceptions
class TFCException(Exception):
    """Base class for Terraform Cloud errors."""

# Terraform Cloud Specific Exceptions
class InvalidTFCTokenException(TFCException):
    """Cannot instantiate TFC API class without a valid TFC_TOKEN."""

class TFCDeprecatedWontFix(TFCException):
    """Terraform Cloud deprecated endpoint. Won't be fixed, use another endpoint."""

# HTTP Exceptions
class TFCHTTPBadRequest(TFCException):
    """Terraform Cloud bad request. (HTTP 400)

    The HTTP 400 Bad Request response status code indicates that the server
    cannot or will not process the request due to something that is perceived
    to be a client error (e.g., malformed request syntax, invalid request
    message framing, or deceptive request routing).
    """

class TFCHTTPUnauthorized(TFCException):
    """Terraform Cloud unauthorized. (HTTP 401)

    The HTTP 401 Unauthorized client error status response code indicates that
    the request has not been applied because it lacks valid authentication
    credentials for the target resource.
    """

class TFCHTTPForbidden(TFCException):
    """Terraform Cloud forbidden. (HTTP 403)

    The HTTP 403 Forbidden client error status response code indicates that
    the server understood the request but refuses to authorize it.
    """

class TFCHTTPNotFound(TFCException):
    """Terraform Cloud not found. (HTTP 404)

    The HTTP 404 Not Found client error response code indicates that the server
    can't find the requested resource. Links that lead to a 404 page are often
    called broken or dead links and can be subject to link rot.
    """

class TFCHTTPConflict(TFCException):
    """Terraform Cloud conflict. (HTTP 409)

    The HTTP 409 Conflict response status code indicates a request conflict with
    current state of the target resource.
    """

class TFCHTTPPreconditionFailed(TFCException):
    """Terraform Cloud precondition failed. (HTTP 412)

    The HTTP 412 Precondition Failed client error response code indicates that
    access to the target resource has been denied. This happens with
    conditional requests on methods other than GET or HEAD when the condition
    defined by the If-Unmodified-Since or If-None-Match headers is not fulfilled.
    In that case, the request, usually an upload or a modification of a resource,
    cannot be made and this error response is sent back.
    """

class TFCHTTPUnprocessableEntity(TFCException):
    """Terraform Cloud unprocessable entity. (HTTP 422)

    The HTTP 422 Unprocessable Entity response status code indicates that the
    server understands the content type of the request entity, and the syntax
    of the request entity is correct, but it was unable to process the contained
    instructions.
    """

class TFCHTTPInternalServerError(TFCException):
    """Terraform Cloud internal server error. (HTTP 500)

    The HTTP 500 Internal Server Error server error response code indicates that
    the server encountered an unexpected condition that prevented it from
    fulfilling the request.
    """

class TFCHTTPUnclassified(TFCException):
    """Terraform Cloud unclassified error.

    This is a catch-all class to manage any HTTP exceptions that are not
    enumerated.
    """
