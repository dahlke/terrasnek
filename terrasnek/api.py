"""
Module for container class of all TFC endpoints and high level exceptions around
API access.
"""

import urllib3
import requests
import json
import logging

from._constants import TFC_SAAS_URL, HTTP_OK
from .account import TFCAccount
from .admin_orgs import TFCAdminOrgs
from .admin_runs import TFCAdminRuns
from .admin_settings import TFCAdminSettings
from .admin_terraform_versions import TFCAdminTerraformVersions
from .admin_users import TFCAdminUsers
from .admin_workspaces import TFCAdminWorkspaces
from .applies import TFCApplies
from .config_versions import TFCConfigVersions
from .cost_estimates import TFCCostEstimates
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
from .workspaces import TFCWorkspaces

# Suppress insecure TLS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class InvalidTFCTokenException(Exception):
    """Cannot instantiate TFC API class without a valid TFC_TOKEN."""


class TFC():
    """
    Super class for access to all TFC Endpoints.
    """

    """
    This dict specifies which class should be used for each attribute of this API class,
    which simplifies the initialization of each endpoint since they share the same initialization
    values.
    """
    _class_for_attr_dict = {
        "org-not-required": {
            "admin_orgs": TFCAdminOrgs,
            "admin_runs": TFCAdminRuns,
            "admin_settings": TFCAdminSettings,
            "admin_terraform_versions": TFCAdminTerraformVersions,
            "admin_users": TFCAdminUsers,
            "admin_workspaces": TFCAdminWorkspaces,
            "orgs": TFCOrgs
        },
        "org-required": {
            "account": TFCAccount,
            "applies": TFCApplies,
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
            "workspaces": TFCWorkspaces
        }
    }

    def __init__(self, api_token, url=TFC_SAAS_URL, verify=True):
        # TODO: add logging about initialization and such
        if api_token is None:
            raise InvalidTFCTokenException

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        self._instance_url = url
        self._token = api_token
        self._verify = verify

        self._current_org = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/vnd.api+json"
        }

        self._well_known_paths = self.well_known_paths()

        # Loop through all the endpoints that don't require an org and initialize them
        for ep_name in self._class_for_attr_dict["org-not-required"]:
            class_for_attr = self._class_for_attr_dict["org-not-required"][ep_name]
            initialized_endpoint_class = class_for_attr(
                self._instance_url,
                None,
                self._headers,
                self._verify)
            setattr(self, ep_name, initialized_endpoint_class)

        # Loop through all the endpoints that do require an org and initialize them
        for ep_name in self._class_for_attr_dict["org-required"]:
            setattr(self, ep_name, None)

    # TODO: move this somewhere else?
    def _get(self, url, return_raw=False):
        results = None
        req = requests.get(url, headers=self._headers, verify=self._verify)

        if req.status_code == HTTP_OK and not return_raw:
            results = json.loads(req.content)
            self._logger.debug(f"GET to {url} successful")
        elif req.status_code == HTTP_OK and return_raw:
            results = req.content
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

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

        # Update the current org attribute
        self._current_org = org_name

        for ep_name in self._class_for_attr_dict["org-required"]:
            class_for_attr = self._class_for_attr_dict["org-required"][ep_name]
            initialized_endpoint_class = class_for_attr(
                self._instance_url,
                self._current_org,
                self._headers,
                self._verify)

            setattr(self, ep_name, initialized_endpoint_class)
