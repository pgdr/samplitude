import unittest
from tests import SamplitudeTestCase


class TestSamplitudeExpressions(SamplitudeTestCase):

    def test_unknown_keyword(self):
        with self.assertRaises(ValueError):
            self.asserts8e('range(1, 100) | spunge | list', '')

    def test_empty_template(self):
        with self.assertRaises(ValueError):
            self.asserts8e('', '')

    def test_infinite_generator(self):
        with self.assertRaises(ValueError):
            self.asserts8e('poisson(0.3) | round', '')


if __name__ == '__main__':
    unittest.main()
