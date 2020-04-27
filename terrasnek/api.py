"""
Module for container class of all TFC endpoints and high level exceptions around
API access.
"""

from._constants import TFC_SAAS_URL

from .oauth_clients import TFCOAuthClients
from .oauth_tokens import TFCOAuthTokens

from .organizations import TFCOrganizations
from .organization_memberships import TFCOrganizationMemberships
from .organization_tokens import TFCOrganizationTokens
from .workspaces import TFCWorkspaces
from .variables import TFCVariables
from .config_versions import TFCConfigVersions
from .runs import TFCRuns
from .plans import TFCPlans
from .plan_exports import TFCPlanExports
from .state_versions import TFCStateVersions
from .state_version_outputs import TFCStateVersionOutputs
from .ssh_keys import TFCSSHKeys
from .policies import TFCPolicies
from .policy_sets import TFCPolicySets
from .policy_set_params import TFCPolicySetParams
from .notification_configurations import TFCNotificationConfigurations
from .run_triggers import TFCRunTriggers
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

    def __init__(self, api_token, url=TFC_SAAS_URL, verify=True):
        if api_token is None:
            raise InvalidTFCTokenException

        self._instance_url = f"{url}/api/v2"
        self._token = api_token
        self._verify = verify
        self._current_organization = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/vnd.api+json"
        }

        self.organizations = TFCOrganizations(
            self._instance_url,
            None,
            self._headers,
            self._verify)
        self.organization_memberships = None
        self.organization_tokens = None
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
        self.ssh_keys = None
        self.policies = None
        self.policy_sets = None
        self.policy_set_params = None
        self.notification_configurations = None
        self.run_triggers = None
        self.oauth_clients = None
        self.oauth_tokens = None
        self.teams = None
        self.team_memberships = None
        self.team_access = None
        self.team_tokens = None

        self.admin_organizations = TFCAdminOrganizations(
            self._instance_url,
            None,
            self._headers,
            self._verify)
        self.admin_users = None


    def set_organization(self, organization_name):
        """
        Sets the organization to use for org specific endpoints.
        This method must be called for their respective endpoints to work.
        """
        self._current_organization = organization_name

        # TODO: there is a better way initialize these all the same way.
        self.organization_memberships = TFCOrganizationMemberships(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.organization_tokens = TFCOrganizationTokens(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.workspaces = TFCWorkspaces(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.users = TFCUsers(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.user_tokens = TFCUserTokens(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.variables = TFCVariables(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.config_versions = TFCConfigVersions(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.runs = TFCRuns(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.applies = TFCApplies(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.plans = TFCPlans(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.plan_exports = TFCPlanExports(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.state_versions = TFCStateVersions(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.state_version_outputs = TFCStateVersionOutputs(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.ssh_keys = TFCSSHKeys(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.policies = TFCPolicies(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.policy_sets = TFCPolicySets(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.policy_set_params = TFCPolicySetParams(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.notification_configurations = TFCNotificationConfigurations(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.run_triggers = TFCRunTriggers(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.teams = TFCTeams(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.team_memberships = TFCTeamMemberships(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.team_access = TFCTeamAccess(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.team_tokens = TFCTeamTokens(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.oauth_clients = TFCOAuthClients(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        self.oauth_tokens = TFCOAuthTokens(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

        # Admin Endpoints
        self.admin_users = TFCAdminUsers(
            self._instance_url,
            self._current_organization,
            self._headers,
            self._verify)

