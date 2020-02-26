"""
Functions for creating assets hierarchy by adding parentExternalId field to assets
"""

import numpy
import pandas

from .generate_assets import create_asset_frame

ASSET_CONFIG = (
    ("Substation", 18, {}),
    ("GeographicalRegion", 1, {}),
    ("BiddingArea", 4, {}),
)


def add_specific_parent(assets: pandas.DataFrame, child_name: str, parent_name: str) -> pandas.DataFrame:
    """
    Add parentExternalId to fields with type child_name pointing to parent_name 

    Args:
        assets:
            pandas DataFrame with assets
        child_name:
            type of asset to add parent too
        parent_name:
            type of asset to point too

    Returns:
        assets:
            pandas DataFrame with parentExternalId added to field of type child_name 

    Examples:
        
        >>> assets = create_asset_frame(("Substation", 2, {}), ("BiddingArea", 1, {}), ("Terminal", 1, {}))
        >>> assets = add_specific_parent(assets, "Substation", "BiddingArea")
        >>> print(
        ...     assets.loc[("Substation", slice(None), slice(None)), "parentExternalId"]
        ... ) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
        type        externalId                            metadata
        Substation  ...-134e-7a6cfa6660df  IdentifiedObject.aliasName ...-9bb2-1b9ac39a740c
                                           IdentifiedObject.name      ...-9bb2-1b9ac39a740c
                                           PositionPoint.xPosition    ...-9bb2-1b9ac39a740c
                                           PositionPoint.yPosition    ...-9bb2-1b9ac39a740c
                                           name                       ...-9bb2-1b9ac39a740c
                                           source                     ...-9bb2-1b9ac39a740c
                    ...-1c21-6648c66afc9b  IdentifiedObject.aliasName ...-9bb2-1b9ac39a740c
                                           IdentifiedObject.name      ...-9bb2-1b9ac39a740c
                                           PositionPoint.xPosition    ...-9bb2-1b9ac39a740c
                                           PositionPoint.yPosition    ...-9bb2-1b9ac39a740c
                                           name                       ...-9bb2-1b9ac39a740c
                                           source                     ...-9bb2-1b9ac39a740c
        Name: parentExternalId, dtype: object

        >>> print(
        ...     assets.loc[
        ...         (["Terminal", "BiddingArea"], slice(None), slice(None)), "parentExternalId"
        ...     ]
        ... ) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
        type         externalId                            metadata
        BiddingArea  00000000-0000-0000-9bb2-1b9ac39a740c  IdentifiedObject.aliasName    NaN
                                                           IdentifiedObject.name         NaN
                                                           name                          NaN
                                                           source                        NaN
        Terminal     00000000-0000-0000-063d-208d78fd732b  IdentifiedObject.aliasName    NaN
                                                           IdentifiedObject.name         NaN
                                                           name                          NaN
                                                           source                        NaN
        Name: parentExternalId, dtype: object
  """

    child_frame = assets.loc[child_name]
    parent_ids = assets.loc[parent_name].index.get_level_values("externalId")

    numpy.random.seed(5469)

    parents = numpy.random.choice(parent_ids, size=len(child_frame.index.get_level_values("externalId").unique()))

    parents = numpy.repeat(parents, child_frame.index.get_level_values("externalId").value_counts())

    assets.loc[(child_name, slice(None), slice(None)), "parentExternalId"] = parents

    return assets


def add_parents() -> pandas.DataFrame:
    """
    Create assets as defined in ASSET_CONFIG and add random parent relations
    """

    assets = create_asset_frame(ASSET_CONFIG)

    add_specific_parent(assets, "BiddingArea", "GeographicalRegion")
    add_specific_parent(assets, "Substation", "BiddingArea")

    return assets
