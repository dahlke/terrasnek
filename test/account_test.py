"""
Module for testing the Terraform Cloud API Endpoint: Account.
"""

from .base import TestTFCBaseTestCase


class TestTFCAccount(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Account.
    """

    _unittest_name = "acc"

    def test_account_methods(self):
        """
        Test the Account API endpoints: show, update, change password.
        """

        # Show the account and confirm we get a valid response
        shown_account = self._api.account.show()["data"]
        self.assertTrue("id" in shown_account)
        original_email = shown_account["attributes"]["email"]
        original_username = shown_account["attributes"]["username"]

        email_name = self._name_with_random()
        email_to_update_to = f"{email_name}@gmail.com"
        update_payload = {
            "data": {
                "type": "users",
                "attributes": {
                "email": email_to_update_to,
                "username": original_username
                }
            }
        }
        updated_account = self._api.account.update(update_payload)["data"]
        updated_email = updated_account["attributes"]["email"]
        self.assertEqual(updated_email, email_to_update_to)

        # Set it back to the original email
        update_payload = {
            "data": {
                "type": "users",
                "attributes": {
                "email": original_email,
                "username": original_username
                }
            }
        }
        updated_account = self._api.account.update(update_payload)["data"]
        updated_email = updated_account["attributes"]["email"]
        self.assertEqual(updated_email, original_email)

        # Update the password and confirm the request didn't fail
        password_to_update_to = self._name_with_random()
        change_password_payload = {
            "data": {
                "type": "users",
                "attributes": {
                "current_password": self._test_password,
                "password": password_to_update_to,
                "password_confirmation": password_to_update_to
                }
            }
        }
        changed_account = self._api.account.change_password(change_password_payload)["data"]
        self.assertTrue("id" in changed_account)

        # Change the password back to the initial one to make this easier
        change_password_payload = {
            "data": {
                "type": "users",
                "attributes": {
                "current_password": password_to_update_to,
                "password": self._test_password,
                "password_confirmation": self._test_password
                }
            }
        }
        changed_account = self._api.account.change_password(change_password_payload)["data"]
        self.assertTrue("id" in changed_account)