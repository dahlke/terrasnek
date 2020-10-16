"""
Module for testing the Terraform Cloud API Endpoint: Admin Settings.
"""

import random

from .base import TestTFCBaseTestCase


class TestTFCAdminSettings(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Settings.
    """

    _unittest_name = "admin-settings"
    _endpoint_being_tested = "admin_settings"

    def test_admin_settings_general(self):
        """
        Test the Admin Settings General API endpoints.
        """
        # List all the general settings, verify the response type
        all_general = self._api.admin_settings.list_general()["data"]
        self.assertEqual("general-settings", all_general["type"])

        # Update the rate limit to a random number, verify it worked.
        updated_rate_limit = random.randint(45, 60)
        update_payload = {
            "data": {
                "attributes": {
                    "api-rate-limiting-enabled": True,
                    "api-rate-limit": updated_rate_limit
                }
            }
        }
        updated_settings = self._api.admin_settings.update_general(update_payload)["data"]
        self.assertEqual(updated_rate_limit, updated_settings["attributes"]["api-rate-limit"])

    def test_admin_settings_cost_estimation(self):
        """
        Test the Admin Settings Cost Estimation API endpoints.
        """

        # List all the cost estimation settings, verify the response type
        all_cost_est = self._api.admin_settings.list_cost_estimation()["data"]
        self.assertEqual("cost-estimation-settings", all_cost_est["type"])

        # Update the cost estimation settings to enable cost estimation,
        # verify that it's been enabled
        update_payload = {
            "data": {
                "attributes": {
                    "enabled": True,
                    "aws-enabled": True,
                    "aws-access-key-id": "foo",
                    "aws-secret-key": "bar",
                    "azure-enabled": False,
                    "gcp-enabled": False
                }
            }
        }
        updated_cost_est = self._api.admin_settings.update_cost_estimation(update_payload)["data"]
        self.assertTrue(updated_cost_est["attributes"]["enabled"])
        self.assertTrue(updated_cost_est["attributes"]["aws-enabled"])

    def test_admin_settings_saml(self):
        """
        Test the Admin Settings SAML API endpoints.
        """

        # List all the SAML settings, verify the response type
        all_saml = self._api.admin_settings.list_saml()["data"]
        self.assertEqual("saml-settings", all_saml["type"])

        # Update the SAML settings to enable SAML, confirm it's enabled
        update_payload = {
            "data": {
                "attributes": {
                    "enabled": True,
                    "debug": False,
                    "idp-cert": "NEW-CERTIFICATE",
                    "slo-endpoint-url": "https://example.com/slo",
                    "sso-endpoint-url": "https://example.com/sso",
                    "attr-username": "Username",
                    "attr-groups": "MemberOf",
                    "attr-site-admin": "SiteAdmin",
                    "site-admin-role": "site-admins",
                    "sso-api-token-session-timeout": 1209600
                }
            }
        }
        updated_saml = self._api.admin_settings.update_saml(update_payload)["data"]
        self.assertTrue(updated_saml["attributes"]["enabled"])

        # TODO: revoke_previous_saml_idp_cert

        # Disable SAML after running the test so that it's easier to log in with
        # username and password.
        update_payload["data"]["attributes"]["enabled"] = False
        updated_saml = self._api.admin_settings.update_saml(update_payload)["data"]
        self.assertFalse(updated_saml["attributes"]["enabled"])

    def test_admin_settings_smtp(self):
        """
        Test the Admin Settings SMTP API endpoints.
        """

        # List all the SMTP settings, verify the response type
        all_smtp = self._api.admin_settings.list_smtp()["data"]
        self.assertEqual("smtp-settings", all_smtp["type"])

        # TODO: need to use a real SMTP server to finish this test.

    def test_admin_settings_twilio(self):
        """
        Test the Admin Settings Twilio API endpoints.
        """

        # List all the Twilio settings, verify the response type
        all_twilio = self._api.admin_settings.list_twilio()["data"]
        self.assertEqual("twilio-settings", all_twilio["type"])

        # TODO: need to use a real twilio account to finish this test.

    def test_admin_settings_customization(self):
        """
        Test the Admin Settings Customization API endpoints.
        """

        # List all the customization settings, verify the response type
        all_customization = self._api.admin_settings.list_customization()["data"]
        self.assertEqual("customization-settings", all_customization["type"])

        # Update the support email, confirm it works
        email_to_update_to = "foo@bar.com"
        update_payload = {
            "data": {
                "attributes": {
                    "support-email-address": email_to_update_to
                }
            }
        }
        updated_customization = \
            self._api.admin_settings.update_customization(update_payload)["data"]
        self.assertEqual(\
            email_to_update_to, updated_customization["attributes"]["support-email-address"])
