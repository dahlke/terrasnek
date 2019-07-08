import requests
import json

from .endpoint import TFEEndpoint

class TFEWorkspaces(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._organization_name = organization_name
        self._ws_base_url = f"{base_url}/workspaces"
        self._org_base_url = f"{base_url}/organizations/{organization_name}/workspaces"
    
    def assign_ssh_key(self, workspace_id):
        # PATCH /workspaces/:workspace_id/relationships/ssh-key
        url = f"{self._ws_base_url}/{workspace_id}/relationships/ssh-key"
        # TODO: requires SSH key endpoint
        self._logger.error("Assign SSH Key is not yet implemented.")

    def create(self, payload):
        # POST /organizations/:organization_name/workspaces
        return self._create(self._org_base_url, payload)

    def destroy(self, workspace_id=None, workspace_name=None):
        if workspace_name is not None:
            # GET /organizations/:organization_name/workspaces/:name
            url = f"{self._org_base_url}/{workspace_name}"
        elif workspace_id is not None:
            # DELETE /workspaces/:workspace_id
            url = f"{self._ws_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._destroy(url)

    def force_unlock(self, workspace_id):
        # POST /workspaces/:workspace_id/actions/force-unlock
        results = None
        url = f"{self._ws_base_url}/{workspace_id}/actions/force-unlock"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def lock(self, workspace_id, payload):
        # POST /workspaces/:workspace_id/actions/lock
        results = None
        url = f"{self._ws_base_url}/{workspace_id}/actions/lock"
        r = requests.post(url, json.dumps(payload), headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def ls(self):
        # GET /organizations/:organization_name/workspaces
        return self._ls(self._org_base_url)

    def show(self, workspace_name=None, workspace_id=None):
        if workspace_name is not None:
            # GET /organizations/:organization_name/workspaces/:name
            url = f"{self._org_base_url}/{workspace_name}"
        elif workspace_id is not None:
            # GET /workspaces/:workspace_id
            url = f"{self._ws_base_url}/{workspace_id}"
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._show(url)

    def unassign_ssh_key(self, workspace_id):
        # PATCH /workspaces/:workspace_id/relationships/ssh-key
        url = f"{self._ws_base_url}/{workspace_id}/relationships/ssh-key"
        # TODO: requires SSH key endpoint
        self._logger.error("Unassign SSH Key is not yet implemented.")

    def unlock(self, workspace_id):
        # POST /workspaces/:workspace_id/actions/unlock
        results = None
        url = f"{self._ws_base_url}/{workspace_id}/actions/unlock"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def update(self, workspace_id, payload):
        # PATCH /workspaces/:workspace_id
        url = f"{self._ws_base_url}/{workspace_id}"
        return self._update(url, payload)
