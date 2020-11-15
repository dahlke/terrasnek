"""
Module for Terraform Cloud API Endpoint: Admin Users.
"""

from .endpoint import TFCEndpoint

class TFCAdminUsers(TFCEndpoint):
    """
    `Admin Users API Docs \
        <https://www.terraform.io/docs/cloud/api/admin/users.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin/users"

    def _required_entitlements(self):
        return []

    def destroy(self, user_id):
        """
        ``DELETE /admin/users/:id``

        `Admin Users Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#delete-a-user-account>`_
        """
        url = f"{self._endpoint_base_url}/{user_id}"
        return self._destroy(url)

    def disable_two_factor(self, user_id):
        """
        ``POST /admin/users/:id/actions/disable_two_factor``

        `Admin Users Disable Two Factor API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#disable-a-user-39-s-two-factor-authentication>`_
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/disable_two_factor"
        return self._post(url)

    def grant_admin(self, user_id):
        """
        ``POST /admin/users/:id/actions/grant_admin``

        `Admin Users Grant Admin API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#grant-a-user-administrative-privileges>`_
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/grant_admin"
        return self._post(url)

    def impersonate(self, user_id):
        """
        ``POST /admin/users/:id/actions/impersonate``

        `Admin Users Impersonate API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#impersonate-another-user>`_
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/impersonate"
        return self._post(url)

    def list(self, query=None, filters=None, page=None, page_size=None):
        """
        ``GET /admin/users``

        `Admin Users List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#list-all-users>`_
        """
        return self._list(\
            self._endpoint_base_url, query=query, filters=filters, page=page, page_size=page_size)

    def revoke_admin(self, user_id):
        """
        ``POST /admin/users/:id/actions/revoke_admin``

        `Admin Users Revoke Admin API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#revoke-an-user-39-s-administrative-privileges>`_
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/revoke_admin"
        return self._post(url)

    def suspend(self, user_id):
        """
        ``POST /admin/users/:id/actions/suspend``

        `Admin Users Suspend API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#suspend-a-user>`_
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/suspend"
        return self._post(url)

    def unimpersonate(self):
        """
        ``POST /admin/users/actions/unimpersonate``

        `Admin Users Unimpersonate API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#end-an-impersonation-session>`_
        """
        url = f"{self._endpoint_base_url}/actions/unimpersonate"
        return self._post(url)

    def unsuspend(self, user_id):
        """
        ``POST /admin/users/:id/actions/unsuspend``

        `Admin Users Unsuspend API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/users.html#re-activate-a-suspended-user>`_
        """
        url = f"{self._endpoint_base_url}/{user_id}/actions/unsuspend"
        return self._post(url)
