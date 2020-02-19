"""
Module for Terraform Cloud API Endpoint: Admin Users.
"""

import json
import requests

from .endpoint import TFCEndpoint


class TFCAdminUsers(TFCEndpoint):
    """
    The Users Admin API contains endpoints to help site administrators manage user accounts.

    https://www.terraform.io/docs/cloud/api/admin/users.html
    """

    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, organization_name, headers)
        self._base_url = f"{base_url}/admin/users"

    def destroy(self, user_id):
        """
        DELETE /admin/users/:id

        This endpoint deletes a user's account from Terraform Cloud. To prevent unowned
        organizations, a user cannot be deleted if they are the sole owner of any organizations.
        The organizations must be given a new owner or deleted first.
        """
        url = f"{self._base_url}/{user_id}"
        return self._destroy(url)

    def disable_two_factor(self, user_id):
        """
        POST /admin/users/:id/actions/disable_two_factor

        This endpoint disables a user's two-factor authentication in the situation where they
        have lost access to their device and recovery codes. Before disabling a user's two-factor
        authentication, completing a security verification process is recommended to ensure
    the request is legitimate.
        """
        results = None
        url = f"{self._base_url}/{user_id}/actions/disable_two_factor"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def grant_admin(self, user_id):
        """
        POST /admin/users/:id/actions/grant_admin

        """
        results = None
        url = f"{self._base_url}/{user_id}/actions/grant_admin"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def impersonate(self, user_id):
        """
        POST /admin/users/:id/actions/impersonate

        Impersonation allows an admin to begin a new session as another user in the system; for
        more information, see Impersonating a User in the Private Terraform Cloud
        administration section. This endpoint does not respond with a body, but the response
        does include a Set-Cookie header to persist a new session.
        """
        url = f"{self._base_url}/{user_id}/actions/impersonate"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 204:
            self._logger.info(f"Begin impersonating user: {user_id}.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def lst(self, query=None):
        """
        GET /admin/users

        This endpoint lists all user accounts in the Terraform Cloud installation.

        # TODO: handle the rest of the potential parameters
        """
        url = self._base_url
        if query is not None:
            url += f"?q={query}"

        return self._ls(url)

    def revoke_admin(self, user_id):
        """
        POST /admin/users/:id/actions/revoke_admin
        """
        results = None
        url = f"{self._base_url}/{user_id}/actions/revoke_admin"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def suspend(self, user_id):
        """
        POST /admin/users/:id/actions/suspend

        This endpoint suspends a user's account, preventing them from authenticating
        and accessing resources.
        """
        results = None
        url = f"{self._base_url}/{user_id}/actions/suspend"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def unimpersonate(self, user_id):
        """
        POST /admin/users/:id/actions/unimpersonate

        When an admin has used the above endpoint to begin an impersonation session, they
        can make a request to this endpoint, using the cookie provided originally, in order
        to end that session and log out as the impersonated user.

        This endpoint does not respond with a body, but the response does include a
        Set-Cookie header to persist a new session as the original admin user. As such,
        this endpoint will have no effect unless the client is able to persist and use cookies.
        """
        url = f"{self._base_url}/{user_id}/actions/unimpersonate"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 204:
            self._logger.info(f"Stop impersonating user: {user_id}.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def unsuspend(self, user_id):
        """
        POST /admin/users/:id/actions/unsuspend

        This endpoint re-activates a suspended user's account, allowing them to
        resume authenticating and accessing resources.
        """
        results = None
        url = f"{self._base_url}/{user_id}/actions/unsuspend"
        req = requests.post(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results
