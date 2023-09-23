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
    TFCHTTPInternalServerError, TFCHTTPUnclassified, TFCHTTPAPIRequestRateLimit

from ._constants import \
    HTTP_OK, HTTP_CREATED, HTTP_ACCEPTED, HTTP_NO_CONTENT, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED, \
          HTTP_FORBIDDEN, HTTP_NOT_FOUND, HTTP_CONFLICT, HTTP_PRECONDITION_FAILED, \
             HTTP_UNPROCESSABLE_ENTITY, HTTP_API_REQUEST_RATE_LIMIT_REACHED, \
                HTTP_INTERNAL_SERVER_ERROR, MAX_PAGE_SIZE, HTTP_MOVED_PERMANENTLY, \
                HTTP_MOVED_TEMPORARILY, TFC_SAAS_HOSTNAME


class TFCEndpoint(ABC):
    """
    Base class providing common CRUD operation implementations across all TFC Endpoints.
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)

        self._instance_url = \
            instance_url if instance_url[-1] != "/" else instance_url[:-1]
        self._api_v2_base_url = f"{self._instance_url}{well_known_paths['tfe.v2'][:-1]}"
        self._meta_base_url = f"{self._instance_url}/api/meta"
        self._mods_v1_base_url = f"{self._instance_url}{well_known_paths['modules.v1'][:-1]}"
        # TODO: support the public registry workflows?
        # self._public_registry_v1_url = "https://registry.terraform.io/v1/modules"
        self._headers = headers
        self._org_name = org_name
        self._verify = verify

    @abstractmethod
    def required_entitlements(self):
        """
        Terraform Cloud Entitlements required for endpoint to work.
        """
        return []

    @abstractmethod
    def terraform_cloud_only(self):
        """
        Return ``True`` if this endpoint is only for Terraform Cloud, else ``False``.
        """
        return False

    @abstractmethod
    def terraform_enterprise_only(self):
        """
        Return ``True`` if this endpoint is only for Terraform Enterprise, else ``False``.
        """
        return False

    def is_terraform_cloud(self):
        """
        Returns true if this API instance is configured for Terraform Cloud.
        """
        return TFC_SAAS_HOSTNAME in self._instance_url

    def _delete(self, url, data=None):
        req = requests.delete(
            url, data=json.dumps(data), headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_OK:
            self._logger.debug(f"Terraform Cloud resource at URL [{url}] destroyed.")
        elif req.status_code == HTTP_NO_CONTENT:
            self._logger.debug(f"Terraform Cloud resource at URL [{url}] destroyed.")
        elif req.status_code == HTTP_NOT_FOUND:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPNotFound(err)
        elif req.status_code == HTTP_FORBIDDEN:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPForbidden(err)
        elif req.status_code == HTTP_API_REQUEST_RATE_LIMIT_REACHED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPAPIRequestRateLimit(err)
        else:
            try:
                err = json.loads(req.content.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                err = req.content
            self._logger.debug(err)
            raise TFCHTTPUnclassified(err)

    # pylint: disable=too-many-statements,too-many-branches
    def _get(self, url, return_raw=None, allow_redirects=None, query=None, filters=None, \
          page=None, page_size=None, search=None, include=None, sort=None, \
            offset=None, limit=None, provider=None, namespace=None, verified=None, \
                since=None):

        results = None

        q_options = []

        if query is not None:
            q_options.append(f"q={query}")

        if filters is not None:
            if isinstance(filters, list):
                if filters:
                    for fil in filters:
                        filter_string = "filter"
                        for k in fil["keys"]:
                            filter_string += f"[{k}]"
                        filter_string += f"={fil['value']}"
                        q_options.append(filter_string)
            else:
                raise TypeError("The `filters` parameter must be of `list` type.")

        if include is not None:
            if isinstance(include, list):
                if include:
                    joined_include = ",".join(include)
                    q_options.append(f"include={joined_include}")
            else:
                raise TypeError("The `include` parameter must be of `list` type.")

        if page is not None:
            q_options.append(f"page[number]={page}")

        if page_size is not None:
            q_options.append(f"page[size]={page_size}")

        if sort is not None:
            q_options.append(f"sort={sort}")

        if search is not None:
            if "name" in search:
                q_options.append(f"search[name]={search['name']}")

            if "tags" in search:
                q_options.append(f"search[tags]={search['tags']}")

            if "user" in search:
                q_options.append(f"search[user]={search['user']}")

            if "commit" in search:
                q_options.append(f"search[commit]={search['commit']}")

            if "basic" in search:
                q_options.append(f"search[basic]={search['basic']}")

        if since is not None:
            q_options.append(f"since={since}")

        # V1 Modules API options
        # NOTE: The `offset` parameter is not in use very much now, but remains for
        # backwards compatibility.
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

        self._logger.debug(f"Trying HTTP GET to URL: {url} ...")
        req = requests.get(
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
            # URL to match the private module registry URL schema. At some point
            # in the future, this may need to use HTTP_MOVED_TEMPORARILY.
            url = req.url.replace("/v1/modules/", "/api/registry/v1/modules/")
            results = {"redirect-url": url}
        elif req.status_code == HTTP_MOVED_TEMPORARILY:
            results = req.content.decode("utf-8")
        elif req.status_code == HTTP_MOVED_PERMANENTLY:
            self._logger.info(
                "HTTP_MOVED_PERMANENTLY, this is unexpected and should be investigated.")
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
        elif req.status_code == HTTP_UNAUTHORIZED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPUnauthorized(err)
        elif req.status_code == HTTP_NOT_FOUND:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPNotFound(err)
        elif req.status_code == HTTP_API_REQUEST_RATE_LIMIT_REACHED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPAPIRequestRateLimit(err)
        else:
            try:
                err = json.loads(req.content.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                err = req.content
            self._logger.debug(err)
            raise TFCHTTPUnclassified(err)

        return results

    def _patch(self, url, data=None):
        results = None

        self._logger.debug(f"Trying HTTP PATCH to URL: {url} ...")
        req = requests.patch(url, data=json.dumps(
            data), headers=self._headers, verify=self._verify)

        if req.status_code in [HTTP_OK, HTTP_CREATED]:
            results = json.loads(req.content)
        elif req.status_code == HTTP_BAD_REQUEST:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPBadRequest(err)
        elif req.status_code == HTTP_UNAUTHORIZED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPUnauthorized(err)
        elif req.status_code == HTTP_UNPROCESSABLE_ENTITY:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPUnprocessableEntity(err)
        elif req.status_code == HTTP_API_REQUEST_RATE_LIMIT_REACHED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPAPIRequestRateLimit(err)
        elif req.status_code == HTTP_CONFLICT:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPConflict(err)
        elif req.status_code == HTTP_NO_CONTENT:
            pass
        else:
            # print(req.status_code)
            try:
                err = json.loads(req.content.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                err = req.content
            self._logger.debug(err)
            raise TFCHTTPUnclassified(err)

        return results

    def _post(self, url, data=None):
        results = None

        self._logger.debug(f"Trying HTTP POST to URL: {url} ...")
        req = requests.post(url, data=json.dumps(
            data), headers=self._headers, verify=self._verify)

        if req.status_code in [HTTP_OK, HTTP_CREATED]:
            results = json.loads(req.content)
            self._logger.debug(f"POST to {url} successful")
        elif req.status_code in [HTTP_ACCEPTED, HTTP_NO_CONTENT]:
            self._logger.debug(f"POST to {url} successful")
        elif req.status_code == HTTP_BAD_REQUEST:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPBadRequest(err)
        elif req.status_code == HTTP_NOT_FOUND:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPNotFound(err)
        elif req.status_code == HTTP_CONFLICT:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPConflict(err)
        elif req.status_code == HTTP_PRECONDITION_FAILED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPPreconditionFailed(err)
        elif req.status_code == HTTP_UNPROCESSABLE_ENTITY:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPUnprocessableEntity(err)
        elif req.status_code == HTTP_API_REQUEST_RATE_LIMIT_REACHED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPAPIRequestRateLimit(err)
        elif req.status_code == HTTP_INTERNAL_SERVER_ERROR:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPInternalServerError(err)
        else:
            try:
                err = json.loads(req.content.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                err = req.content
            self._logger.debug(err)
            raise TFCHTTPUnclassified(err)

        return results

    def _put(self, url, octet=False, data=None):
        results = None

        headers = dict.copy(self._headers)
        if octet is True:
            headers["Content-Type"] = "application/octet-stream"
            data = bytes(data, "utf-8")

        self._logger.debug(f"Trying HTTP PUT to URL: {url} ...")
        req = requests.put(url, data=data, headers=headers, verify=self._verify)

        if req.status_code == HTTP_OK:
            if octet:
                results = json.loads(req.content)
            self._logger.debug(f"PUT to {url} successful")
        elif req.status_code == HTTP_API_REQUEST_RATE_LIMIT_REACHED:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.debug(err)
            raise TFCHTTPAPIRequestRateLimit(err)
        else:
            try:
                err = json.loads(req.content.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                err = req.content
            self._logger.debug(err)
            raise TFCHTTPUnclassified(err)

        return results

    def _create(self, url, payload=None):
        """
        Implementation the common create resource pattern for the TFC API.
        """
        if payload is None:
            payload = {}

        return self._post(url, data=payload)

    def _destroy(self, url, data=None):
        """
        Implementation of the common destroy resource pattern for the TFC API.

        NOTE: This is basically an alias to the _delete method, but is more
        along the verbiage used in the docs.
        """
        self._delete(url, data=data)

    def _list(self, url, query=None, filters=None, \
        page=None, page_size=None, search=None, include=None, sort=None, \
            offset=None, limit=None, provider=None, namespace=None, verified=None, \
                since=None):
        """
        Implementation of the common list resources pattern for the TFC API.
        """
        return self._get(url, query=query, filters=filters, page=page, \
            page_size=page_size, search=search, include=include, sort=sort, \
                offset=offset, limit=limit, provider=provider, namespace=namespace, \
                    verified=verified, since=since)

    def _list_all(self, url, include=None, search=None, filters=None, query=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every workspace in an organization.

        Returns an object with two arrays of objects.
        """
        current_page_number = 1
        list_resp = \
                    self._list(url, page=current_page_number, page_size=MAX_PAGE_SIZE, include=include,
                               search=search, filters=filters, query=query)

        if "meta" in list_resp:
            total_pages = list_resp["meta"]["pagination"]["total-pages"]
        elif "pagination" in list_resp:
            total_pages = list_resp["pagination"]["total_pages"]

        included = []
        data = []

        while current_page_number <= total_pages:
            list_resp = \
                self._list(url, page=current_page_number, page_size=MAX_PAGE_SIZE, \
                    include=include, search=search, filters=filters, query=query)
            data += list_resp["data"]

            if "included" in list_resp:
                included += list_resp["included"]

            current_page_number += 1

        return {
            "data": data,
            "included": included
        }

    def _show(self, url, include=None):
        """
        Implementation of the common show resource pattern for the TFC API.
        """
        return self._get(url, include=include)

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
