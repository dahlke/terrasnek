"""
Module for container class of all TFC endpoints and high level exceptions around
API access.
"""

import json
import logging
import requests
import urllib3

from._constants import TFC_SAAS_URL, HTTP_OK, LOG_LEVEL
from .account import TFCAccount
from .admin_orgs import TFCAdminOrgs
from .admin_runs import TFCAdminRuns
from .admin_settings import TFCAdminSettings
from .admin_terraform_versions import TFCAdminTerraformVersions
from .admin_users import TFCAdminUsers
from .admin_workspaces import TFCAdminWorkspaces
from .agents import TFCAgents
from .agent_tokens import TFCAgentTokens
from .applies import TFCApplies
from .audit_trails import TFCAuditTrails
from .config_versions import TFCConfigVersions
from .cost_estimates import TFCCostEstimates
from .ip_ranges import TFCIPRanges
from .oauth_clients import TFCOAuthClients
from .oauth_tokens import TFCOAuthTokens
from .orgs import TFCOrgs
from .org_memberships import TFCOrgMemberships
from .org_tokens import TFCOrgTokens
from .plans import TFCPlans
from .plan_exports import TFCPlanExports
from .policies import TFCPolicies
from .policy_checks import TFCPolicyChecks
from .policy_sets import TFCPolicySets
from .policy_set_params import TFCPolicySetParams
from .notification_configs import TFCNotificationConfigurations
from .registry_modules import TFCRegistryModules
from .run_triggers import TFCRunTriggers
from .runs import TFCRuns
from .state_versions import TFCStateVersions
from .state_version_outputs import TFCStateVersionOutputs
from .ssh_keys import TFCSSHKeys
from .teams import TFCTeams
from .team_access import TFCTeamAccess
from .team_memberships import TFCTeamMemberships
from .team_tokens import TFCTeamTokens
from .users import TFCUsers
from .user_tokens import TFCUserTokens
from .vars import TFCVars
from .workspace_vars import TFCWorkspaceVars
from .workspaces import TFCWorkspaces

# Suppress insecure TLS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class InvalidTFCTokenException(Exception):
    """Cannot instantiate TFC API class without a valid TFC_TOKEN."""


