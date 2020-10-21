"""
Module containing class for common endpoint implementations across all TFC Endpoints.
"""

from abc import ABC, abstractmethod

import json
import logging
import requests

from .exceptions import \
    TFCHTTPBadRequest, TFCHTTPUnauthorized, TFCHTTPForbidden, TFCHTTPNotFound, \
        TFCHTTPConflict, TFCHTTPPreconditionFailed, TFCHTTPUnprocessableEntity, \
            TFCHTTPInternalServerError, TFCHTTPUnclassified

from ._constants import \
    HTTP_OK, HTTP_CREATED, HTTP_ACCEPTED, HTTP_NO_CONTENT, HTTP_MOVED_TEMPORARILY, \
        HTTP_TEMPORARY_REDIRECT, HTTP_NOT_MODIFIED, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED, \
            HTTP_FORBIDDEN, HTTP_NOT_FOUND, HTTP_CONFLICT, HTTP_PRECONDITION_FAILED, \
                HTTP_UNPROCESSABLE_ENTITY, HTTP_INTERNAL_SERVER_ERROR


class TFCEndpoint(ABC):
    """
    Base class providing common CRUD operation implementations across all TFC Endpoints.
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)

        # Remove the slack at the end if someone adds it.
        self._instance_url = \
            instance_url if instance_url[-1] != "/" else instance_url[:-1]
        self._api_v2_base_url = f"{self._instance_url}{well_known_paths['tfe.v2'][:-1]}"
        self._meta_base_url = f"{self._instance_url}/api/meta"
        self._modules_v1_base_url = f"{self._instance_url}{well_known_paths['modules.v1']}"
        self._headers = headers
        self._org_name = org_name
        self._verify = verify

    @abstractmethod
    def _required_entitlements(self):
        """
        Terraform Cloud Entitlements required for endpoint to work.
        """
        return []

    def _delete(self, url, data=None):
        results = None
        req = requests.delete(\
            url, data=json.dumps(data), headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_NO_CONTENT:
            pass
        elif req.status_code == HTTP_NOT_FOUND:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPNotFound()
        elif req.status_code == HTTP_FORBIDDEN:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPForbidden()
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnclassified()

        return results

    def _get(self, url, return_raw=False, allow_redirects=False):
        results = None

        req = requests.get(\
            url, headers=self._headers, verify=self._verify, allow_redirects=allow_redirects)

        if req.status_code == HTTP_OK and not return_raw:
            results = json.loads(req.content)
            self._logger.debug(f"GET to {url} successful")
        elif req.status_code == HTTP_OK and return_raw:
            results = req.content
        elif req.status_code == HTTP_NO_CONTENT:
            results = req.headers
        elif req.history:
            # NOTE: If we got redirected, run the get on the new URL, and fix the
            # URL to match the private module registry URL schema.
            url = req.url.replace("/v1/modules/", "/api/registry/v1/modules/")
            results = {"redirect-url": url}
        elif req.status_code == HTTP_UNAUTHORIZED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnauthorized()
        elif req.status_code == HTTP_NOT_FOUND:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPNotFound()
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnclassified()

        return results

    def _patch(self, url, data=None):
        results = None
        req = requests.patch(url, data=json.dumps(data), headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_OK:
            results = json.loads(req.content)
        elif req.status_code == HTTP_BAD_REQUEST:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPBadRequest()
        elif req.status_code == HTTP_UNAUTHORIZED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnauthorized()
        elif req.status_code == HTTP_UNPROCESSABLE_ENTITY:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnprocessableEntity()
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnclassified()

        return results

    def _post(self, url, data=None):
        results = None
        req = requests.post(url, data=json.dumps(data), headers=self._headers, verify=self._verify)

        if req.status_code in [HTTP_OK, HTTP_CREATED]:
            results = json.loads(req.content)
            self._logger.debug(f"POST to {url} successful")
        elif req.status_code in [HTTP_ACCEPTED, HTTP_NO_CONTENT]:
            self._logger.debug(f"POST to {url} successful")
        elif req.status_code == HTTP_BAD_REQUEST:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPBadRequest()
        elif req.status_code == HTTP_NOT_FOUND:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPNotFound()
        elif req.status_code == HTTP_CONFLICT:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPConflict()
        elif req.status_code == HTTP_PRECONDITION_FAILED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPPreconditionFailed()
        elif req.status_code == HTTP_UNPROCESSABLE_ENTITY:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnprocessableEntity()
        elif req.status_code == HTTP_INTERNAL_SERVER_ERROR:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPInternalServerError()
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            raise TFCHTTPUnclassified()

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
            raise TFCHTTPUnclassified()

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
            raise TFCHTTPUnclassified()

    def _list(self, url, query=None, filters=None, \
        page=None, page_size=None, search=None, include=None, sort=None, \
        offset=None, limit=None, provider=None, namespace=None, verified=None, \
        since=None):
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

        if sort is not None:
            q_options.append(f"sort={sort}")

        if search is not None:
            q_options.append(f"search[name]={search}")

        if since is not None:
            q_options.append(f"since={since}")

        # V1 Modules API options
        if offset is not None:
            q_options.append(f"offset={offset}")

        if limit is not None:
            q_options.append(f"limit={limit}")

        if provider is not None:
            q_options.append(f"provider={provider}")

        if namespace is not None:
            q_options.append(f"namespace={namespace}")

        if verified is not None:
            q_options.append(f"verified={verified}")

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

    def _download(self, url, target_path, header_with_url=None, allow_redirects=False):
        """
        Implementation of a common download pattern from the TFC API.
        """
        results = None
        if header_with_url is None:
            results = self._get(url, return_raw=True, allow_redirects=allow_redirects)
        else:
            response = self._get(url, allow_redirects=allow_redirects)
            if "redirect-url" in response:
                response = self._get(response["redirect-url"])
            download_url = response[header_with_url]
            results = self._get(download_url, return_raw=True)

        with open(target_path, 'wb') as target_file:
            target_file.write(results)

    def get_current_org(self):
        """
        Return the active org for this endpoint.
        """
        return self._org_name
