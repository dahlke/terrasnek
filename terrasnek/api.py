"""
Module for container class of all TFE endpoints and high level exceptions around
API access.
"""

from._constants import TFE_SAAS_URL

from .oauth_clients import TFEOAuthClients
from .oauth_tokens import TFEOAuthTokens

from .organizations import TFEOrganizations
from .workspaces import TFEWorkspaces
from .variables import TFEVariables
from .config_versions import TFEConfigVersions
from .runs import TFERuns
from .plans import TFEPlans
from .plan_exports import TFEPlanExports
from .state_versions import TFEStateVersions
from .state_version_outputs import TFEStateVersionOutputs
from .applies import TFEApplies
from .users import TFEUsers
from .user_tokens import TFEUserTokens
from .teams import TFETeams
from .team_memberships import TFETeamMemberships
from .team_access import TFETeamAccess
from .team_tokens import TFETeamTokens

from .admin_users import TFEAdminUsers
from .admin_organizations import TFEAdminOrganizations


class InvalidTFETokenException(Exception):
    """Cannot instantiate TFE Api class without a valid TFE_TOKEN."""


class TFE():
    """
    Super class for access to all TFE Endpoints.
    """

    def __init__(self, api_token, url=TFE_SAAS_URL):
        if api_token is None:
            raise InvalidTFETokenException

        self._instance_url = f"{url}/api/v2"
        self._token = api_token
        self._current_organization = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/vnd.api+json"
        }

        self.organizations = TFEOrganizations(
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
        self.admin_organizations = TFEAdminOrganizations(
            self._instance_url, None, self._headers)

        self.oauth_clients = None
        self.oauth_tokens = None

    def set_organization(self, organization_name):
        """
        Sets the organization to use for org specific endpoints.
        This method must be called for their respective endpoints to work.
        """
        self._current_organization = organization_name

        self.workspaces = TFEWorkspaces(
            self._instance_url, self._current_organization, self._headers)
        self.users = TFEUsers(self._instance_url,
                              self._current_organization, self._headers)
        self.user_tokens = TFEUserTokens(
            self._instance_url, self._current_organization, self._headers)
        self.variables = TFEVariables(
            self._instance_url, self._current_organization, self._headers)
        self.config_versions = TFEConfigVersions(
            self._instance_url, self._current_organization, self._headers)
        self.runs = TFERuns(self._instance_url,
                            self._current_organization, self._headers)
        self.applies = TFEApplies(
            self._instance_url, self._current_organization, self._headers)
        self.plans = TFEPlans(self._instance_url,
                              self._current_organization, self._headers)
        self.plan_exports = TFEPlanExports(
            self._instance_url, self._current_organization, self._headers)
        self.state_versions = TFEStateVersions(
            self._instance_url, self._current_organization, self._headers)
        self.state_version_outputs = TFEStateVersionOutputs(
            self._instance_url, self._current_organization, self._headers)

        self.teams = TFETeams(self._instance_url,
                              self._current_organization, self._headers)
        self.team_memberships = TFETeamMemberships(
            self._instance_url, self._current_organization, self._headers)
        self.team_access = TFETeamAccess(
            self._instance_url, self._current_organization, self._headers)
        self.team_tokens = TFETeamTokens(
            self._instance_url, self._current_organization, self._headers)

        self.admin_users = TFEAdminUsers(
            self._instance_url, self._current_organization, self._headers)

        self.oauth_clients = TFEOAuthClients(
            self._instance_url, self._current_organization, self._headers)
        self.oauth_tokens = TFEOAuthTokens(
            self._instance_url, self._current_organization, self._headers)
