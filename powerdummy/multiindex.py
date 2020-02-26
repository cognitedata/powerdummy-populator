"""
Functions for Concatenating a list of dataframes and use type, externalId and metadata as index
fields and to return a multiindex frame to flat structure
"""
from typing import List, Tuple

import pandas


def concatenate_frames(assets: List[pandas.DataFrame], main_columns: Tuple[str],) -> pandas.DataFrame:
    """
    Concatenate frames with a MultiIndex structure

    Args:
        assets: 
            list of DataFrames with assets
        main_columns:
            columns too use for multiindex (in addition to metadata)

    Returns:
        MultIndex DataFrame
    """

    assets = pandas.concat(
        [frame.melt(main_columns, var_name="metadata", value_name="metavalue") for frame in assets], ignore_index=True,
    )

    assets = assets.set_index(pandas.MultiIndex.from_frame(assets[["type", "externalId", "metadata"]])).sort_index()
    assets = assets[["metavalue"]]

    return assets


def flatten_multiindex(assets: pandas.DataFrame, index_name: str) -> pandas.DataFrame:
    """
    Flatten frame created by concatenate_frames by pivoting the index fields into own columns.
    Non-existing values are left as NaN.

    Args:
        assets:
            MultiIndex DataFrame

    Returns:
        flattended DataFrame
    """

    for name in assets.index.names:
        assets[name] = assets.index.get_level_values(name)

    assets.index = assets.reset_index(drop=True)

    index_frame = assets[[col for col in assets if col not in ["metadata", "metavalue"]]]
    index_frame = index_frame.drop_duplicates(subset=index_name, ignore_index=True)

    assets = pandas.pivot(assets, index=index_name, columns="metadata", values="metavalue")

    assets[index_name] = assets.index.values
    assets = assets.reset_index(drop=True)
    assets = assets.rename_axis("", axis="columns")

    assets = pandas.merge(assets, index_frame, how="left")

    return assets
