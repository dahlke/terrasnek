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

    def list_tags(self):
        """
        ``GET /organizations/:organization_name/tags``

        `Get Tags API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#get-tags>`_
        """
        # TODO: does this support pagination?
        return self._get(self._org_tags_base_url)

    def delete_tags(self, payload):
        """
        ``DELETE /organizations/:organization_name/tags``

        `Delete Tags API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#delete-tags>`_

        `Delete Tags API Doc Sample Payload \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#sample-payload>`_
        """
        return self._delete(self._org_tags_base_url, data=payload)

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

    # NOTE: this endpoint has been temporarily removed
    """
    def remove_workspaces_from_tag(self, tag_id, payload):
        \"""
        ``DELETE /tags/:tag_id/relationships/workspaces``

        `Remove Workspaces from Tags API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/organization-tags.html#remove-workspaces-from-a-tag>`_

        `Remove Workspaces from Tags API Doc Sample Payload \
            <>`_
        \"""
        url = f"{self._tags_base_url}/{tag_id}/relationships/workspaces"
        return self._delete(url, data=payload)
    """
