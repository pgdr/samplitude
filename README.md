# samplitude

CLI generation and plotting of random variables:

```bash
$ samplitude "sin(0.31415) | sample(6) | round | cli"
0.0
0.309
0.588
0.809
0.951
1.0
```

The word _samplitude_ is a portmanteau of _sample_ and _amplitude_.  This
project also started as an étude, hence should be pronounced _sampl-étude_.

`samplitude` is a chain starting with a _generator_, followed by zero or more
_filters_, followed by a consumer.  Most generators are infinite (with the
exception of `range` and `lists` and possibly `stdin`).  Some of the filters can
turn infinite generators into finite generators (like `sample` and `gobble`),
and some filters can turn finite generators into infinite generators, such as
`choice`.

_Consumers_ are any filter that necessarily flush the input; `list`, `cli`,
`tojson`, `unique`, and the plotting tools, `hist`, `scatter` and `line` are
examples of consumers.  The `list` consumer is a Jinja2 built-in, and other
Jinja2 consumers are `sum`, `min`, and `max`:

```bash
samplitude "sin(0.31415) | sample(5) | round | max | cli"
0.951
```

For simplicity, **s8e** is an alias for samplitude.


##  Generators

In addition to the standard `range` function, we support infinite generators

* `exponential(lambd)`: `lambd` is 1.0 divided by the desired mean.
* `uniform(a, b)`: Get a random number in the range `[a, b)` or `[a, b]`
  depending on rounding.
* `gauss(mu, sigma)`: `mu` is the mean, and `sigma` is the standard deviation.
* `normal(mu, sigma)`: as above
* `lognormal(mu, sigma)`: as above
* `triangular(low, high)`: Continuous distribution bounded by given lower and
  upper limits, and having a given mode value in-between.
* `beta(alpha, beta)`: Conditions on the parameters are `alpha > 0` and `beta >
  0`.  Returned values range between 0 and 1.
* `gamma(alpha, beta)`: as above
* `weibull(alpha, beta)`: `alpha` is the scale parameter and `beta` is the shape
  parameter.
* `pareto(alpha)`: Pareto distribution.  `alpha` is the shape parameter.
* `vonmises(mu, kappa)`: `mu` is the mean angle, expressed in radians between 0
  and `2*pi`, and `kappa` is the concentration parameter, which must be greater
  than or equal to zero.  If kappa is equal to zero, this distribution reduces
  to a uniform random angle over the range 0 to `2*pi`.


We have a special infinite generator (filter) that works on finite generators:

* `choice`,

whose behaviour is explained below.

Finally, we have a generator

* `stdin()`

that reads from `stdin`.

## A warning about infinity

All generators are infinite generators, and must be sampled with `sample(n)`
before consuming!

## Usage and installation

Install with
```bash
pip install samplitude
```
or to get bleeding release,
```bash
pip install git+https://github.com/pgdr/samplitude
```


### Examples

This is pure Jinja2:
```bash
>>> samplitude "range(5) | list"
[0, 1, 2, 3, 4]
```

However, to get a more UNIXy output, we use `cli` instead of `list`:

```bash
>>> samplitude "range(5) | cli"
0
1
2
3
4
```

To limit the output, we use `sample(n)`:


```bash
>>> samplitude "range(1000) | sample(5) | cli"
0
1
2
3
4
```

That isn't very helpful on the `range` generator, but is much more helpful on an
infinite generator, such as the `uniform` generator:

```bash
>>> s8e "uniform(0, 5) | sample(5) | cli"
3.3900198868059235
1.2002767137709318
0.40999391897569126
1.9394585953696264
4.37327472704115
```

We can round the output in case we don't need as many digits (note that `round`
is a generator as well and can be placed on either side of `sample`):
```bash
>>> s8e "uniform(0, 5) | round(2) | sample(5) | cli"
4.58
4.33
1.87
2.09
4.8
```



### Selection and modifications

The `samplitude` behavior is equivalent to the `head` program, or from languages
such as Haskell. The `head` alias is supported:
```bash
>>> samplitude "uniform(0, 5) | round(2) | head(5) | cli"
4.58
4.33
1.87
2.09
4.8
```

`drop` is also available:
```bash
>>> s8e "uniform(0, 5) | round(2) | drop(2) | head(3) | cli"
1.87
2.09
4.8
```

To **shift** and **scale** distributions, we can use the `shift(s)` and
`scale(s)` filters.  To get a Poisson point process starting at 15, we can run

```bash
>>> s8e "poisson(0.3) | shift(15)"  # equivalent to exponential(0.3)...
```


### Choices and other operations

Using `choice` with a finite generator gives an infinite generator that chooses
from the provided generator:

```bash
>>> samplitude "range(0, 11, 2) | choice | sample(6) | cli"
8
0
8
10
4
6
```

Jinja2 supports more generic lists, e.g., lists of string.  Hence, we can write

```bash
>>> s8e "['win', 'draw', 'loss'] | choice | sample(6) | sort | cli"
draw
draw
draw
loss
win
win
```

... and as in Python, strings are also iterable:

```bash
>>> s8e "'HT' | cli"
H
T
```
... so we can flip six coins with
```bash
>>> s8e "'HT' | choice | sample(6) | cli"
H
T
T
H
H
H
```

We can flip 100 coins and count the output with `counter` (which is
`collections.Counter`)
```bash
>>> s8e "'HT' | choice | sample(100) | counter | cli"
H 47
T 53
```

The `sort` functionality does not work as expected on a `Counter` object (a
`dict` type), so if we want the output sorted, we pipe through `sort` from
_coreutils_:

```bash
>>> s8e "range(1,7) | choice | sample(100) | counter | cli" | sort -n
1 24
2 17
3 18
4 16
5 14
6 11
```

Using `stdin()` as a generator, we can pipe into `samplitude`.  Beware that
`stdin()` flushes the input, hence `stdin` (currently) does not work with
infinite input streams.

```bash
>>> ls | samplitude "stdin() | choice | sample(1) | cli"
some_file
```


Then, if we ever wanted to shuffle `ls` we can run

```bash
>>> ls | samplitude "stdin() | shuffle | cli"
some_file
```

```bash
>>> cat FILE | samplitude "stdin() | cli"
# NOOP; cats FILE
```



### The fun powder plot

For fun, if you have installed `matplotlib`, we support plotting, `hist` being
the most useful.

```bash
>>> samplitude "normal(100, 5) | sample(1000) | hist"
```

![normal distribution](https://raw.githubusercontent.com/pgdr/samplitude/master/assets/hist_normal.png)

An exponential distribution can be plotted with `exponential(lamba)`.  Note that
the `cli` output must be the last filter in the chain, as that is a command-line
utility only:

```bash
>>> s8e "normal(100, 5) | sample(1000) | hist | cli"
```

![exponential distribution](https://raw.githubusercontent.com/pgdr/samplitude/master/assets/hist_exponential.png)


To **repress output after plotting**, you can use the `gobble` filter to empty
the pipe:

```bash
>>> s8e "normal(100, 5) | sample(1000) | hist | gobble"
```
