from .organizations import TFEOrganizations
from .workspaces import TFEWorkspaces

TFE_SAAS_URL = "https://app.terraform.io"

class TFE():

    def __init__(self, api_token, url=TFE_SAAS_URL):
        self._instance_url = f"{url}/api/v2"
        self._token = api_token
        self._current_organization = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/vnd.api+json"
        }

        self.organizations = TFEOrganizations(self._instance_url, self._headers)
        self.workspaces = None

    
    def set_organization(self, organization_name):
        self._current_organization = organization_name
        self.workspaces = TFEWorkspaces(self._instance_url, self._current_organization, self._headers)