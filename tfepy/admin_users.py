import requests
import json

from .endpoint import TFEEndpoint

class TFEAdminUsers(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._base_url = f"{base_url}/admin/users"
    
    def destroy(self, user_id):
        # DELETE /admin/users/:id
        url = f"{self._base_url}/{user_id}"
        return self._destroy(url)

    def disable_two_factor(self, user_id):
        # POST /admin/users/:id/actions/disable_two_factor
        results = None
        url = f"{self._base_url}/{user_id}/actions/disable_two_factor"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def grant_admin(self, user_id):
        # POST /admin/users/:id/actions/grant_admin
        results = None
        url = f"{self._base_url}/{user_id}/actions/grant_admin"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def impersonate(self, user_id):
        # POST /admin/users/:id/actions/impersonate
        url = f"{self._base_url}/{user_id}/actions/impersonate"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"Begin impersonating user: {user_id}.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)
    
    def ls(self, query=None):
        # GET /admin/users
        # TODO: handle the rest of the potential parameters
        url = self._base_url
        if query != None:
            url += f"?q={query}"

        return self._ls(url)

    def revoke_admin(self, user_id):
        # POST /admin/users/:id/actions/revoke_admin
        results = None
        url = f"{self._base_url}/{user_id}/actions/revoke_admin"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def suspend(self, user_id):
        # POST /admin/users/:id/actions/suspend
        results = None
        url = f"{self._base_url}/{user_id}/actions/suspend"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def unimpersonate(self, user_id):
        # POST /admin/users/:id/actions/unimpersonate
        url = f"{self._base_url}/{user_id}/actions/unimpersonate"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"Stop impersonating user: {user_id}.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def unsuspend(self, user_id):
        # POST /admin/users/:id/actions/unsuspend
        results = None
        url = f"{self._base_url}/{user_id}/actions/unsuspend"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
