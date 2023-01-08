# viper

<a href='https://github.com/aropele/viper'><img src='logo.png' align="right" width="150" /></a>

[![PyPI version](https://badge.fury.io/py/viper-df.svg)](https://pypi.org/project/viper-df/)
[![pages-build](https://github.com/aropele/viper/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/aropele/viper/actions/workflows/pages/pages-build-deployment)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Simple, expressive pipeline syntax to transform and manipulate data with ease 

## Overview

`viper` is a Python package that provides a simple, expressive way to work with data. It allows you to easily manipulate and transform data using a pipeline syntax similar to that of [dplyr](https://dplyr.tidyverse.org/).
 
Pipelining your DataFrame manipulation operations offers several benefits:

- improved code readability (no need to 'comment the what')
- no need to save intermediate dataframes
- ability to chain a long sequence of operations in a single command
- thinking of coding as a series of transformations between the input and the desired output can improve the design and make it less coupled

## Docs
Complete documentation is available [here](reference.md).

## Quick Start

Installation:
``` shell
pip install viper-df
```

Here is an example of how to use `viper` to analyze the famed `mtcars` dataset.

We want to find:

- the average consumption, expressed in Miles/(US) gallon
- the average power

Furthermore:

- only consider those cars that weigh more than 2000lbs
- group the results by the number of cylinders and number of gears
- arrange in descending orders by the grouping variables


``` python
import viper as v
from viper.data import mtcars

v.pipeline(
    mtcars,
    v.rename(
        "hp = power",
        "mpg = consumption",
    ),
    v.mutate(
        consumption=lambda r: 1 / r["consumption"]
    ),
    v.filter(
        lambda r: r["wt"] > 2
    ),
    v.group_by("cyl", "gear"),
    v.summarize(
        "power = mean()",
        "consumption = mean()"
    ),
    v.arrange(
        "cyl desc",
        "gear desc"
    ),
)
#                power  consumption
# cyl gear
# 8   5     299.500000     0.064979
#     3     194.166667     0.068824
# 6   5     175.000000     0.050761
#     4     116.500000     0.050875
#     3     107.500000     0.050989
# 4   5      91.000000     0.038462
#     4      85.000000     0.041259
#     3      97.000000     0.046512
```

[Here](usage.md) you can find more examples, particularly on joins.

## Roadmap

The future development of the package will probably focus on:

- adding `pivot_longer`and `pivot_wider` functions
- adding more `join_*` functions

## Contributions

You are welcome to contribute to the [project](https://github.com/aropele/viper) or open [issues](https://github.com/aropele/viper/issues) if you have any ideas.