class TFC():
    """
    Super class for access to all TFC Endpoints.
    """

    # This dict specifies which class should be used for each attribute of this API class,
    # which simplifies the initialization of each endpoint since they share the same initialization
    # values.
    _class_for_attr_dict = {
        "org-not-required": {
            "admin_orgs": TFCAdminOrgs,
            "admin_runs": TFCAdminRuns,
            "admin_settings": TFCAdminSettings,
            "admin_terraform_versions": TFCAdminTerraformVersions,
            "admin_users": TFCAdminUsers,
            "admin_workspaces": TFCAdminWorkspaces,
            "audit_trails": TFCAuditTrails,
            "ip_ranges": TFCIPRanges,
            "orgs": TFCOrgs
        },
        "org-required": {
            "account": TFCAccount,
            "applies": TFCApplies,
            "agents": TFCAgents,
            "agent_tokens": TFCAgentTokens,
            "config_versions": TFCConfigVersions,
            "cost_estimates": TFCCostEstimates,
            "oauth_clients": TFCOAuthClients,
            "oauth_tokens": TFCOAuthTokens,
            "org_memberships": TFCOrgMemberships,
            "org_tokens": TFCOrgTokens,
            "plans": TFCPlans,
            "plan_exports": TFCPlanExports,
            "policies": TFCPolicies,
            "policy_checks": TFCPolicyChecks,
            "policy_sets": TFCPolicySets,
            "policy_set_params": TFCPolicySetParams,
            "notification_configs": TFCNotificationConfigurations,
            "registry_modules": TFCRegistryModules,
            "run_triggers": TFCRunTriggers,
            "runs": TFCRuns,
            "state_versions": TFCStateVersions,
            "state_version_outputs": TFCStateVersionOutputs,
            "ssh_keys": TFCSSHKeys,
            "teams": TFCTeams,
            "team_access": TFCTeamAccess,
            "team_memberships": TFCTeamMemberships,
            "team_tokens": TFCTeamTokens,
            "users": TFCUsers,
            "user_tokens": TFCUserTokens,
            "vars": TFCVars,
            "workspace_vars": TFCWorkspaceVars,
            "workspaces": TFCWorkspaces
        }
    }

    def __init__(self, api_token, url=TFC_SAAS_URL, verify=True, log_level=LOG_LEVEL):
        if api_token is None:
            raise InvalidTFCTokenException

        self._logger = logging.getLogger(self.__class__.__name__)
        self._log_level = log_level
        self._logger.setLevel(self._log_level)

        self._logger.debug("Initializing the TFC API class...")

        self._instance_url = url
        self._verify = verify
        self._current_org = None

        self.admin_orgs: TFCAdminOrgs = None
        self.admin_runs: TFCAdminRuns = None
        self.admin_settings: TFCAdminSettings = None
        self.admin_terraform_versions: TFCAdminTerraformVersions = None
        self.admin_users: TFCAdminUsers = None
        self.admin_workspaces: TFCAdminWorkspaces = None
        self.audit_trails: TFCAuditTrails = None
        self.ip_ranges: TFCIPRanges = None
        self.orgs: TFCOrgs = None
        self.account: TFCAccount = None
        self.applies: TFCApplies = None
        self.agents: TFCAgents = None
        self.agent_tokens: TFCAgentTokens = None
        self.config_versions: TFCConfigVersions = None
        self.cost_estimates: TFCCostEstimates = None
        self.oauth_clients: TFCOAuthClients = None
        self.oauth_tokens: TFCOAuthTokens = None
        self.org_memberships: TFCOrgMemberships = None
        self.org_tokens: TFCOrgTokens = None
        self.plans: TFCPlans = None
        self.plan_exports: TFCPlanExports = None
        self.policies: TFCPolicies = None
        self.policy_checks: TFCPolicyChecks = None
        self.policy_sets: TFCPolicySets = None
        self.policy_set_params: TFCPolicySetParams = None
        self.notification_configs: TFCNotificationConfigurations = None
        self.registry_modules: TFCRegistryModules = None
        self.run_triggers: TFCRunTriggers = None
        self.runs: TFCRuns = None
        self.state_versions: TFCStateVersions = None
        self.state_version_outputs: TFCStateVersionOutputs = None
        self.ssh_keys: TFCSSHKeys = None
        self.teams: TFCTeams = None
        self.team_access: TFCTeamAccess = None
        self.team_memberships: TFCTeamMemberships = None
        self.team_tokens: TFCTeamTokens = None
        self.users: TFCUsers = None
        self.user_tokens: TFCUserTokens = None
        self.vars: TFCVars = None
        self.workspace_vars: TFCWorkspaceVars = None
        self.workspaces: TFCWorkspaces = None

        self._token = None
        self._headers = None

        self._logger.debug("Retrieving TFC API well known paths..")
        self._well_known_paths = self.well_known_paths()
        self._logger.debug("TFC API well known paths retrieved.")

        self.set_token(api_token)
        self._initialize_endpoints()


    def _get(self, url):
        """
        Simplified HTTP GET function for usage only with this API module.
        """
        results = None
        req = requests.get(url, headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_OK:
            results = json.loads(req.content)
            self._logger.debug(f"GET to {url} successful")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def set_token(self, token):
        """
        Allows for the user to change the token they are using on the fly if
        they need to change tokens.
        """
        self._token = token
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json"
        }
        self._initialize_endpoints()

    def _initialize_endpoints(self):
        self._logger.debug("Initializing endpoints that don't require an org to be set...")
        # Loop through all the endpoints that don't require an org and initialize them
        for ep_name in self._class_for_attr_dict["org-not-required"]:
            class_for_attr = self._class_for_attr_dict["org-not-required"][ep_name]
            initialized_endpoint_class = class_for_attr(
                self._instance_url,
                None,
                self._headers,
                self._well_known_paths,
                self._verify,
                self._log_level)
            setattr(self, ep_name, initialized_endpoint_class)

        self._logger.debug("Initialized endpoints that don't require an org to be set.")
        # Loop through all the endpoints that do require an org and initialize them
        for ep_name in self._class_for_attr_dict["org-required"]:
            setattr(self, ep_name, None)

        self._logger.debug("TFC API class initialized.")

    def well_known_paths(self):
        """
        Retrieve all the well known paths from the Terraform Cloud installation.
        """
        url = f"{self._instance_url}/.well-known/terraform.json"
        return self._get(url)

    def set_org(self, org_name):
        """
        Sets the organization to use for org specific endpoints.
        This method must be called for any non-admin endpoint to work.
        """

        self._logger.debug("Initializing endpoints that do require an org to be set...")

        # Update the current org attribute
        self._current_org = org_name

        for ep_name in self._class_for_attr_dict["org-required"]:
            class_for_attr = self._class_for_attr_dict["org-required"][ep_name]
            initialized_endpoint_class = class_for_attr(
                self._instance_url,
                self._current_org,
                self._headers,
                self._well_known_paths,
                self._verify,
                self._log_level)

            setattr(self, ep_name, initialized_endpoint_class)

        self._logger.debug("Initialized endpoints that do require an org to be set.")
