Here are some additional examples of using `viper` to analyze the `mtcars` dataset.

## Single DataFrame

Find the Mercedes models present in the dataset, convert their weight to tonnes, and sort the results by horsepower:
```python
from viper.main import *
from viper.data import mtcars

df = pipeline(
    mtcars,
    filter(lambda r: "Merc" in r["model"]),
    select("model", "hp", "wt"),
    mutate(wt=lambda r: r["wt"] * 0.45359),
    arrange("hp desc")
)
df
#>           model   hp        wt
#> 11   Merc 450SE  180  1.846111
#> 12   Merc 450SL  180  1.691891
#> 13  Merc 450SLC  180  1.714570
#> 9      Merc 280  123  1.560350
#> 10    Merc 280C  123  1.560350
#> 8      Merc 230   95  1.428808
#> 7     Merc 240D   62  1.446952
```

Determine the frequency table of car manufacturers that have at least two models in the dataset:
```python
df = pipeline(
    mtcars,
    mutate(
        producer=lambda r: r["model"].split(' ')[0]
    ),
    group_by("producer"),
    summarize("producer = size()"),
    filter(lambda r: r["producer"] >= 2)
)
df
#>           producer
#> producer
#> Fiat             2
#> Hornet           2
#> Mazda            2
#> Merc             7
#> Toyota           2
```

## Two DataFrames

To demonstrate the use of the `left_join` function, we will calculate the z-scores of the horsepower variable with respect to the population grouped by the number of cylinders, using only `viper`:
```python
df_metrics = pipeline(
    mtcars,
    mutate(
        hp_mean=lambda r: r["hp"],
        hp_std=lambda r: r["hp"]
    ),
    group_by("cyl"),
    summarize(
        "hp_mean = mean()",
        "hp_std = std()"
    )
)
df_metrics
#>         hp_mean     hp_std
#> cyl
#> 4     82.636364  20.934530
#> 6    122.285714  24.260491
#> 8    209.214286  50.976886

df_zscores = pipeline(
    mtcars,
    select("model", "cyl", "hp"),
    left_join(
        df_metrics,
        by = "cyl"
    ),
    mutate(
        zscore = lambda r: (r["hp"] - r["hp_mean"]) / r["hp_std"]
    )
)
df_zscores.head()
#>                model  cyl   hp     hp_mean     hp_std    zscore
#> 0          Mazda RX4    6  110  122.285714  24.260491 -0.506408
#> 1      Mazda RX4 Wag    6  110  122.285714  24.260491 -0.506408
#> 2         Datsun 710    4   93   82.636364  20.934530  0.495050
#> 3     Hornet 4 Drive    6  110  122.285714  24.260491 -0.506408
#> 4  Hornet Sportabout    8  175  209.214286  50.976886 -0.671173
```

The `anti_join` function is a type of filtering join that can be used to remove from the current dataset any rows that match a row in another dataset.
In this example, it will be used to remove models from the dataset that are made by producers that are present in df_filter:
```python
df = pipeline(
    mtcars,
    mutate(producer=lambda r: r["model"].split(' ')[0])
)

df_filter = pipeline(
    df,
    select("producer"),
    filter(lambda r: r["producer"] in ["Merc", "Ferrari", "Toyota"]),
    distinct("producer")
)
df_filter
#>    producer
#> 7      Merc
#> 19   Toyota
#> 29  Ferrari

df_filtered = pipeline(
    df,
    anti_join(
        df_filter,
        by = "producer"
    ),
    distinct("producer"),
    arrange("producer")
)
df_filtered
#>     producer
#> 22       AMC
#> 14  Cadillac
#> 23    Camaro
#> 16  Chrysler
#> 2     Datsun
#> 21     Dodge
#> 6     Duster
#> 17      Fiat
#> 28      Ford
#> 18     Honda
#> 3     Hornet
#> 15   Lincoln
#> 27     Lotus
#> 30  Maserati
#> 0      Mazda
#> 24   Pontiac
#> 26   Porsche
#> 5    Valiant
#> 31     Volvo
```