"""
Module for Terraform Cloud API Endpoint: Plan Exports.
"""

from .endpoint import TFCEndpoint

class TFCPlanExports(TFCEndpoint):
    """
    Plan exports allow users to download data exported from the plan of a Run in a Terraform
    workspace. Currently, the only supported format for exporting plan data is to generate mock
    data for Sentinel.

    https://www.terraform.io/docs/cloud/api/plan-exports.html
    """

    def __init__(self, base_url, org_name, headers, verify):
        super().__init__(base_url, org_name, headers, verify)
        self._base_url = f"{base_url}/plan-exports"

    def create(self, payload):
        """
        POST /plan-exports

        This endpoint exports data from a plan in the specified format. The export process
        is asynchronous, and the resulting data becomes downloadable when its status is
        "finished". The data is then available for one hour before expiring. After the hour
        is up, a new export can be created.
        """

        return self._create(self._base_url, payload)

    def show(self, plan_export_id):
        """
        GET /plan-exports/:plan_export_id

        There is no endpoint to list plan exports. You can find IDs for plan exports in the
        relationships.exports property of a plan object.
        """
        url = f"{self._base_url}/{plan_export_id}"
        return self._show(url)

    def download(self, plan_export_id, target_path="/tmp/terrasnek.planexport.tar.gz"):
        """
        GET /plan-exports/:plan_export_id/download

        This endpoint generates a temporary URL to the location of the exported plan data in
        a .tar.gz archive, and then redirects to that link. If using a client that can follow
        redirects, you can use this endpoint to save the .tar.gz archive locally without needing
        to save the temporary URL.
        """
        url = f"{self._base_url}/{plan_export_id}/download"
        results = self._get(url, return_raw=True)
        with open(target_path, 'wb') as target_file:
            target_file.write(results)

    def destroy(self, plan_export_id):
        """
        DELETE /plan-exports/:plan_export_id

        Plan exports expire after being available for one hour, but they can be deleted
        manually as well.
        """
        url = f"{self._base_url}/{plan_export_id}"
        return self._destroy(url)
