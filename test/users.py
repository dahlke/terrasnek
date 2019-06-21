import unittest
import os
from .base import TestTFEBaseTestCase

from tfepy.api import TFE

class TestTFEUsers(TestTFEBaseTestCase):

    def test_destroy_users(self):
        # No test since a new user can't be created with the API. 
        pass

    def test_disable_two_factor_users(self):
        # No test since it can't be re-enabled with the API.
        pass

    def test_list_show_users(self):
        users = self._api.admin_users.ls(query=self._test_username)["data"]
        self.assertNotEqual(len(users), 0)

        # NOTE: The endpoint for the normal Users API does not work.
        # user_id = users[0]['id']
        # user = self._api.users.show(user_id)

    def test_suspend_unsuspend_user(self):
        test_user_id = self._api.admin_users.ls(query=self._test_username)["data"][0]["id"]

        suspended_user = self._api.admin_users.suspend(test_user_id)["data"]
        self.assertTrue(suspended_user["attributes"]["is-suspended"])

        unsuspended_user = self._api.admin_users.unsuspend(test_user_id)["data"]
        self.assertFalse(unsuspended_user["attributes"]["is-suspended"])

    def test_impersonate_unimpersonate_user(self):
        # TODO
        pass

    def test_grant_revoke_admin_user(self):
        test_user_id = self._api.admin_users.ls(query=self._test_username)["data"][0]["id"]

        granted_admin_user = self._api.admin_users.grant_admin(test_user_id)["data"]
        self.assertTrue(granted_admin_user["attributes"]["is-admin"])

        revoked_admin_user = self._api.admin_users.revoke_admin(test_user_id)["data"]
        self.assertFalse(revoked_admin_user["attributes"]["is-admin"])