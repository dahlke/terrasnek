"""
Module for Terraform Cloud API Endpoint: VCS Events.
"""

from .endpoint import TFCEndpoint

class TFCVCSEvents(TFCEndpoint):
    """
    `VCS Events API Docs \
        <https://www.terraform.io/docs/cloud/api/vcs-events.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._vcs_events_api_v2_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/vcs-events"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        # TODO: change this once it is released in TFE.
        return True

    def terraform_enterprise_only(self):
        return False

    def list(self, page=None, page_size=None, include=None, filters=None):
        """
        ``GET /organizations/:organization_name/vcs-events``

        `VCS Events List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/vcs-events.html#list-vcs-events>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/vcs-events.html#query-parameters>`__):
            - ``page[number]`` (Optional)
            - ``page[size]`` (Optional)
            - ``filter[from]`` (Optional)
            - ``filter[to]`` (Optional)
            - ``filter[oauth_client_external_ids]`` (Optional)
            - ``filter[levels]`` (Optional)
            - ``include`` (Optional)

        Example filter(s):

        .. code-block:: python

            filters = [
                {
                    "keys": ["from"],
                    "value": "foo"
                },
                {
                    "keys": ["to"],
                    "value": "bar"
                }
            ]

        NOTE / TODO: Currently, this feature is in beta, and only supports GitLab.
        Since all of the testing is done with GitHub, this function is
        provided, but is not well tested yet.
        """

        return self._list(self._vcs_events_api_v2_base_url, \
            page=page, page_size=page_size, include=include, filters=filters)
