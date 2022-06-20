"""Entity-Relationship-Modellierung und die Abbildung auf Tabellen."""


def course_example():
    """Liefert das Modell der Übung: Kurse, Voraussetzungen, Betreuung.

    Ein Kurs kann beliebig viele Kurse voraussetzen und selbst
    Voraussetzung beliebig vieler Kurse sein, also (0, *) auf beiden
    Seiten. Jeder Kurs wird von mindestens einer Lehrkraft betreut.

    Returns:
        Abbildung von Beziehungsnamen auf ihre Kardinalitäten.
    """
    return {
        "setzt voraus": {"kind": "n:m", "left": (0, "*"), "right": (0, "*"),
                         "entities": ("kurs", "kurs")},
        "betreut": {"kind": "n:m", "course side": (1, "*"),
                    "teacher side": (0, "*"),
                    "entities": ("lehrkraft", "kurs")},
    }


def to_tables(model):
    """Bildet ein Modell auf Relationenschemata ab.

    Eine n:m-Beziehung bekommt eine eigene Tabelle, eine 1:n-Beziehung
    wird zum Fremdschlüssel auf der n-Seite.

    Args:
        model: Abbildung von Beziehungsnamen auf Beschreibungen mit den
            Schlüsseln ``kind``, ``left`` und ``right``.

    Returns:
        Abbildung von Tabellennamen auf ihre Beschreibung.
    """
    tables = {}
    for name, relationship in model.items():
        if relationship["kind"] == "n:m":
            tables[name.replace(" ", "_")] = {
                "references": list(relationship.get("entities", ()))}
        else:
            many_side = relationship["right"]
            one_side = relationship["left"]
            table = tables.setdefault(many_side, {"references": []})
            table["references"].append(one_side)
    return tables


def needs_owner_key(entity_kind):
    """Sagt, ob eine Entität den Schlüssel ihres Besitzers übernehmen muss.

    Raises:
        ValueError: bei einer unbekannten Art.
    """
    if entity_kind not in ("weak", "strong"):
        raise ValueError("unbekannte Entitätsart")
    return entity_kind == "weak"


def cardinality_notations():
    """Stellt die Chen-Notation der (min, max)-Notation gegenüber."""
    return {"chen": "1:n at the side that is functionally determined",
            "min max": "(0,1) and (0,*) written at each edge",
            "same information": True}


def is_a_hierarchy():
    """Beschreibt die drei Abbildungen einer Spezialisierung."""
    return ["one table per class", "one table for the whole hierarchy",
            "one table per leaf"]
