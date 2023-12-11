"""Die Elemente von BPMN 2.0 und die Regel für die beiden Flussarten."""

KINDS = ("event", "task", "gateway", "sequence flow", "message flow",
         "pool", "lane", "data object", "data store")

CROSSES_POOLS = {"sequence flow": False, "message flow": True}


def kinds():
    """Nennt die Elementarten, die in der Vorlesung vorkommen."""
    return list(KINDS)


def crosses_pools(kind):
    """Sagt, ob ein Fluss eine Pool-Grenze überschreiten darf.

    Der Sequenzfluss ordnet die Schritte eines Beteiligten und bleibt
    deshalb in seinem Pool. Zwischen Beteiligten läuft nur der
    Nachrichtenfluss, und der überschreitet die Grenze immer: innerhalb
    eines Pools wäre er sinnlos.

    Raises:
        ValueError: bei einer Art, die kein Fluss ist.
    """
    if kind not in CROSSES_POOLS:
        raise ValueError("keine Flussart")
    return CROSSES_POOLS[kind]


def example():
    """Der Bestellprozess aus der Vorlesung mit drei Beteiligten.

    Returns:
        Abbildung mit ``nodes`` und ``flows``.
    """
    return {
        "nodes": {
            "customer": {"type": "pool"},
            "supplier": {"type": "pool"},
            "receive": {"type": "event", "pool": "supplier",
                        "lane": "Verkauf"},
            "check": {"type": "task", "pool": "supplier",
                      "lane": "Verkauf"},
            "decide": {"type": "gateway", "gateway": "xor",
                       "pool": "supplier", "lane": "Verkauf"},
            "cancel": {"type": "task", "pool": "supplier",
                       "lane": "Verkauf"},
            "confirm": {"type": "task", "pool": "supplier",
                        "lane": "Verkauf"},
            "ship": {"type": "task", "pool": "supplier", "lane": "Lager"},
            "invoice": {"type": "task", "pool": "supplier",
                        "lane": "Verkauf"},
            "done": {"type": "event", "pool": "supplier",
                     "lane": "Verkauf"},
        },
        "flows": [
            {"kind": "message flow", "source": "customer",
             "target": "receive", "label": "PO"},
            {"kind": "sequence flow", "source": "receive",
             "target": "check"},
            {"kind": "sequence flow", "source": "check", "target": "decide"},
            {"kind": "sequence flow", "source": "decide", "target": "cancel",
             "label": "nicht verfügbar"},
            {"kind": "sequence flow", "source": "decide",
             "target": "confirm", "label": "verfügbar"},
            {"kind": "sequence flow", "source": "confirm", "target": "ship"},
            {"kind": "sequence flow", "source": "confirm",
             "target": "invoice"},
            {"kind": "sequence flow", "source": "invoice", "target": "done"},
            {"kind": "message flow", "source": "cancel",
             "target": "customer", "label": "PO Storno"},
            {"kind": "message flow", "source": "invoice",
             "target": "customer", "label": "Rechnung"},
        ],
    }


def pool_of(model, name):
    """Nennt den Pool, in dem ein Knoten liegt.

    Ein Pool liegt in sich selbst; das macht die Prüfung der Flüsse
    einheitlich, ohne den Sonderfall gesondert behandeln zu müssen.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    node = model["nodes"].get(name)
    if node is None:
        raise ValueError("unbekannter Knoten")
    if node["type"] == "pool":
        return name
    return node.get("pool")


def check_flows(model):
    """Prüft jeden Fluss gegen die Regel für Pool-Grenzen.

    Returns:
        Abbildung mit ``errors`` und der Zahl der geprüften Flüsse.
    """
    errors = []
    for flow in model["flows"]:
        kind = flow["kind"]
        if kind not in CROSSES_POOLS:
            errors.append("keine Flussart: %s" % kind)
            continue
        crossing = pool_of(model, flow["source"]) != pool_of(model,
                                                            flow["target"])
        if crossing != CROSSES_POOLS[kind]:
            errors.append("%s von %s nach %s" % (kind, flow["source"],
                                                 flow["target"]))
    return {"errors": errors, "checked": len(model["flows"])}


def lanes(model):
    """Nennt die Bahnen je Pool.

    Returns:
        Abbildung vom Pool auf die Bahnen, alphabetisch.
    """
    found = {}
    for name, node in model["nodes"].items():
        if node["type"] == "pool":
            found.setdefault(name, set())
        elif node.get("lane"):
            found.setdefault(node["pool"], set()).add(node["lane"])
    return {pool: sorted(names) for pool, names in found.items()}


def what_a_pool_means():
    """Erklärt, wofür Pool und Bahn stehen.

    Der Pool ist ein Beteiligter, die Bahn eine Rolle innerhalb davon.
    Zwei Pools tauschen Nachrichten aus und teilen keinen Kontrollfluss;
    zwei Bahnen desselben Pools teilen ihn sehr wohl.
    """
    return {"pool": "ein Beteiligter",
            "lane": "eine Rolle innerhalb eines Beteiligten",
            "between pools": "message flow only",
            "within a pool": "sequence flow"}
