from powerdummy.utils.power_assets import *


def populate_assets(client):

    substations = [generate_substation(name=f"Substation {i}") for i in range(10)]
    transformers = [generate_substation(name=f"Transformer {i}") for i in range(10)]
    lines = [generate_line(name=f"Line {i}") for i in range(10)]

    al = client.assets.create(substations + transformers + lines)
    print(f"created {len(al)} assets")

    terminal_assets = []
    for a in lines:
        terminal_assets += populate_terminal(a)

    tl = client.assets.create(terminal_assets)
    print(f"created {len(tl)} assets")


def populate_terminal(asset):
    terminal = generate_terminal(f"Terminal-{hash(asset.name)}")
    num_analogs = hash(asset.name) % 3
    analogs = []
    for i in range(num_analogs):
        a = generate_analog(f"Analog-{hash(asset.name*(i+1))}")
        a.parent_external_id = terminal.external_id
        analogs.append(a)
    return analogs + [terminal]
