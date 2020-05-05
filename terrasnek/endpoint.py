"""
Module containing class for common endpoint implementations across all TFC Endpoints.
"""

import json
import logging
import requests

from._constants import HTTP_OK, HTTP_CREATED, HTTP_ACCEPTED, HTTP_NO_CONTENT


class TFCEndpoint():
    """
    Base class providing common CRUD operation implementations across all TFC Endpoints.
    """

    def __init__(self, base_url, org_name, headers, verify):
        self._base_url = base_url
        self._headers = headers
        self._org_name = org_name
        self._verify = verify
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

    def _delete(self, url, data=None):
        results = None
        req = requests.delete(\
            url, data=json.dumps(data), headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_NO_CONTENT:
            pass
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _get(self, url, return_raw=False):
        results = None
        req = requests.get(url, headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_OK and not return_raw:
            results = json.loads(req.content)
            self._logger.debug(f"GET to {url} successful")
        elif req.status_code == HTTP_OK and return_raw:
            results = req.content
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _patch(self, url, data=None):
        results = None
        req = requests.patch(url, data=json.dumps(data), headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_OK:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _post(self, url, data=None):
        results = None
        req = requests.post(url, data=json.dumps(data), headers=self._headers, verify=self._verify)

        if req.status_code in [HTTP_OK, HTTP_CREATED]:
            results = json.loads(req.content)
            self._logger.debug(f"POST to {url} successful")
        elif req.status_code in [HTTP_ACCEPTED, HTTP_NO_CONTENT]:
            self._logger.debug(f"POST to {url} successful")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _put(self, url, octet=False, data=None):
        results = None

        headers = dict.copy(self._headers)
        if octet is True:
            headers["Content-Type"] = "application/octet-stream"
            data = bytes(data, "utf-8")

        req = requests.put(url, data=data, headers=headers, verify=self._verify)

        if req.status_code == HTTP_OK:
            if octet:
                results = json.loads(req.content)
            self._logger.debug(f"PUT to {url} successful")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _create(self, url, payload):
        """
        Implementation the common create resource pattern for the TFC API.
        """
        return self._post(url, data=payload)

    def _destroy(self, url):
        """
        Implementation of the common destroy resource pattern for the TFC API.
        """
        req = requests.delete(url, headers=self._headers, verify=self._verify)

        valid_status_codes = [HTTP_OK, HTTP_NO_CONTENT]
        if req.status_code in valid_status_codes:
            self._logger.debug(f"Terraform Cloud resource at URL [{url}] destroyed.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def _list(self, url, query=None, filters=None, \
        page=None, page_size=None, search=None, include=None):
        """
        Implementation of the common list resources pattern for the TFC API.
        """
        q_options = []

        if query is not None:
            q_options.append(f"q={query}")

        if filters is not None:
            for fil in filters:
                filter_string = "filter"
                for k in fil["keys"]:
                    filter_string += f"[{k}]"
                filter_string += f"={fil['value']}"
                q_options.append(filter_string)

        if page is not None:
            q_options.append(f"page[number]={page}")

        if page_size is not None:
            q_options.append(f"page[size]={page_size}")

        if search is not None:
            q_options.append(f"page[name]={page_size}")

        if include is not None:
            q_options.append(f"include={include}")

        if search is not None:
            q_options.append(f"search[name]={search}")

        if q_options:
            url += "?" + "&".join(q_options)

        return self._get(url)

    def _show(self, url):
        """
        Implementation of the common show resource pattern for the TFC API.
        """
        return self._get(url)

    def _update(self, url, payload):
        """
        Implementation of the common update resource pattern for the TFC API.
        """
        return self._patch(url, data=payload)
