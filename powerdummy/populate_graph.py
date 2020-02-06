from powerdummy.utils.power_assets import *


def populate_assets(client):

    substations = [generate_substation(name=f"Substation {i}") for i in range(10)]
    transformers = [generate_substation(name=f"Transformer {i}") for i in range(5)]

    lines = [generate_line(name=f"Line {i}") for i in range(20)]

    al = client.assets.create(substations + transformers + lines)
    print(f"created {len(al)} core assets")

    term_assets, term_rels = create_terminals(lines)

    tl = client.assets.create(term_assets)
    print(f"created {len(tl)} terminal/analog/sensor assets")
    tr = client.relationships.create(term_rels)
    print(f"created {len(tr)} relationships for terminals")


def create_terminals(assets):
    term_assets = []
    rels = []
    has_voltage_types = {
        "AcLineSegment",
        "Sync Machine",
        "Conform",
        "StaticVar",
        "Shunt",
        "Peterson Coil",
        "PowerTransformerEnd",
    }

    for asset in assets:
        t = generate_terminal(f"Terminal-{asset.name}")
        term_assets.append(t)
        num_analogs = dethash(asset.name) % 3
        # is this an asset?
        #        if asset.metadata["type"] in has_voltage_types:
        #            t = generate_voltage_level(f"Voltage-{asset.name}")
        for i in range(num_analogs):
            a = generate_analog(f"Analog-{asset.name}-{i}")
            a.parent_external_id = t.external_id
            term_assets.append(a)
        rels.append(generate_relationship(asset.external_id, t.external_id, "flowsTo"))  # asset connectsTo terminal

    rels += [
        generate_relationship(a.external_id, a.parent_external_id)
        for a in term_assets
        if a.parent_external_id is not None
    ]  # analog belongsTo terminal
    return term_assets, rels
