"""
Create Model connecting a set of Substations to a number of BiddingAreas and connect the
BiddingAreas to a number of GeographicalRegions

Class Substation is also used as Base for all conducting classes
"""
from typing import List, Tuple

import pandas
import numpy

from cognite.client.data_classes import Relationship

from ..multiindex import flatten_multiindex


class Substation:
    """
    Class for connecting Substations to BiddingAreas to GeographicalRegions
    """

    required_assets: Tuple[str] = (
        "Substation",
        "GeographicalRegion",
        "BiddingArea",
    )

    def __init__(self, assets: pandas.DataFrame):
        """
        Set given input assets and make sure assets contains atleast the specified types as defined
        in required_assets.

        Args:
            assets:
                pandas DataFrame with Substation and GeographicalRegion assets defined
        """
        asset_types = assets.index.get_level_values("type").unique()
        isin_mask = numpy.isin(asset_types, self.required_assets, assume_unique=True)

        assert all(isin_mask), f"missing {asset_types[~isin_mask]} assets"

        self.substations = flatten_multiindex(assets.loc["Substation"], "externalId")
        self.bidding_areas = flatten_multiindex(assets.loc["BiddingArea"], "externalId")
        self.geographical_regions = flatten_multiindex(
            assets.loc["GeographicalRegion"], "externalId"
        )

    def connect(self) -> Tuple[pandas.DataFrame, List[Relationship]]:
        """
        Make GeographicalRegion parent of Substation by adding field parentExternalId
        """

    def set_valid_assets(self):
        """
        set the existing assets given by the substations
        """
