"""Das Datenschema der Möbelhauskette aus dem fünften Tutorium."""

ENTITIES = {
    "kunde": {"key": "knr",
              "attributes": ["knr", "name", "vorname", "strasse", "hnr",
                             "plz", "ort", "geb_datum"]},
    "artikel": {"key": "anr",
                "attributes": ["anr", "abez", "preis",
                               "kap_beanspruchung"]},
    "lager": {"key": "lnr", "attributes": ["lnr", "ort", "kapazitaet"]},
    "verkaeufer": {"key": "vnr", "attributes": ["vnr", "name", "vorname"]},
    "kassenbon": {"key": "bon_nr", "attributes": ["bon_nr", "datum"]},
}

RELATIONS = (
    {"name": "liegt_in", "between": ["artikel", "lager"],
     "cardinalities": ["(1,n)", "(0,n)"], "attributes": ["menge"],
     "why": "ein Artikel muss gelagert werden und kann an mehreren Orten "
            "liegen"},
    {"name": "kunde_wirbt_kunde", "between": ["kunde", "kunde"],
     "cardinalities": ["(0,n)", "(0,1)"], "attributes": [],
     "why": "ein Kunde wirbt mehrere, ein Geworbener hat höchstens einen "
            "Werber"},
    {"name": "gehoert_zu", "between": ["kassenbon", "kunde"],
     "cardinalities": ["(1,1)", "(0,n)"], "attributes": [],
     "why": "ein Bon gehört zu genau einem Kunden"},
    {"name": "k_position", "between": ["kassenbon", "artikel"],
     "cardinalities": ["(1,n)", "(0,n)"], "attributes": ["menge"],
     "why": "ein Bon führt mindestens einen Artikel"},
    {"name": "betreut", "between": ["kassenbon", "artikel", "verkaeufer"],
     "cardinalities": ["(1,n)", "(0,n)", "(0,n)"], "attributes": [],
     "why": "die Provision hängt daran, wer welchen Artikel auf welchem "
            "Bon verkauft hat"},
)


def entities():
    """Nennt die Entitätstypen mit ihren Schlüsseln."""
    return {name: dict(row) for name, row in ENTITIES.items()}


def relations():
    """Nennt die Beziehungstypen."""
    return [dict(row) for row in RELATIONS]


def key_of(entity):
    """Nennt den Schlüssel eines Entitätstyps.

    Raises:
        ValueError: bei einem unbekannten Entitätstyp.
    """
    if entity not in ENTITIES:
        raise ValueError("unbekannter Entitätstyp")
    return ENTITIES[entity]["key"]


def recursive_relations():
    """Nennt die Beziehungen eines Typs mit sich selbst.

    Nur eine: «Kunde wirbt Kunde». Sie ist die Stelle, an der die Aufgabe
    aufhört, geradeaus zu sein, weil beide Enden auf dieselbe Tabelle
    zeigen und der Fremdschlüssel deshalb einen anderen Namen braucht als
    der Primärschlüssel.
    """
    return [row["name"] for row in RELATIONS
            if len(set(row["between"])) < len(row["between"])]


def ternary_relations():
    """Nennt die Beziehungen mit mehr als zwei Beteiligten.

    «Betreut» verbindet Bon, Artikel und Verkäufer. Sie liesse sich nicht
    durch drei zweistellige Beziehungen ersetzen: aus «Verkäufer betreut
    Artikel» und «Artikel steht auf Bon» folgt nicht, welcher Verkäufer
    diesen Artikel auf diesem Bon verkauft hat, und genau das braucht die
    Provisionsabrechnung.
    """
    return [row["name"] for row in RELATIONS if len(row["between"]) > 2]


def why_capacity_lives_where_it_does():
    """Erklärt die Aufteilung der Kapazitätsangaben.

    Die Kapazität gehört zum Lager, die Beanspruchung zum Artikel, und
    die Menge zur Beziehung zwischen beiden. Keine der drei Angaben passt
    in eine der anderen Tabellen: die Beanspruchung ist für jeden Artikel
    dieselbe, egal wo er liegt, und die Menge hängt von beiden ab.
    """
    return {"kapazitaet": "lager", "kap_beanspruchung": "artikel",
            "menge": "liegt_in",
            "test": "wovon hängt der Wert ab, davon hängt die Tabelle ab"}
