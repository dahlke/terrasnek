import logging
import requests
import json

class TFEEndpoint():

    def __init__(self, base_url, headers):
        # TODO: Bring in the TFE Api class here unless I want to manage all that state in a session.
        self._base_url = base_url
        self._headers = headers
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)
    
    def _create(self, url, payload):
        results = None
        r = requests.post(url, json.dumps(payload), headers=self._headers)

        if r.status_code == 201:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _destroy(self, url):
        r = requests.delete(url, headers=self._headers)

        if r.status_code == 204:
            self._logger.info(f"OAuth client {id} destroyed.")
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

    def _ls(self, url):
        results = None
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results


    def _show(self, url):
        results = None
        r = requests.get(url, headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
    
    def _update(self, url, payload):
        r = requests.patch(url, data=json.dumps(payload), headers=self._headers)

        if r.status_code == 200:
            results = json.loads(r.content)
        else:
            err = json.loads(r.content.decode("utf-8"))
            self._logger.error(err)

        return results
