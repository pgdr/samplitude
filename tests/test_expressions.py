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

    def test_2nd_infinite_generator(self):
        with self.assertRaises(ValueError):
            self.asserts8e("poisson(0.3) | sample(2) | list | choice", '')

    def test_sample_generator_with_len(self):
        with self.assertRaises(ValueError):
            self.asserts8e("poisson(0.3) | sample(2) | choice", '')

    def test_to_json_of_sized_iterator(self):
        #  TODO: Add support for custom JSON Encoder?
        with self.assertRaises(TypeError):
            self.asserts8e('"ABC"| choice | sample(5) | tojson', '')


if __name__ == '__main__':
    unittest.main()
