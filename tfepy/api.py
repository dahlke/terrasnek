from .organizations import TFEOrganizations
from .workspaces import TFEWorkspaces
from .users import TFEUsers
from .teams import TFETeams
from .team_memberships import TFETeamMemberships
from .team_access import TFETeamAccess

from .admin_users import TFEAdminUsers
from .admin_organizations import TFEAdminOrganizations

TFE_SAAS_URL = "https://app.terraform.io"

class TFE():

    def __init__(self, api_token, url=TFE_SAAS_URL):
        # TODO: custom exception
        if api_token is None:
            raise Exception("Cannot instantiate TFE Api class without a valid TFE_TOKEN.")

        self._instance_url = f"{url}/api/v2"
        self._token = api_token
        self._current_organization = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/vnd.api+json"
        }

        self.organizations = TFEOrganizations(self._instance_url, self._headers)
        self.workspaces = None
        self.users = None

        self.teams = None
        self.team_memberships = None
        self.team_access = None

        self.admin_organizations = TFEAdminOrganizations(self._instance_url, self._headers)
        self.admin_users = None

    
    def set_organization(self, organization_name):
        self._current_organization = organization_name

        self.workspaces = TFEWorkspaces(self._instance_url, self._current_organization, self._headers)
        self.users = TFEUsers(self._instance_url, self._current_organization, self._headers)

        self.admin_users = TFEAdminUsers(self._instance_url, self._current_organization, self._headers)
        
        self.teams = TFETeams(self._instance_url, self._current_organization, self._headers)
        self.team_memberships = TFETeamMemberships(self._instance_url, self._current_organization, self._headers)
        self.team_access = TFETeamAccess(self._instance_url, self._current_organization, self._headers)