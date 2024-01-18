"""
"""


import pandas as pd

import logging
from IPython.display import display


def precleaning(df: pd.DataFrame) -> pd.DataFrame:
    """ """

    # columns
    cols = [i.lower() for i in df.columns]
    cols = [i.replace(" ", "_") for i in cols]
    cols = [i.replace("-", "_") for i in cols]
    cols = [i.replace("(", "") for i in cols]
    cols = [i.replace(")", "") for i in cols]
    cols = [i.replace(":", "") for i in cols]
    cols = [i.replace(".", "") for i in cols]

    df.columns = cols

    return df


def preprocess_counrty(
    country_specs,
    nan_threshold=0.22,
    verbose=True,
):
    """ """

    # dropna
    country_specs = _dropna_country(
        country_specs,
        nan_threshold=nan_threshold,
        verbose=verbose,
    )

    # drop cols
    country_specs = _drop_cols(
        country_specs,
        verbose=verbose,
    )

    return country_specs


def _dropna_country(country_specs, nan_threshold=0.22, verbose=True):
    """ """

    # work on nan columns
    drop_cols = ["is_EU27", "is_south_america"]
    country_specs = country_specs.drop(columns=drop_cols)

    # work on nan rows
    tmp = country_specs.isna().mean(axis=1).round(2)

    # apply threshold
    drop_idxs = tmp[tmp > nan_threshold].index

    if verbose:
        display(country_specs.loc[drop_idxs, :])

    # drop rows with huge nan rate
    country_specs = country_specs.drop(index=drop_idxs, columns=drop_cols)

    return country_specs


def _drop_cols(country_specs, verbose=True):
    """ """

    # select num cols
    num_cols = country_specs.select_dtypes(
        include=["float", "int"]
    ).columns.tolist()

    num_cols = [i for i in num_cols if "code" not in i]

    # categ cols
    categ_cols = [
        "alpha_3_code",
        "FAO_country_name",
        "exiobase_region_name",
        "globio_country_code",
        "globio_country_name",
        "USS30_region_name",
    ]

    # apply
    country_specs = country_specs.loc[:, num_cols + categ_cols]

    return country_specs


#     crops = crops.loc[crops.item_name == "Wheat", :]


# crops
