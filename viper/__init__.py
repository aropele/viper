"""'viper' is a Python package that provides a simple, expressive way to work with data. It allows you to easily manipulate and transform data using a pipeline syntax similar to that of [dplyr](https://dplyr.tidyverse.org/).
 
Pipelining your DataFrame manipulation operations offers several benefits:

- improved code readability (no need to 'comment the what')
- no need to save intermediate dataframes
- ability to chain a long sequence of operations in a single command
- thinking of coding as a series of transformations between the input and the desired output can improve the design and make it less coupled
"""

__all__ = [
    "anti_join",
    "arrange",
    "distinct",
    "filter",
    "group_by",
    "left_join",
    "mutate",
    "mutate_row",
    "pipeline",
    "rename",
    "select",
    "summarize",
    "tail",
    "head",
    "to_csv",
    "squeeze",
]

from viper.functions import (
    anti_join,
    arrange,
    distinct,
    filter,
    group_by,
    left_join,
    mutate,
    mutate_row,
    pipeline,
    rename,
    select,
    summarize,
    tail,
    head,
    to_csv,
    squeeze,
)
