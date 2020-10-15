"""
Module for Terraform Cloud API Endpoint: Admin Settings.
"""

from .endpoint import TFCEndpoint

class TFCAdminSettings(TFCEndpoint):
    """
    `API Docs \
        <https://www.terraform.io/docs/cloud/api/admin/settings.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/admin"

    def required_entitlements(self):
        return []

    def list_general(self):
        """
        ``GET /api/v2/admin/general-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#list-general-settings>`_
        """
        url = f"{self._endpoint_base_url}/general-settings"
        return self._list(url)

    def update_general(self, data):
        """
        ``PATCH /api/v2/admin/general-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#update-general-settings>`_
        """
        url = f"{self._endpoint_base_url}/general-settings"
        return self._patch(url, data=data)

    def list_cost_estimation(self):
        """
        ``GET /api/v2/admin/cost-estimation-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#list-cost-estimation-settings>`_
        """
        url = f"{self._endpoint_base_url}/cost-estimation-settings"
        return self._list(url)

    def update_cost_estimation(self, data):
        """
        ``PATCH /api/v2/admin/cost-estimation-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#update-cost-estimation-settings>`_
        """
        url = f"{self._endpoint_base_url}/cost-estimation-settings"
        return self._patch(url, data)

    def list_saml(self):
        """
        ``GET /api/v2/admin/saml-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#list-saml-settings>`_
        """
        url = f"{self._endpoint_base_url}/saml-settings"
        return self._list(url)

    def update_saml(self, data):
        """
        ``PATCH /api/v2/admin/saml-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#update-saml-settings>`_
        """
        url = f"{self._endpoint_base_url}/saml-settings"
        return self._patch(url, data)

    def revoke_previous_saml_idp_cert(self):
        """
        ``POST /api/v2/admin/saml-settings/actions/revoke-old-certificate``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#revoke-previous-saml-idp-certificate>`_
        """
        url = f"{self._endpoint_base_url}/saml-settings/actions/revoke-old-certificate"
        return self._post(url)

    def list_smtp(self):
        """
        ``GET /api/v2/admin/smtp-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#list-smtp-settings>`_
        """
        url = f"{self._endpoint_base_url}/smtp-settings"
        return self._list(url)

    def update_smtp(self, data):
        """
        ``PATCH /api/v2/admin/smtp-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#update-smtp-settings>`_
        """
        url = f"{self._endpoint_base_url}/smtp-settings"
        return self._patch(url, data)

    def list_twilio(self):
        """
        ``GET /api/v2/admin/twilio-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#list-twilio-settings>`_
        """
        url = f"{self._endpoint_base_url}/twilio-settings"
        return self._list(url)

    def update_twilio(self, data):
        """
        ``PATCH /api/v2/admin/twilio-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#update-twilio-settings>`_
        """
        url = f"{self._endpoint_base_url}/twilio-settings"
        return self._patch(url, data)

    def verify_twilio(self, data):
        """
        ``POST /api/v2/admin/twilio-settings/verify``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#verify-twilio-settings>`_
        """
        url = f"{self._endpoint_base_url}/twilio-settings/verify"
        return self._post(url, data=data)

    def list_customization(self):
        """
        ``GET /api/v2/admin/customization-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#list-customization-settings>`_
        """
        url = f"{self._endpoint_base_url}/customization-settings"
        return self._list(url)

    def update_customization(self, data):
        """
        ``PATCH /api/v2/admin/customization-settings``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/admin/settings.html#update-customization-settings>`_
        """
        url = f"{self._endpoint_base_url}/customization-settings"
        return self._patch(url, data)
