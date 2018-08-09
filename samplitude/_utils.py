class _set(frozenset):
    # for nicer repr only
    def __repr__(self):
        content = ', '.join(map(str, sorted(self)))
        return '{%s}' % content

def _generator(func):
    def _inner(*args):
        while True:
            yield (func(*args))

    return _inner
