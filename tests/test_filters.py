import unittest
from samplitude import samplitude as s8e
from tests import SamplitudeTestCase


class TestSamplitudeFilters(SamplitudeTestCase):

    def test_round(self):
        self.assertEqual('\n'.join(['0.{}'.format(_) for _ in range(7)]),
                         s8e('sin(0.1) | round(1) | sample(7) | cli'))

    def test_scale(self):
        self.assertEqual('\n'.join(map(str, list(range(5, 15)))),
                         s8e('count() | sample(10) | shift(5) | cli'))


if __name__ == '__main__':
    unittest.main()
