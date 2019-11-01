import unittest
from tests import SamplitudeTestCase


class TestSamplitudeExpressions(SamplitudeTestCase):

    def test_unknown_keyword(self):
        with self.assertRaises(ValueError):
            self.asserts8e('range(1, 100) | spunge | list', '')

    def test_empty_template(self):
        with self.assertRaises(ValueError):
            self.asserts8e('', '')


if __name__ == '__main__':
    unittest.main()
