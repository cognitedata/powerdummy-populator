"""
Function for  creating a DataFrame with a collection of assets

Examples:

    >>> assets = create_asset_frame(("Substation", 2, {}), ("BiddingArea", 1, {}))
    >>> print(assets) # doctest: +NORMALIZE_WHITESPACE
                                                                                    metavalue
    type        externalId                           metadata
    BiddingArea 00000000-0000-0000-9bb2-1b9ac39a740c IdentifiedObject.aliasName  BiddingArea0
                                                     IdentifiedObject.name       BiddingArea0
                                                     name                        BiddingArea0
                                                     source                        powerdummy
    Substation  00000000-0000-0000-134e-7a6cfa6660df IdentifiedObject.aliasName   Substation1
                                                     IdentifiedObject.name        Substation1
                                                     PositionPoint.xPosition             0.63
                                                     PositionPoint.yPosition          1.32063
                                                     name                         Substation1
                                                     source                        powerdummy
                00000000-0000-0000-1c21-6648c66afc9b IdentifiedObject.aliasName   Substation0
                                                     IdentifiedObject.name        Substation0
                                                     PositionPoint.xPosition             5.71
                                                     PositionPoint.yPosition          0.12571
                                                     name                         Substation0
                                                     source                        powerdummy

    >>> assets = create_asset_frame(("Substation", 2, {"kind": "power"}), ("BiddingArea", 1, {}))
    >>> print(assets) # doctest: +NORMALIZE_WHITESPACE
                                                                                    metavalue
    type        externalId                           metadata
    BiddingArea 00000000-0000-0000-9bb2-1b9ac39a740c IdentifiedObject.aliasName  BiddingArea0
                                                     IdentifiedObject.name       BiddingArea0
                                                     name                        BiddingArea0
                                                     source                        powerdummy
    Substation  00000000-0000-0000-134e-7a6cfa6660df IdentifiedObject.aliasName   Substation1
                                                     IdentifiedObject.name        Substation1
                                                     PositionPoint.xPosition             0.63
                                                     PositionPoint.yPosition          1.32063
                                                     kind                               power
                                                     name                         Substation1
                                                     source                        powerdummy
                00000000-0000-0000-1c21-6648c66afc9b IdentifiedObject.aliasName   Substation0
                                                     IdentifiedObject.name        Substation0
                                                     PositionPoint.xPosition             5.71
                                                     PositionPoint.yPosition          0.12571
                                                     kind                               power
                                                     name                         Substation0
                                                     source                        powerdummy
"""
import re
from typing import Dict, Tuple, Union

import pandas

import powerdummy.generate_assets as generate_assets

from ..multiindex import concatenate_frames


def create_asset_frame(*asset_config: Tuple) -> pandas.DataFrame:
    """
    Grab assets defined by config

    Args:
        *asset_config:
            Tuples with three elements:
                first:
                    name of asset
                second:
                    number of assets to create
                third:
                    Dict with additional metadata to add

    Returns:
        assets:
            pandas DataFrame with assets
    """

    camel_to_snake_pattern = re.compile(r"(?<!^)(?=[A-Z])")

    assets = [
        getattr(generate_assets, f"get_{camel_to_snake_pattern.sub('_', name).lower()}s")(num, **metadata,)
        for name, num, metadata in asset_config
    ]

    assets = concatenate_frames(assets, main_columns=["type", "externalId"])

    return assets
