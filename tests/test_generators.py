import unittest
from samplitude import samplitude as s8e

class TestSamplitudeGenerators(unittest.TestCase):

    def test_compact_print(self):
        self.assertEqual('"range(8) | shift(2) | sample(3)"',
                         s8e(' range(8)   | shift(2) | sample(3) '))

    def test_range(self):
        pass#self.assertEqual(str(range(

if __name__ == '__main__':
    unittest.main()
