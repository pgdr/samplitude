#!/usr/bin/env python
from __future__ import print_function

__version__ = '0.0.3'

try:
    import matplotlib.pyplot as plt
except ImportError as err:
    print('Warning: matplotlib unavailable, plotting disabled')
    plt = None

import random
import jinja2

from ._samplitude import (sinegenerator, cosinegenerator, tangenerator)

def _generator(func):
    def _inner(*args):
        while True:
            yield (func(*args))

    return _inner

def __listnstrip(gen):
    return list(map(str.strip, gen))

def _stdin_generator():
    import sys
    return __listnstrip(sys.stdin)

def _words_generator():
    import os
    if os.getenv('DICTIONARY') is not None:
        fname = os.getenv('DICTIONARY')
        if os.path.isfile(fname):
            with open(fname, 'r') as fwords:
                return __listnstrip(fwords.readlines())
    files = ('/usr/share/dict/words', '/usr/dict/words')
    for fname in files:
        if os.path.isfile(fname):
            with open(fname, 'r') as fwords:
                return __listnstrip(fwords.readlines())
    import sys
    sys.stderr.write('Warning: words list not found.\n'
                     'Set environment variable DICTIONARY to dict file.\n'
                     'Or simply pipe to samplitude and use `stdin()`.\n')
    return []

def _pairwise(gen):
    _sentinel = object()
    prev = _sentinel
    for elt in gen:
        if prev is _sentinel:
            prev = elt
        else:
            yield prev, elt
            prev = _sentinel
    raise StopIteration


def _rounder(gen, r=3):
    for x in gen:
        yield (round(x, r))


def _inter(gen):
    for x in gen:
        yield (int(x))


def _scale(gen, s=1):
    for x in gen:
        yield x * s


def _shift(gen, s=0):
    for x in gen:
        yield x + s


def _sample(dist, n):
    try:
        return [next(dist) for _ in range(n)]
    except TypeError:
        return dist[:n]


def _gobble(*args, **kwargs):
    return []


def _drop(dist, n):
    try:
        for _ in range(n):
            next(dist)

    except TypeError:
        return dist[n:]

    except StopIteration:
        pass

    return next(dist)

def _counter(dist):
    from collections import Counter
    return Counter(dist)


def _hist(vals, n_bins=None):
    if plt is None:
        return vals
    vals = list(vals)  # consuming generator
    if n_bins is None:
        plt.hist(vals, bins='auto')
    else:
        plt.hist(vals, bins=n_bins)
    plt.show()
    return vals


def _line(vals):
    if plt is None:
        return vals
    vals = list(vals)  # consuming generator
    plt.plot(vals)
    plt.show()
    return vals


def _scatter(vals):
    if plt is None:
        return vals
    x, y = zip(*list(vals))
    plt.scatter(x, y)
    plt.show()
    return vals


def _cli(vals):
    if isinstance(vals, dict):
        return '\n'.join(['{} {}'.format(k, vals[k]) for k in vals])
    return '\n'.join(map(str, vals))


class __samplitude:
    def __init__(self, seed=None):
        if seed is not None:
            self.__random = random.Random(seed)
        else:
            self.__random = random.Random()

        self.jenv = jinja2.Environment()
        self.jenv.globals.update({
            'exponential':
            _generator(self.__random.expovariate),  # one param
            'poisson':
            _generator(self.__random.expovariate),  # alias
            'uniform':
            _generator(self.__random.uniform),
            'gauss':
            _generator(self.__random.gauss),
            'normal':
            _generator(self.__random.normalvariate),
            'lognormal':
            _generator(self.__random.lognormvariate),
            'triangular':
            _generator(self.__random.triangular),
            'beta':
            _generator(self.__random.betavariate),
            'gamma':
            _generator(self.__random.gammavariate),
            'pareto':
            _generator(self.__random.paretovariate),
            'vonmises':
            _generator(self.__random.vonmisesvariate),
            'weibull':
            _generator(self.__random.weibullvariate),
            # THIS ONE'S SPECIAL
            'stdin':
            _stdin_generator,
            # Reads (Unix) dictionary file
            'words':
            _words_generator,
            # custom generators
            'sin':
            sinegenerator,
            'cos':
            cosinegenerator,
            'tan':
            tangenerator,
        })
        self.jenv.filters['choice'] = _generator(self.__random.choice)
        self.jenv.filters['sample'] = _sample
        self.jenv.filters['head'] = _sample  # alias
        self.jenv.filters['drop'] = _drop
        self.jenv.filters['gobble'] = _gobble
        self.jenv.filters['counter'] = _counter
        self.jenv.filters['pairs'] = _pairwise
        self.jenv.filters['shuffle'] = self._shuffle
        self.jenv.filters['round'] = _rounder
        self.jenv.filters['integer'] = _inter
        self.jenv.filters['shift'] = _shift
        self.jenv.filters['scale'] = _scale
        self.jenv.filters['hist'] = _hist
        self.jenv.filters['line'] = _line
        self.jenv.filters['plot'] = _line  # alias
        self.jenv.filters['scatter'] = _scatter
        self.jenv.filters['cli'] = _cli

    def _shuffle(self, dist):
        dist = list(dist)
        self.__random.shuffle(dist)
        return dist


def samplitude(tmpl, seed=None):
    gkw = __samplitude(seed)
    template = gkw.jenv.from_string(tmpl)
    res = template.render()
    if res is None:
        return
    if res.startswith('<generator object'):
        tmpl = tmpl[3:-3].split('|')
        return '"{}"'.format(' | '.join(map(str.strip, tmpl)))
    return res

def _exit_with_usage(argv):
    msg = """\
{0} {1}

Usage:    {0} "cmd" [seed]
Example:  {0} "normal(100, 5) | sample(1000) | cli"
          {0} "normal(100, 5) | sample(1000) | cli" 1349
          {0} "normal(100, 5) | sample(1000) | hist | gobble"
          {0} "['win', 'draw', 'loss'] | choice | sample(6) | sort | cli"
""".format('samplitude', __version__)
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

    res = samplitude(template, seed=seed)
    if res:
        print(res)

if __name__ == '__main__':
    main()
