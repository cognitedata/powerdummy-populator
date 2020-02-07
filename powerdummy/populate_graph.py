from powerdummy.utils.power_assets import *


def populate_assets(client):

    substations = [generate_substation(name=f"Substation {i}") for i in range(10)]
    transformers = [generate_substation(name=f"Transformer {i}") for i in range(5)]

    lines = [generate_line(name=f"Line {i}") for i in range(20)]

    al = client.assets.create(substations + transformers + lines)
    print(f"created {len(al)} core assets")

    term_assets, term_rels = create_terminals(substations)
    tl = client.assets.create(term_assets)
    print(f"created {len(tl)} terminal/analog/sensor assets")
    tr = client.relationships.create(term_rels)
    print(f"created {len(tr)} relationships for terminals")

    subst_terminals = [a for a in term_assets if a.metadata["type"] == "Terminal"]
    line_rels = []
    for l in lines:
        from_ss = dethash(l.external_id) % len(subst_terminals)
        to_ss = dethash(l.external_id + "x") % len(subst_terminals)
        if to_ss == from_ss:
            to_ss = (to_ss + 1) % len(subst_terminals)
        rf = generate_relationship(subst_terminals[from_ss].external_id, l.external_id, type="connectsTo")
        rt = generate_relationship(subst_terminals[to_ss].external_id, l.external_id, type="connectsTo")
        line_rels += [rf, rt]
    tr = client.relationships.create(line_rels)
    print(f"created {len(tr)} relationships for lines")


def create_terminals(assets):
    term_assets = []
    rels = []
    has_voltage_types = {
        "ACLineSegment",
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
        rels.append(generate_relationship(t.external_id, asset.external_id, "connectsTo"))  # terminal connectsTo asset

    rels += [
        generate_relationship(a.external_id, a.parent_external_id)
        for a in term_assets
        if a.parent_external_id is not None
    ]  # analog belongsTo terminal
    return term_assets, rels
