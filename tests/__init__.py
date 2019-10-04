from samplitude import samplitude as s8e
import unittest


class SamplitudeTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest', seed=1729):
        super().__init__(methodName)
        self.seed = seed

    def asserts8e(self, template, expected, seed=None):
        if seed is None:
            seed = self.seed

        self.assertEqual(str(expected), str(s8e(template, seed=seed)))
