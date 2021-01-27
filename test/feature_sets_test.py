"""
Module for testing the Terraform Cloud API Endpoint: Feature Sets.
"""

from .base import TestTFCBaseTestCase


class TestTFCFeatureSets(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Feature Sets.
    """

    _unittest_name = "fset"
    _endpoint_being_tested = "feature_sets"

    def test_feature_sets(self):
        """
        Test the Feature Sets API endpoints.
        """
        feature_sets = self._api.feature_sets.list()["data"]
        self.assertEqual("feature-sets", feature_sets[0]["type"])

        feature_sets_for_org = self._api.feature_sets.list_for_org()["data"]
        self.assertEqual("feature-sets", feature_sets_for_org[0]["type"])
