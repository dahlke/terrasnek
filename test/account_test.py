"""
Module for testing the Terraform Cloud API Endpoint: Account.
"""

from .base import TestTFCBaseTestCase


class TestTFCAccount(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Account.
    """

    _unittest_name = "acc"
    _endpoint_being_tested = "account"

    def test_account(self):
        """
        Test the Account API endpoints.
        """

        # Show the account and confirm we get a valid response
        shown_account = self._api.account.show()["data"]
        self.assertIn("id", shown_account)

        # Store the original username and email for later usage
        original_email = shown_account["attributes"]["email"]
        original_username = shown_account["attributes"]["username"]

        # Generate a new email to change on the account, confirm the update
        email_name = self._unittest_random_name()
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

        # If it's TFC, we don't want to actually change the email, so we will
        # check against the unconfirmed email.
        if not self._api.is_terraform_cloud():
            updated_email = updated_account["attributes"]["email"]
        else:
            updated_email = updated_account["attributes"]["unconfirmed-email"]

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

        # Only fiddle around with the password for the account if it's not TFC,
        # and is a TFE instance used only for testing.
        if not self._api.is_terraform_cloud():
            # Update the password and confirm the request didn't fail
            password_to_update_to = self._unittest_random_name()
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
            self.assertIn("id", changed_account)

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
            self.assertIn("id", changed_account)
