#!/usr/bin/env python
from __future__ import print_function

__version__ = '0.0.1'

try:
    import matplotlib.pyplot as plt
except ImportError as err:
    print('Warning: matplotlib unavailable, plotting disabled')
    plt = None

import random
import jinja2


def _generator(func):
    def _inner(*args):
        while True:
            yield (func(*args))

    return _inner

def _stdin_generator():
    import sys
    return list(map(str.strip, sys.stdin))

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
        yield (round(x, r))


def inter(gen):
    for x in gen:
        yield (int(x))


def sample(dist, n):
    try:
        return [next(dist) for _ in range(n)]
    except TypeError:
        return dist[:n]


def counter(dist):
    from collections import Counter
    return Counter(dist)


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
    if isinstance(vals, dict):
        return '\n'.join(['{} {}'.format(k, vals[k]) for k in vals])
    return '\n'.join(map(str, vals))


class __clidist:
    def __init__(self, seed=None):
        if seed is not None:
            self.random = random.Random(seed)
        else:
            self.random = random.Random()

        self.jenv = jinja2.Environment()
        self.jenv.globals.update({
            'exponential':
            _generator(self.random.expovariate),  # one param
            'uniform':
            _generator(self.random.uniform),
            'gauss':
            _generator(self.random.gauss),
            'normal':
            _generator(self.random.normalvariate),
            'lognormal':
            _generator(self.random.lognormvariate),
            'triangular':
            _generator(self.random.triangular),
            'beta':
            _generator(self.random.betavariate),
            'gamma':
            _generator(self.random.gammavariate),
            'pareto':
            _generator(self.random.paretovariate),
            'vonmises':
            _generator(self.random.vonmisesvariate),
            'weibull':
            _generator(self.random.weibullvariate),
            # THIS ONE'S SPECIAL
            'stdin':
            _stdin_generator,
        })
        self.jenv.filters['choice'] = _generator(self.random.choice)
        self.jenv.filters['sample'] = sample
        self.jenv.filters['counter'] = counter
        self.jenv.filters['pairs'] = pairwise
        self.jenv.filters['shuffle'] = self.shuffle
        self.jenv.filters['round'] = rounder
        self.jenv.filters['integer'] = inter
        self.jenv.filters['hist'] = hist
        self.jenv.filters['line'] = line
        self.jenv.filters['scatter'] = scatter
        self.jenv.filters['cli'] = cli

    def shuffle(self, dist):
        dist = list(dist)
        self.random.shuffle(dist)
        return dist


def clidist(tmpl, seed=None):
    gkw = __clidist(seed)
    template = gkw.jenv.from_string(tmpl)
    print(template.render())


def _exit_with_usage(argv):
    msg = """\
{0} {1}

Usage:    {0} "cmd" [seed]
Example:  {0} "normal(100, 5) | sample(1000) | cli"
          {0} "normal(100, 5) | sample(1000) | cli" 1349
          {0} "['win', 'draw', 'loss'] | choice | sample(6) | sort | cli"
""".format(argv[0], __version__)
    exit(msg)


def main():
    from sys import argv
    if not 1 < len(argv) < 4:
        _exit_with_usage(argv)

    template = '{{ %s }}' % argv[1]
    seed = None

    if len(argv) == 3:
        try:
            seed = int(argv[2])
        except Exception:
            _exit_with_usage(argv)

    clidist(template, seed=seed)

if __name__ == '__main__':
    main()
