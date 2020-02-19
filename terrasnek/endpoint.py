"""
Module containing class for common endpoint implementations across all TFC Endpoints.
"""

import json
import logging
import requests

class TFCEndpoint():
    """
    Base class providing common CRUD operation implementations across all TFC Endpoints.
    """

    def __init__(self, base_url, organization_name, headers):
        self._base_url = base_url
        self._headers = headers
        self._organization_name = organization_name
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

    def _create(self, url, payload):
        """
        Implementation the common create resource pattern for the TFC API.
        """
        results = None
        req = requests.post(url, json.dumps(payload), headers=self._headers)

        if req.status_code == 201:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _destroy(self, url):
        """
        Implementation of the common destroy resource pattern for the TFC API.
        """
        req = requests.delete(url, headers=self._headers)

        valid_status_codes = [200, 204]
        if req.status_code in valid_status_codes:
            self._logger.debug(f"Terraform Cloud resource at URL [{url}] destroyed.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def _ls(self, url):
        """
        Implementation of the common list resources pattern for the TFC API.
        """
        results = None
        req = requests.get(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results


    def _show(self, url):
        """
        Implementation of the common show resource pattern for the TFC API.
        """
        results = None
        req = requests.get(url, headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _update(self, url, payload):
        """
        Implementation of the common update resource pattern for the TFC API.
        """
        req = requests.patch(url, data=json.dumps(payload), headers=self._headers)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results
