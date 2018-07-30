#!/usr/bin/env python
from __future__ import print_function

__version__ = '0.0.15'
__all__ = ['samplitude']

try:
    import matplotlib.pyplot as plt
except ImportError as err:
    print('Warning: matplotlib unavailable, plotting disabled')
    plt = None

import random
import itertools
import jinja2

from ._samplitude import (sinegenerator, cosinegenerator, tangenerator)

class __set(frozenset):
    # for nicer repr only
    def __repr__(self):
        content = ', '.join(map(str, sorted(self)))
        return '{%s}' % content

def _generator(func):
    def _inner(*args):
        while True:
            yield (func(*args))

    return _inner


def _count(start=0, step=1):
    return itertools.count(start=start, step=step)


def __listnstrip(gen):
    return list(map(str.strip, gen))

def _csv_generator(fname, col=None, sep=None):
    try:
        import pandas as pd
    except ImportError:
        print('Warning: pandas unavailable, csv disabled')
        return []
    if sep is None:
        df = pd.read_csv(fname)
    else:
        df = pd.read_csv(fname, sep=sep)
    if col is None:
        return df[df.columns[0]]
    if isinstance(col, int):
        return df[df.columns[col]]
    return df[col]

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


def _fft(gen):
    import numpy as np
    import scipy.fftpack
    gen = np.array(gen)
    N = len(gen)
    f = scipy.fftpack.fft(gen)
    return list(f[:N//2])

def _dropna(gen):
    for x in gen:
        if x != x:
            continue
        yield x

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
    if isinstance(s, (int, float, complex)):
        for x in gen:
            yield x * s
    else:
        for x, y in zip(gen, s):
            yield x * y


def _shift(gen, s=0):
    if isinstance(s, (int, float, complex)):
        for x in gen:
            yield x + s
    else:
        for x, y in zip(gen, s):
            yield x + y



def _sample(dist, n):
    for x in dist:
        if n <= 0:
            return
        yield x
        n -= 1


def _swap(gen):
    if isinstance(gen, dict):
        for k in sorted(gen.keys()):
            yield (gen[k], k)
        return
    for elt in gen:
        if isinstance(elt, tuple):
            eltp = list(elt)
            eltp.reverse()
            yield tuple(eltp)
        else:
            elt.reverse()
            yield elt

def _elt_join(gen, sep=' '):
    for x in gen:
        yield sep.join(map(str, x))


def _gobble(*args, **kwargs):
    return []


def _len(gen):
    try:
        return len(gen)
    except TypeError:
        return len(list(gen))


def _drop(dist, n):
    try:
        for _ in range(n):
            next(dist)

    except TypeError:
        return dist[n:]

    except StopIteration:
        pass

    return next(dist)


def _sort(gen):
    if isinstance(gen, (int, float, complex)):
        return (gen,)
    if isinstance(gen, dict):
        return ((k, gen[k])
                for k in sorted(gen.keys()))
    gen = list(gen)
    return tuple(sorted(gen))


def _counter(dist):
    from collections import Counter
    return Counter(dist)


def _product(A, B, combiner=None):
    if combiner is None or combiner == 'tuple':
        comb = lambda x,y: tuple((x,y))
    elif combiner in ('add', '+'):
        comb = lambda x,y: x+y
    elif combiner in ('minus', 'sub', '-'):
        comb = lambda x,y: x - y
    elif combiner in ('mul', '*'):
        comb = lambda x,y: x * y
    elif combiner in ('div', '/'):
        comb = lambda x,y: x / y
    elif combiner in ('idiv', '//'):
        comb = lambda x,y: x // y
    elif combiner == 'set':
        comb = lambda x,y: __set((x, y))
    elif combiner.startswith('concat'):
        comb = lambda x,y: '{}{}'.format(x, y)

    return tuple(comb(a,b)
                 for a in A for b in B)


def _permutations(gen, r=None):
    inp = list(gen)
    for perm in itertools.permutations(gen, r=r):
        yield perm


def _combinations(gen, r):
    inp = list(gen)
    for comb in itertools.combinations(gen, r=r):
        yield comb


def _hist(vals, n_bins=None):
    if plt is None:
        return vals
    vals = list(vals)  # consuming generator
    if n_bins is None:
        try:
            plt.hist(vals, bins='auto')
        except:
            plt.hist(vals)
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
    if isinstance(vals, dict):
        vals = vals.items()
    x, y = zip(*list(vals))
    plt.scatter(x, y)
    plt.show()
    return vals


def _cli(vals):
    if isinstance(vals, dict):
        return '\n'.join(['{} {}'.format(k, vals[k]) for k in vals])
    elif isinstance(vals, (int, float, complex)):
        vals = [vals]
    return '\n'.join(map(str, vals))


class __samplitude:
    def __init__(self, seed=None, filters=None):
        if seed is not None:
            self.__random = random.Random(seed)
        else:
            self.__random = random.Random()

        self.jenv = jinja2.Environment()
        self.jenv.globals.update({
            'count':
            _count,  # count from 0 to infinity
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
            # Pandas
            'csv':
            _csv_generator,
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
            'product':
            _product,
        })
        self.jenv.filters['choice'] = _generator(self.__random.choice)
        self.jenv.filters['sample'] = _sample
        self.jenv.filters['head'] = _sample  # alias
        self.jenv.filters['drop'] = _drop
        self.jenv.filters['gobble'] = _gobble
        self.jenv.filters['counter'] = _counter
        self.jenv.filters['pairs'] = _pairwise
        self.jenv.filters['sort'] = _sort
        self.jenv.filters['shuffle'] = self._shuffle
        self.jenv.filters['round'] = _rounder
        self.jenv.filters['integer'] = _inter
        self.jenv.filters['shift'] = _shift
        self.jenv.filters['scale'] = _scale
        self.jenv.filters['fft'] = _fft
        self.jenv.filters['dropna'] = _dropna
        self.jenv.filters['hist'] = _hist
        self.jenv.filters['line'] = _line
        self.jenv.filters['plot'] = _line  # alias
        self.jenv.filters['scatter'] = _scatter
        self.jenv.filters['cli'] = _cli
        self.jenv.filters['len'] = _len
        self.jenv.filters['elt_join'] = _elt_join
        self.jenv.filters['swap'] = _swap
        self.jenv.filters['permutations'] = _permutations
        self.jenv.filters['combinations'] = _combinations
        if filters:
            for fname, f in filters.items():
                self.jenv.filters[fname] = f

    def _shuffle(self, dist):
        dist = list(dist)
        self.__random.shuffle(dist)
        return dist

def __verify_no_jinja_braces(tmpl):
    tmpl = str(tmpl).strip()
    if tmpl.startswith('{{'):
        tmpl = tmpl[2:]
        raise UserWarning('Do not prefix with "{{".')
    if tmpl.endswith('}}'):
        tmpl = tmpl[:-2]
        raise UserWarning('Do not postfix with "}}".')
    return tmpl

def samplitude(tmpl, seed=None, filters=None):
    tmpl = '{{ %s }}' % __verify_no_jinja_braces(tmpl)
    if not tmpl:
        raise ValueError('Empty template')

    gkw = __samplitude(seed=seed, filters=filters)
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

    template = argv[1]
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
