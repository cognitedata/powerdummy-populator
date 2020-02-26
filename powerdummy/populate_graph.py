from powerdummy.utils.power_assets import *


def populate_assets(client):

    substations = [generate_substation(name=f"Substation {i}") for i in range(10)]

    transformers = [generate_power_transformer(name=f"PowerTransformer {i}") for i in range(5)]
    transformer_ends = [generate_power_transformer_end(name=f"PowerTransformerEnd {i}") for i in range(5)]

    generators = [generate_hydro_generators(name=f"HydroGenerator {i}") for i in range(5)]
    sync_machines = [generate_synchronous_machines(name=f"SyncMachine for HydroGenerator {i}") for i in range(5)]

    lines = [generate_ac_line_segment(name=f"ACLineSegment {i}") for i in range(20)]

    al = client.assets.create(substations + transformers + generators + sync_machines + transformer_ends + lines)
    print(f"created {len(al)} core assets")

    substation_rels = (
        [
            generate_relationship(te.external_id, t.external_id, type="belongsTo")
            for te, t in zip(transformer_ends, transformers)
        ]
        + [
            generate_relationship(t.external_id, s.external_id, type="belongsTo")
            for t, s in zip(transformers, substations[:5])
        ]
        + [
            generate_relationship(g.external_id, s.external_id, type="belongsTo")
            for g, s in zip(generators, substations[5:10])
        ]
        + [
            generate_relationship(sm.external_id, g.external_id, type="belongsTo")
            for sm, g in zip(sync_machines, generators)
        ]
    )
    tr = client.relationships.create(substation_rels)
    print(f"created {len(tr)} relationships for substations")

    term_assets, term_rels = create_terminals(sync_machines + transformer_ends)
    tl1 = client.assets.create(term_assets)
    tr1 = client.relationships.create(term_rels)
    print(
        f"created {len(tl1)} terminal/analog/sensor assets with {len(tr1)} relationships for sync machines/transformer terminals"
    )

    term_assets, term_rels = create_terminals(substations)  # separately to more easily get the terminals to connect
    tl2 = client.assets.create(term_assets)
    tr2 = client.relationships.create(term_rels)
    print(f"created {len(tl2)} terminal/analog/sensor assets with {len(tr2)} relationships for substation terminals")

    analogs = [a for a in tl1 + tl2 if a.metadata["type"] == "Analog"]
    ts = [TimeSeries(external_id=f"{a.external_id}_value") for a in analogs]
    tsc = client.time_series.create(ts)
    print(f"created {len(tsc)} time series on analogs")

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
        "SynchronousMachine",
        "Conform",
        "StaticVarCompensator",
        "ShuntCompensator",
        "PetersonCoil",
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
        rels.append(generate_relationship(t.external_id, asset.external_id, "belongsTo"))  # terminal connectsTo asset

    rels += [
        generate_relationship(a.external_id, a.parent_external_id)
        for a in term_assets
        if a.parent_external_id is not None
    ]  # analog belongsTo terminal
    return term_assets, rels
