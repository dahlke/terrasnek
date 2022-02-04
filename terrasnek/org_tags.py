"""
Module for Terraform Cloud API Endpoint: Org Tags.
"""

from .endpoint import TFCEndpoint

class TFCOrgTags(TFCEndpoint):
    """
    `Org Tags API Docs \
        <https://www.terraform.io/docs/cloud/api/organization-tags.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._org_tags_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/tags"
        self._tags_base_url = \
            f"{self._api_v2_base_url}/tags"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def list_tags(self, query=None, filters=None, page=None, page_size=None):
        """
        ``GET /organizations/:organization_name/tags``

        `Get Tags API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#get-tags>`_
        """
        return self._list(self._org_tags_base_url, query=query, filters=filters, page=page, page_size=page_size)

    def delete_tags(self, payload):
        """
        ``DELETE /organizations/:organization_name/tags``

        `Delete Tags API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#delete-tags>`_

        `Delete Tags API Doc Sample Payload \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#sample-payload>`_
        """
        return self._destroy(self._org_tags_base_url, data=payload)

    def add_workspaces_to_tag(self, tag_id, payload):
        """
        ``POST /tags/:tag_id/relationships/workspaces``

        `Add Workspace to a Tag API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#add-workspaces-to-a-tag>`_

        `Add Workspace to a Tag API Doc Sample Payload \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#sample-payload-1>`_
        """
        url = f"{self._tags_base_url}/{tag_id}/relationships/workspaces"
        return self._post(url, data=payload)
