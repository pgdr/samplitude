#!/usr/bin/env python
from __future__ import print_function

try:
    import matplotlib.pyplot as plt
except ImportError as err:
    print('Warning: matplotlib unavailable, plotting disabled')
    plt = None

import jinja2
import random

def _generator(func):
    def _inner(*args):
        while True:
            yield(func(*args))
    return _inner

def pairwise(gen):
    _sentinel = object()
    prev = _sentinel
    for elt in gen:
        if prev is _sentinel:
            prev = elt
        else:
            yield prev, elt
            prev = _sentinel
    raise StopIteration

def rounder(gen, r=3):
    for x in gen:
        yield(round(x, r))

def sample(dist, n):
    try:
        return [next(dist) for _ in range(n)]
    except TypeError:
        return dist[:n]

def hist(vals):
    if plt is None:
        return vals
    plt.hist(vals, bins='auto')
    plt.show()
    return vals

def line(vals):
    if plt is None:
        return vals
    plt.plot(vals)
    plt.show()
    return vals

def scatter(vals):
    if plt is None:
        return vals
    x, y = zip(*vals)
    plt.scatter(x, y)
    plt.show()
    return vals


def cli(vals):
    return '\n'.join(map(str, vals))

class __cliplot:
    def __init__(self, seed=None):
        if seed is not None:
            self.random = random.Random(seed)
        else:
            self.random = random.Random()

        self.jenv = jinja2.Environment()
        self.jenv.globals.update({
            'exponential': _generator(self.random.expovariate),  # one param
            'uniform': _generator(self.random.uniform),
            'gauss': _generator(self.random.gauss),
            'normal': _generator(self.random.normalvariate),
            'lognormal': _generator(self.random.lognormvariate),
            'triangular': _generator(self.random.triangular),
            'beta': _generator(self.random.betavariate),
            'gamma': _generator(self.random.gammavariate),
            'pareto': _generator(self.random.paretovariate),
            'vonmises': _generator(self.random.vonmisesvariate),
            'weibull': _generator(self.random.weibullvariate),
        })
        self.jenv.filters['choice'] = _generator(self.random.choice)
        self.jenv.filters['sample'] = sample
        self.jenv.filters['pairs'] = pairwise
        self.jenv.filters['shuffle'] = self.shuffle
        self.jenv.filters['round'] = rounder
        self.jenv.filters['hist'] = hist
        self.jenv.filters['line'] = line
        self.jenv.filters['scatter'] = scatter
        self.jenv.filters['cli'] = cli


    def shuffle(self, dist):
        dist = list(dist)
        self.random.shuffle(dist)
        return dist


def cliplot(tmpl, seed=None):
    gkw = __cliplot(seed)
    template = gkw.jenv.from_string(tmpl)
    print(template.render())


if __name__ == '__main__':
    from sys import argv
    if not 1 < len(argv) < 4:
        exit('Usage: app arg [seed]')

    template = '{{ %s }}' % argv[1]
    seed = None

    if len(argv) == 3:
        try:
            seed = int(argv[2])
        except Exception:
            exit('Usage: app arg seed(int)')

    cliplot(template, seed=seed)
