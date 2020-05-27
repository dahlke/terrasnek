"""
Module for Terraform Cloud API Endpoint: Admin Users.
"""

from .endpoint import TFCEndpoint

class TFCAdminUsers(TFCEndpoint):
    """
    The Users Admin API contains endpoints to help site administrators manage user accounts.

    https://www.terraform.io/docs/cloud/api/admin/users.html
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/users"

    def required_entitlements(self):
        return []

    def destroy(self, user_id):
        """
        ``DELETE /admin/users/:id``

        This endpoint deletes a user's account from Terraform Cloud. To prevent unowned
        organizations, a user cannot be deleted if they are the sole owner of any organizations.
        The organizations must be given a new owner or deleted first.
        """
        url = f"{self._endpoint_base_url}/{user_id}"
        return self._destroy(url)

    def disable_two_factor(self, user_id):
        """
        ``POST /admin/users/:id/actions/disable_two_factor``

        This endpoint disables a user's two-factor authentication in the situation where they
        have lost access to their device and recovery codes. Before disabling a user's two-factor
        authentication, completing a security verification process is recommended to ensure
        the request is legitimate.
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/disable_two_factor"
        return self._post(url)

    def grant_admin(self, user_id):
        """
        ``POST /admin/users/:id/actions/grant_admin``

        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/grant_admin"
        return self._post(url)

    def impersonate(self, user_id):
        """
        ``POST /admin/users/:id/actions/impersonate``

        Impersonation allows an admin to begin a new session as another user in the system; for
        more information, see Impersonating a User in the Private Terraform Cloud
        administration section. This endpoint does not respond with a body, but the response
        does include a ``Set-Cookie`` header to persist a new session.
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/impersonate"
        return self._post(url)

    def list(self, query=None, filters=None, page=None, page_size=None):
        """
        ``GET /admin/users``

        This endpoint lists all user accounts in the Terraform Cloud installation.
        """
        return self._list(\
            self._endpoint_base_url, query=query, filters=filters, page=page, page_size=page_size)

    def revoke_admin(self, user_id):
        """
        ``POST /admin/users/:id/actions/revoke_admin``
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/revoke_admin"
        return self._post(url)

    def suspend(self, user_id):
        """
        ``POST /admin/users/:id/actions/suspend``

        This endpoint suspends a user's account, preventing them from authenticating
        and accessing resources.
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/suspend"
        return self._post(url)

    def unimpersonate(self):
        """
        ``POST /admin/users/actions/unimpersonate``


        When an admin has used the above endpoint to begin an impersonation session, they
        can make a request to this endpoint, using the cookie provided originally, in order
        to end that session and log out as the impersonated user.

        This endpoint does not respond with a body, but the response does include a
        Set-Cookie header to persist a new session as the original admin user. As such,
        this endpoint will have no effect unless the client is able to persist and use cookies.
        """
        url = f"{self._endpoint_base_url}/actions/unimpersonate"
        return self._post(url)

    def unsuspend(self, user_id):
        """
        ``POST /admin/users/:id/actions/unsuspend``

        This endpoint re-activates a suspended user's account, allowing them to
        resume authenticating and accessing resources.
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/unsuspend"
        return self._post(url)
