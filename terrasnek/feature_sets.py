"""
Module for Terraform Cloud API Endpoint: Feature Sets.
"""

from .endpoint import TFCEndpoint

class TFCFeatureSets(TFCEndpoint):
    """
    `Feature Sets API Docs \
        <https://www.terraform.io/docs/cloud/api/feature-sets.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/feature-sets"
        self._org_base_url = \
            f"{self._api_v2_base_url}/organizations/{org_name}/feature-sets"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return True

    def terraform_enterprise_only(self):
        return False

    def list(self):
        """
        ``GET /feature-sets``

        `Feature Sets List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/feature-sets.html>`_
        """
        return self._list(self._endpoint_base_url)

    def list_for_org(self):
        """
        ``GET /organizations/:organization_name/feature-sets``

        `Feature Sets List for Orgs API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/feature-sets.html#list-feature-sets-for-organization>`_
        """
        return self._list(self._org_base_url)
