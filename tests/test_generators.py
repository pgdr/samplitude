import unittest
from samplitude import samplitude as s8e

class TestSamplitudeGenerators(unittest.TestCase):

    def setUp(self):
        self.seed = 1729

    def asserts8e(self, template, expected):
        self.assertEqual(str(expected),
                         str(s8e(template, seed=self.seed)))


    def test_compact_print(self):
        self.assertEqual('"range(8) | shift(2) | sample(3)"',
                         s8e(' range(8)   | shift(2) | sample(3) '))

    def test_range(self):
        self.asserts8e('range(10) | sum',
                       '45')


    def test_normal(self):
        self.asserts8e('normal(170, 10) | sample(3) | round | cli',
                       """\
167.178
173.51
164.402""")
        self.asserts8e('gauss(170, 10) | sample(3) | round | cli',
                       """\
190.785
169.526
160.629""")

    def test_uniform(self):
        self.asserts8e('uniform(0, 42) | sample(3) | round | cli',
                       """\
41.848
37.162
17.254""")


    def test_exponential(self):
        self.asserts8e('exponential(1/2.71828) | round | sample(3) | cli',
                       """\
15.274
5.875
1.438""")
        self.asserts8e('poisson(1/2.71828) | round | sample(3) | cli',
                       """\
15.274
5.875
1.438""")



    def test_chi2(self):
        self.asserts8e('chi2(5) | sample(3) | round | len',
                       '3')

if __name__ == '__main__':
    unittest.main()
