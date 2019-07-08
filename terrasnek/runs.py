import requests
import json

from .endpoint import TFEEndpoint

class TFERuns(TFEEndpoint):
    
    def __init__(self, base_url, organization_name, headers):
        super().__init__(base_url, headers)
        self._ws_base_url = f"{base_url}/workspaces"
        self._runs_base_url = f"{base_url}/runs"
    
    def ls(self, workspace_id):
        # GET /workspaces/:workspace_id/runs
        url = f"{self._ws_base_url}/{workspace_id}/runs"
        return self._ls(url)

    def show(self, run_id):
        # GET /runs/:run_id
        url = f"{self._runs_base_url}/{run_id}"
        return self._show(url)
    
    def create(self, payload):
        # POST /runs
        return self._create(self._runs_base_url, payload)
    
    def apply(self, run_id):
        # POST /runs/:run_id/actions/apply
        url = f"{self._runs_base_url}/{run_id}/actions/apply"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 202:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def discard(self, run_id):
        # POST /runs/:run_id/actions/discard
        url = f"{self._runs_base_url}/{run_id}/actions/discard"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 202:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def cancel(self, run_id):
        # POST /runs/:run_id/actions/cancel
        url = f"{self._runs_base_url}/{run_id}/actions/cancel"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 202:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def force_cancel(self, run_id):
        # POST /runs/:run_id/actions/force-cancel
        url = f"{self._runs_base_url}/{run_id}/actions/force-cancel"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 202:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def force_execute(self, run_id):
        # POST /runs/:run_id/actions/force-execute
        url = f"{self._runs_base_url}/{run_id}/actions/force-execute"
        r = requests.post(url, headers=self._headers)

        if r.status_code == 202:
            pass
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)