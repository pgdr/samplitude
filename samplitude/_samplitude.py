import random
import jinja2

from ._utils import _generator

class _Samplitude:
    def __init__(self, seed=None, filters=None):
        self.__random = None
        self.jenv = jinja2.Environment()
        self.set_seed(seed)

    def set_seed(self, seed):
        if seed is None:
            self.__random = random.Random()
        else:
            self.__random = random.Random(seed)

        self.__add_the_ugly_stuff()

    def add_filters(self, filters):
        for fname, f in filters.items():
            self.jenv.filters[fname] = f

    def generator(self, name, func=None):
        if func is not None:
            self.jenv.globals.update({name: func})
            return
        def decorator(func):
            self.jenv.globals.update({name: func})
            return lambda x: x
        return decorator

    def filter(self, name, func=None):
        if func is not None:
            self.jenv.filters[name] = func
            return
        def decorator(func):
            self.jenv.filters[name] = func
            return lambda x: x
        return decorator

    def _shuffle(self, dist):
        dist = list(dist)
        self.__random.shuffle(dist)
        return dist

    def __add_the_ugly_stuff(self):
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
            })
        self.jenv.filters['choice'] = _generator(self.__random.choice)
        self.jenv.filters['shuffle'] = self._shuffle
