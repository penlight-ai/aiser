import unittest
from aiser.utils import meets_minimum_version


class CurrentSemanticVersionMeetsMinVersionTestCase(unittest.TestCase):
    def assert_acceptable(self, current_version: str, min_version: str):
        self.assertTrue(meets_minimum_version(current_version, min_version))

    def assert_not_acceptable(self, current_version: str, min_version: str):
        self.assertFalse(meets_minimum_version(current_version, min_version))

    def test_low_major_version_is_not_accepted(self):
        self.assert_not_acceptable(current_version="0.1.0", min_version="1.0.0")

    def test_low_minor_version_is_not_accepted(self):
        self.assert_not_acceptable(current_version="1.0.0", min_version="1.1.0")

    def test_low_patch_version_is_not_accepted(self):
        self.assert_not_acceptable(current_version="1.1.0", min_version="1.1.1")

    def test_high_major_version_is_accepted(self):
        self.assert_acceptable(current_version="2.0.0", min_version="1.0.0")

    def test_high_minor_version_is_accepted(self):
        self.assert_acceptable(current_version="1.2.0", min_version="1.1.0")

    def test_high_patch_version_is_accepted(self):
        self.assert_acceptable(current_version="1.1.2", min_version="1.1.1")

    def test_equal_version_is_accepted(self):
        self.assert_acceptable(current_version="1.1.1", min_version="1.1.1")
