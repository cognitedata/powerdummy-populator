import copy
import hashlib
import uuid

from cognite.client.data_classes import *


def dethash(str):
    return int(hashlib.md5(str.encode("utf-8")).hexdigest()[:16], 16)


def generate_power_asset(name, type, metadata={}):
    h = dethash(name)
    lx = h % 1000 / 100
    ly = h * h % 1000000 / 100000
    eid = str(uuid.UUID(int=h * h))
    return Asset(
        external_id=eid,
        name=name,
        metadata={
            "Location X": lx,
            "Location Y": ly,
            "type": type,
            **metadata,
            "usecase": "grid",
            "name": name,
            "IdentifiedObject.aliasName": name,
        },
        source="GraphDB",
    )


def generate_substation(name):
    return generate_power_asset(name, "Substation")


def generate_terminal(name):
    return generate_power_asset(name, "Terminal")


def generate_transformer(name):
    return generate_power_asset(name, "Substation", {"Substation.kind": "SubstationKind.transformer"})


def generate_line(name):
    metadata = {"Source type": "ACLineSegment", "Equipment.gridType": "GridTypeKind.regional"}
    return generate_power_asset(name, "Line", metadata)


def generate_breaker(name):
    metadata = {"Equipment.gridType": "GridTypeKind.production"}
    return generate_power_asset(name, "Breaker", metadata)


def generate_analog(name):
    metadata = {
        "Measurement.measurementType": "ThreePhaseReactivePower",
        "Measurement.unitMultiplier": "UnitMultiplier.M",
        "Measurement.unitSymbol": "UnitSymbol.VAr",
        "Analog.positiveFlowIn": "true (boolean)",
        "hotspot": "False",
    }
    return generate_power_asset(name, "Analog", metadata)


def generate_hydro_plant(name):
    metadata = {
        "Equipment.gridType": "GridTypeKind.production",
        "GeneratingUnit.genControlSource": "GeneratorControlSource.plantControl",
        "GeneratingUnit.startupTime": "123.0 (Seconds)",
        "HydroGeneratingUnit.turbineType": "HydroTurbineKind.pelton",
    }
    return generate_power_asset(name, "HydroGeneratingUnit", metadata)


def generate_relationship(from_asset, to_asset, type="belongsTo"):
    return Relationship(
        external_id=f"{type}:{from_asset}->{to_asset}",
        source={"resourceId": from_asset, "resource": "Asset"},
        target={"resourceId": to_asset, "resource": "Asset"},
        relationship_type=type,
        confidence=1.0,
        data_set="powerdummy",
    )
