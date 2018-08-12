import unittest
from samplitude import samplitude as s8e

class TestReadme(unittest.TestCase):

    def setUp(self):
        self.seed = 1729

    def asserts8e(self, template, expected):
        self.assertEqual(str(expected),
                         str(s8e(template, seed=self.seed)))

    def test_intro(self):
        self.asserts8e("sin(0.31415) | sample(6) | round | cli",
                       """0.0
0.309
0.588
0.809
0.951
1.0""")



    def test_intro_head(self):
        self.asserts8e("sin(0.31415) | head(6) | round | cli",
                       """0.0
0.309
0.588
0.809
0.951
1.0""")


    def test_intro_drop(self):
        self.asserts8e("sin(0.31415) | drop(2) | head(4) | round | cli",
                       """0.588
0.809
0.951
1.0""")


    def test_sin_max(self):
        self.asserts8e("sin(0.31415) | sample(5) | round | max | cli",
                       '0.951')


    def test_poisson_scale(self):
        self.asserts8e("poisson(0.3) | round | shift(15) | sample(5) |cli",
                       """\
33.731
22.204
16.763
17.04
18.668""")


    def test_csv_counter(self):
        self.asserts8e("csv('data/iris.csv', 'virginica') | counter | cli",
                         """\
0 50
1 50
2 50""")

    def test_file_read(self):
        self.asserts8e("file('data/iris.csv') | sample(1) | cli",
                       "150,4,setosa,versicolor,virginica")


    def test_permutations_join(self):
        self.asserts8e("'HT' | permutations | cli",
                       """\
('H', 'T')
('T', 'H')""")
        self.asserts8e("'HT' | permutations | elt_join | cli",
                       """\
H T
T H""")
        self.asserts8e("'HT' | permutations | elt_join(';') | cli",
                        """\
H;T
T;H""")
        self.asserts8e("range(10) | permutations | len",
                       '3628800')



    def test_pure_jinja(self):
        self.asserts8e("range(5) | list",
                       '[0, 1, 2, 3, 4]')

    def test_cli(self):
        self.asserts8e("range(5) | cli",
                       """\
0
1
2
3
4""")

    def test_countsamplecli(self):
        self.asserts8e("count() | sample(5) | cli",
                       """\
0
1
2
3
4""")

    def test_uniform(self):
        self.asserts8e("uniform(0, 5) | sample(5) | cli",
                       """\
4.98186188391
4.42410048265
2.05399187287
2.28859745598
3.33617203154""")

    def test_uniform_round(self):
        self.asserts8e("uniform(0, 5) | round(2) | sample(5) | cli",
                       """\
4.98
4.42
2.05
2.29
3.34""")


    def test_even_choice(self):
        self.asserts8e("range(0, 11, 2) | choice | sample(6) | cli",
                       """\
10
10
4
4
8
2""")


    def test_coinflip(self):
        self.asserts8e("'HT' | choice | sample(6) | cli",
                       """\
T
T
H
H
T
H""")

    def test_count_dice_seed42(self):
        self.seed = 42
        self.asserts8e("range(1,7) | choice | sample(100) | counter | sort | elt_join | cli",
                       """\
1 17
2 21
3 12
4 21
5 13
6 16""")

    def test_count_dice_seed42_sort(self):
        self.seed = 42
        self.asserts8e("range(1,7) | choice | sample(100) |\
                        counter | swap | sort | swap | elt_join | cli",
                       """\
3 12
5 13
6 16
1 17
2 21
4 21""")


    def test_win_draw_loss(self):
        self.asserts8e("['win', 'draw', 'loss'] | choice | sample(6) | sort | cli",
                       """\
draw
draw
loss
loss
loss
win""")


if __name__ == '__main__':
    unittest.main()
