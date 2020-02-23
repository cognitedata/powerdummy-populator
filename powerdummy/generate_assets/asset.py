"""
Functions for creating a number of assets with given name
"""

import pandas
import numpy

from .hashing import deterministic_hash, deterministic_sequence


def get_asset(num: int, name: str, **metadata) -> pandas.DataFrame:
    """
    Generate assets with a name

    Args:
        num:
            number of assets to create
        name:
            the value of field type

    Kwargs:
        metadata:
            key:
                name of field in frame
            value:
                value of field frame

    Returns:
        assets:
            pandas DataFrame with assets
    """
    names = [f"{name}{i}" for i in range(num)]
    external_ids = [deterministic_hash(name) for name in names]

    if metadata:
        assets = pandas.DataFrame(dict({"externalId": external_ids}, **metadata))
    else:
        assets = pandas.DataFrame({"externalId": external_ids})

    assets["name"] = names
    assets["type"] = name
    assets["IdentifiedObject.name"] = names
    assets["IdentifiedObject.aliasName"] = names
    assets["source"] = "powerdummy"

    return assets


def get_conducting_asset(num: int, name: str, **metadata) -> pandas.DataFrame:
    """
    Create assets with a BaseVoltage field added

    Args:
        num:
            number of assets to create
        name:
            the value of field type

    Returns:
        conducting_assets:
            pandas DataFrame with assets
    """
    conducting_assets = get_asset(num=num, name=name, **metadata)

    numpy.random.seed(1223)

    conducting_assets["BaseVoltage_nominalVoltage"] = numpy.random.randint(
        low=22, high=1000, size=len(conducting_assets)
    )

    return conducting_assets


def get_generating_unit_asset(num: int, name: str, **metadata) -> pandas.DataFrame:
    """
    Create assets ending in name GeneratingUnit

    Args:
        num:
            number of assets to create
        name:
            the value of field type

    Returns:
        generating_assets:
            pandas DataFrame with assets
    """
    generating_assets = get_asset(num=num, name=f"{name}GeneratingUnit", **metadata)

    return generating_assets


def get_geographical_regions(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type GeographicalRegion

    Args:
        num:
            number of geographical regions too create

    Returns:
        geographical_regions:
            pandas.DataFrame with assets of type GeographicalRegion
    """

    geographical_regions = get_asset(num=num, name="GeographicalRegion", **metadata)

    return geographical_regions


def get_substations(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type Substation

    Args:
        num:
            number of substations too create

    Returns:
        substations:
            pandas.DataFrame with assets of type Substation
    """
    substations = get_asset(num=num, name="Substation", **metadata)

    random_positions = [deterministic_sequence(f"Substation{i}") for i in range(num)]

    substations["PositionPoint.xPosition"] = [rp % 1000 / 100 for rp in random_positions]
    substations["PositionPoint.yPosition"] = [rp % 1000000 / 100000 for rp in random_positions]

    return substations


def get_ac_line_segments(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type ACLineSegment

    Args:
        num:
            number of ac line segments too create

    Returns:
        ac_line_segments:
            pandas.DataFrame with assets of type ACLineSegment
    """
    return get_conducting_asset(num, "ACLineSegment")


def get_terminals(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type Terminal

    Args:
        num:
            number of terminals too create

    Returns:
        terminals:
            pandas.DataFrame with assets of type Terminal
    """
    terminals = get_asset(num=num, name="Terminal", **metadata)

    return terminals


def get_analogs(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type Analog

    Args:
        num:
            number of analogs too create

    Returns:
        analogs:
            pandas.DataFrame with assets of type Analog
    """
    analogs = get_asset(num=num, name="Analog", **metadata)

    return analogs


def get_bidding_areas(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type BiddingArea

    Args:
        num:
            number of bidding areas too create

    Returns:
        bidding_areas:
            pandas.DataFrame with assets of type BiddingArea
    """

    bidding_areas = get_asset(num=num, name="BiddingArea", **metadata)

    return bidding_areas


def get_power_transformers(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type PowerTransformer

    Args:
        num:
            number of power_transformers too create

    Returns:
        power_transformers:
            pandas.DataFrame with assets of type PowerTransformer
    """
    power_transformers = get_asset(num=num, name="PowerTransformer", **metadata)

    return power_transformers


def get_power_transformers_ends(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type PowerTransformerEnd

    Args:
        num:
            number of power transformers too create

    Returns:
        power_transformers_ends:
            pandas.DataFrame with assets of type PowerTransformerEnd
    """

    power_transformers_ends = get_conducting_asset(num=num, name="PowerTransformerEnd", **metadata)

    return power_transformers_ends


def get_synchronous_machines(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type SynchronousMachine

    Args:
        num:
            number of power transformers too create

    Returns:
        synchronous_machines:
            pandas.DataFrame with assets of type SynchronousMachines
    """

    synchronous_machines = get_asset(num=num, name="SynchronousMachine", **metadata)

    return synchronous_machines


def get_hydro_generating_units(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type HydroGeneratingUnit

    Args:
        num:
            number of power transformers too create

    Returns:
        hydro_generating_units:
            pandas.DataFrame with assets of type HydroGeneratingUnits
    """

    hydro_generating_units = get_generating_unit_asset(num=num, name="Hydro", **metadata)

    return hydro_generating_units


def get_thermal_generating_units(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type ThermalGeneratingUnit

    Args:
        num:
            number of power transformers too create

    Returns:
        thermal_generating_units:
            pandas.DataFrame with assets of type ThermalGeneratingUnits
    """

    thermal_generating_units = get_generating_unit_asset(num=num, name="Thermal", **metadata)

    return thermal_generating_units


def get_wind_generating_units(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type WindGeneratingUnit

    Args:
        num:
            number of power transformers too create

    Returns:
        wind_generating_units:
            pandas.DataFrame with assets of type WindGeneratingUnits
    """

    wind_generating_units = get_generating_unit_asset(num=num, name="Wind", **metadata)

    return wind_generating_units


def get_wave_traps(num: int, **metadata) -> pandas.DataFrame:
    """
    Create num assets with type WaveTrap

    Args:
        num:
            number of power transformers too create

    Returns:
        wave_traps:
            pandas.DataFrame with assets of type WaveTrap
    """

    wave_traps = get_conducting_asset(num=num, name="WaveTrap", **metadata)

    return wave_traps
