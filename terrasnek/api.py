"""
Module for container class of all TFC endpoints and high level exceptions around
API access.
"""

from._constants import TFC_SAAS_URL

from .oauth_clients import TFCOAuthClients
from .oauth_tokens import TFCOAuthTokens

from .organizations import TFCOrganizations
from .workspaces import TFCWorkspaces
from .variables import TFCVariables
from .config_versions import TFCConfigVersions
from .runs import TFCRuns
from .plans import TFCPlans
from .plan_exports import TFCPlanExports
from .state_versions import TFCStateVersions
from .state_version_outputs import TFCStateVersionOutputs
from .applies import TFCApplies
from .users import TFCUsers
from .user_tokens import TFCUserTokens
from .teams import TFCTeams
from .team_memberships import TFCTeamMemberships
from .team_access import TFCTeamAccess
from .team_tokens import TFCTeamTokens

from .admin_users import TFCAdminUsers
from .admin_organizations import TFCAdminOrganizations


class InvalidTFCTokenException(Exception):
    """Cannot instantiate TFC Api class without a valid TFC_TOKEN."""


class TFC():
    """
    Super class for access to all TFC Endpoints.
    """

    def __init__(self, api_token, url=TFC_SAAS_URL):
        if api_token is None:
            raise InvalidTFCTokenException

        self._instance_url = f"{url}/api/v2"
        self._token = api_token
        self._current_organization = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/vnd.api+json"
        }

        self.organizations = TFCOrganizations(
            self._instance_url, None, self._headers)
        self.workspaces = None
        self.users = None
        self.user_tokens = None
        self.variables = None
        self.config_versions = None
        self.runs = None
        self.applies = None
        self.plans = None
        self.plan_exports = None
        self.state_versions = None
        self.state_version_outputs = None

        self.teams = None
        self.team_memberships = None
        self.team_access = None
        self.team_tokens = None

        self.admin_users = None
        self.admin_organizations = TFCAdminOrganizations(
            self._instance_url, None, self._headers)

        self.oauth_clients = None
        self.oauth_tokens = None

    def set_organization(self, organization_name):
        """
        Sets the organization to use for org specific endpoints.
        This method must be called for their respective endpoints to work.
        """
        self._current_organization = organization_name

        self.workspaces = TFCWorkspaces(
            self._instance_url, self._current_organization, self._headers)
        self.users = TFCUsers(self._instance_url,
                              self._current_organization, self._headers)
        self.user_tokens = TFCUserTokens(
            self._instance_url, self._current_organization, self._headers)
        self.variables = TFCVariables(
            self._instance_url, self._current_organization, self._headers)
        self.config_versions = TFCConfigVersions(
            self._instance_url, self._current_organization, self._headers)
        self.runs = TFCRuns(self._instance_url,
                            self._current_organization, self._headers)
        self.applies = TFCApplies(
            self._instance_url, self._current_organization, self._headers)
        self.plans = TFCPlans(self._instance_url,
                              self._current_organization, self._headers)
        self.plan_exports = TFCPlanExports(
            self._instance_url, self._current_organization, self._headers)
        self.state_versions = TFCStateVersions(
            self._instance_url, self._current_organization, self._headers)
        self.state_version_outputs = TFCStateVersionOutputs(
            self._instance_url, self._current_organization, self._headers)

        self.teams = TFCTeams(self._instance_url,
                              self._current_organization, self._headers)
        self.team_memberships = TFCTeamMemberships(
            self._instance_url, self._current_organization, self._headers)
        self.team_access = TFCTeamAccess(
            self._instance_url, self._current_organization, self._headers)
        self.team_tokens = TFCTeamTokens(
            self._instance_url, self._current_organization, self._headers)

        self.admin_users = TFCAdminUsers(
            self._instance_url, self._current_organization, self._headers)

        self.oauth_clients = TFCOAuthClients(
            self._instance_url, self._current_organization, self._headers)
        self.oauth_tokens = TFCOAuthTokens(
            self._instance_url, self._current_organization, self._headers)
