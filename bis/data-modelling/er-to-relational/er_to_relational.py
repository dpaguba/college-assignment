"""Die Abbildung eines ER-Modells auf Tabellen."""


def _read_maximum(notation):
    """Liest das Maximum eines (min,max)-Paares.

    Raises:
        ValueError: bei einer fehlerhaften Notation.
    """
    text = str(notation).strip()
    if not (text.startswith("(") and text.endswith(")") and "," in text):
        raise ValueError("keine (min,max)-Notation")
    high = text[1:-1].split(",", 1)[1].strip()
    if high == "n":
        return None
    if not high.isdigit():
        raise ValueError("das Maximum muss eine Zahl oder n sein")
    return int(high)


def example():
    """Studierende besuchen Vorlesungen, n:m.

    Returns:
        Abbildung mit ``entities`` und ``relations``.
    """
    return {
        "entities": {
            "Studierende": {"key": "Matrikelnummer",
                            "attributes": ["Matrikelnummer", "Name"]},
            "Vorlesung": {"key": "Vorlesungsnummer",
                          "attributes": ["Vorlesungsnummer", "Name"]},
        },
        "relations": [
            {"name": "Besuch", "between": ["Studierende", "Vorlesung"],
             "cardinalities": ["(0,n)", "(0,n)"], "attributes": []},
        ],
    }


def one_to_many_example():
    """Ein Betreuer betreut viele Arbeiten, jede Arbeit hat einen.

    Returns:
        Abbildung mit ``entities`` und ``relations``.
    """
    return {
        "entities": {
            "Betreuer": {"key": "Personalnummer",
                         "attributes": ["Personalnummer", "Name"]},
            "Arbeit": {"key": "Arbeitsnummer",
                       "attributes": ["Arbeitsnummer", "Titel"]},
        },
        "relations": [
            {"name": "Betreuung", "between": ["Betreuer", "Arbeit"],
             "cardinalities": ["(0,n)", "(1,1)"], "attributes": []},
        ],
    }


def map_model(model):
    """Bildet ein ER-Modell auf Tabellen ab.

    Die Regeln der Vorlesung: jeder Entitätstyp wird eine Tabelle mit
    seinem Schlüssel. Eine n:m-Relation wird eine eigene Tabelle, deren
    Schlüssel aus beiden Fremdschlüsseln besteht. Eine 1:n-Relation
    braucht keine eigene Tabelle: der Fremdschlüssel wandert auf die
    Seite, die höchstens einmal teilnimmt.

    Args:
        model: Abbildung mit ``entities`` und ``relations``.

    Returns:
        Abbildung vom Tabellennamen auf ``columns`` und ``key``.

    Raises:
        ValueError: bei einer Relation auf einen unbekannten Entitätstyp
            oder einer fehlerhaften Notation.
    """
    tables = {}
    for name, entity in model["entities"].items():
        tables[name] = {"columns": list(entity["attributes"]),
                        "key": [entity["key"]], "from": "entity type"}
    for relation in model["relations"]:
        first, second = relation["between"]
        for name in (first, second):
            if name not in model["entities"]:
                raise ValueError("unbekannter Entitätstyp: %s" % name)
        left = _read_maximum(relation["cardinalities"][0])
        right = _read_maximum(relation["cardinalities"][1])
        many = (left is None or left > 1, right is None or right > 1)
        if all(many):
            key = [model["entities"][first]["key"],
                   model["entities"][second]["key"]]
            tables[relation["name"]] = {
                "columns": key + list(relation.get("attributes", [])),
                "key": key, "from": "n:m relation"}
            continue
        if many[0]:
            holder, referenced = second, first
        else:
            holder, referenced = first, second
        tables[holder]["columns"].append(referenced)
        tables[holder].setdefault("foreign keys", []).append(
            {"column": referenced, "references": referenced})
    return tables


def summary(model):
    """Zählt, was bei der Abbildung entsteht.

    Raises:
        ValueError: bei einem fehlerhaften Modell.
    """
    tables = map_model(model)
    return {"tables": len(tables),
            "from entity types": sum(1 for table in tables.values()
                                     if table["from"] == "entity type"),
            "from relations": sum(1 for table in tables.values()
                                  if table["from"] == "n:m relation"),
            "names": sorted(tables)}


def rules():
    """Nennt die Abbildungsregeln in kurzer Form."""
    return {"entity type": "eine Tabelle, Schlüssel wird Primärschlüssel",
            "n:m": "eine eigene Tabelle mit beiden Fremdschlüsseln",
            "1:n": "Fremdschlüssel auf der n-Seite, keine neue Tabelle",
            "1:1": "Fremdschlüssel auf einer der beiden Seiten",
            "attributes of a relation": "in die Tabelle der Relation, "
                                        "sonst gehen sie verloren"}
