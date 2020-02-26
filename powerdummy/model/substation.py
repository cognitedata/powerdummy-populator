"""
Create Model connecting a set of Substations to a number of BiddingAreas and connect the
BiddingAreas to a number of GeographicalRegions

Class Substation is also used as Base for all conducting classes
"""
from typing import List, Tuple

import numpy
import pandas
from cognite.client.data_classes import Relationship

from ..multiindex import flatten_multiindex


class Substation:
    """
    Class for connecting Substations to BiddingAreas to GeographicalRegions
    """

    pidx: pandas.core.indexing._IndexSlice = pandas.IndexSlice

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

        self.assets = assets

    def connect(self) -> Tuple[pandas.DataFrame, List[Relationship]]:
        """
        Make GeographicalRegion parent of Substation by adding field parentExternalId
        """

    def set_valid_assets(self):
        """
        set the existing assets given by the substations
        """

        bidding_areas = self.assets.xs("BiddingArea", level="type")
        geographical_regions = self.assets.xs("GeographicalRegions", level="type")

        invalid_bidding_areas = (
            bidding_area["parentExternalId"]
            .isin(geographical_regions.index.get_level_values("externalId"))
            .index.get_level_values("externalId")
        )

        self.assets = self.assets.drop(invalid_bidding_areas, level="externalId")
