"""Vom Datenschema zum Relationenmodell."""

ENTITY_KEYS = {"kunde": "knr", "artikel": "anr", "lager": "lnr",
               "verkaeufer": "vnr", "kassenbon": "bon_nr"}

ENTITY_ATTRIBUTES = {
    "kunde": ["knr", "name", "vorname", "strasse", "hnr", "plz", "ort",
              "geb_datum"],
    "artikel": ["anr", "abez", "preis", "kap_beanspruchung"],
    "lager": ["lnr", "ort", "kapazitaet"],
    "verkaeufer": ["vnr", "name", "vorname"],
    "kassenbon": ["bon_nr", "datum"],
}

RELATIONS = (
    {"name": "liegt_in", "between": ["artikel", "lager"],
     "maxima": ["n", "n"], "attributes": ["menge"]},
    {"name": "kunde_wirbt_kunde", "between": ["kunde", "kunde"],
     "maxima": ["n", "1"], "attributes": [], "roles": ["knr_alt",
                                                       "knr_neu"]},
    {"name": "gehoert_zu", "between": ["kassenbon", "kunde"],
     "maxima": ["1", "n"], "attributes": []},
    {"name": "k_position", "between": ["kassenbon", "artikel"],
     "maxima": ["n", "n"], "attributes": ["menge"]},
    {"name": "betreut", "between": ["kassenbon", "artikel", "verkaeufer"],
     "maxima": ["n", "n", "n"], "attributes": []},
)


def tables():
    """Bildet das Schema auf Relationen ab.

    Die Regeln: jeder Entitätstyp wird eine Relation mit seinem Schlüssel
    als Primärschlüssel. Eine Beziehung mit n auf beiden Seiten wird eine
    eigene Relation, deren Primärschlüssel aus den Fremdschlüsseln
    besteht. Eine Beziehung mit 1 auf einer Seite braucht keine eigene
    Relation: der Fremdschlüssel wandert auf die Seite mit der 1.

    Returns:
        Abbildung vom Relationennamen auf Spalten, Schlüssel und Herkunft.
    """
    built = {}
    for name, key in ENTITY_KEYS.items():
        built[name] = {"key": [key],
                       "columns": list(ENTITY_ATTRIBUTES[name]),
                       "from": "Entitätstyp", "foreign keys": []}
    for relation in RELATIONS:
        many = [maximum == "n" for maximum in relation["maxima"]]
        if all(many):
            keys = []
            for index, entity in enumerate(relation["between"]):
                roles = relation.get("roles")
                keys.append(roles[index] if roles
                            else ENTITY_KEYS[entity])
            built[relation["name"]] = {
                "key": keys,
                "columns": keys + list(relation["attributes"]),
                "from": "n:m-Beziehung",
                "foreign keys": list(zip(keys, relation["between"]))}
            continue
        holder = relation["between"][many.index(False)]
        other = relation["between"][many.index(True)]
        roles = relation.get("roles")
        column = roles[many.index(True)] if roles else ENTITY_KEYS[other]
        built[holder]["columns"].append(column)
        built[holder]["foreign keys"].append((column, other))
    return built


def key_inheritance(name):
    """Nennt, woher der Schlüssel einer Relation kommt.

    Raises:
        ValueError: bei einer unbekannten Relation.
    """
    built = tables()
    if name not in built:
        raise ValueError("unbekannte Relation")
    row = built[name]
    return {"key": row["key"], "from": row["from"],
            "inherited": [column for column, _ in row["foreign keys"]
                          if column in row["key"]]}


def no_repeating_attributes(rows):
    """Prüft die erste Normalform: keine Wiederholung in einer Zelle.

    Der Hinweis der Aufgabe, dass es in den Relationen keine
    Attributwiederholungen gibt, ist die erste Normalform. Ein Kunde mit
    drei Telefonnummern bekommt keine Spalte ``telefon1, telefon2,
    telefon3`` und keine Liste in einer Zelle, sondern eine eigene
    Relation.

    Args:
        rows: die Zeilen als Abbildungen.

    Returns:
        Abbildung mit den Spalten, die eine Liste enthalten.

    Raises:
        ValueError: bei einer leeren Tabelle.
    """
    if not rows:
        raise ValueError("leere Tabelle")
    offenders = sorted({name for row in rows for name, value in row.items()
                        if isinstance(value, (list, tuple, set))})
    return {"first normal form": not offenders, "repeating": offenders}


def where_the_rules_and_the_data_disagree():
    """Nennt zwei Stellen, an denen Regel und Tutorium auseinandergehen.

    Die Abbildungsregeln liefern für «Kunde wirbt Kunde» keinen eigenen
    Relationstyp: die neue Seite hat höchstens einen Werber, also gehört
    der Fremdschlüssel in die Kundentabelle. Das sechste Tutorium legt
    trotzdem eine eigene Tabelle an. Beides ist vertretbar, und die
    eigene Tabelle hat zwei Vorteile: die Kundentabelle bleibt frei von
    einer Spalte, die für die meisten Kunden leer ist, und die Beziehung
    kann später ein Attribut bekommen, etwa das Datum der Werbung.

    Die zweite Stelle ist ``betreut``. Als dreistellige Beziehung bekäme
    sie einen Schlüssel aus allen drei Fremdschlüsseln. In den Daten des
    Tutoriums bestimmt aber schon das Paar aus Bon und Artikel den
    Verkäufer, es gibt keine zwei Zeilen mit demselben Paar. Damit ist
    die Beziehung in Wahrheit zweistellig mit dem Verkäufer als Attribut,
    und der Schlüssel besteht aus zwei Spalten.

    Returns:
        Abbildung mit beiden Stellen und der Entscheidung.
    """
    return {
        "kunde_wirbt_kunde": {
            "by the rules": "Fremdschlüssel knr_alt in kunde",
            "in the tutorial": "eine eigene Tabelle",
            "argument for the table": ["keine überwiegend leere Spalte",
                                       "Platz für spätere Attribute"]},
        "betreut": {
            "by the rules": ["bon_nr", "anr", "vnr"],
            "in the data": ["bon_nr", "anr"],
            "why": "das Paar aus Bon und Artikel bestimmt den Verkäufer "
                   "bereits",
            "consequence": "die Beziehung ist zweistellig mit dem "
                           "Verkäufer als Attribut"},
    }


def the_recursive_case():
    """Erklärt die Beziehung eines Typs mit sich selbst.

    «Kunde wirbt Kunde» hat auf einer Seite höchstens eins, also wandert
    der Fremdschlüssel in die Kundentabelle. Beide Enden zeigen aber auf
    denselben Schlüssel, deshalb braucht der Fremdschlüssel einen eigenen
    Namen: ``knr_alt`` neben ``knr``. Ohne die Umbenennung stünde die
    Spalte zweimal gleich in derselben Relation.
    """
    return {"relation": "kunde_wirbt_kunde",
            "maximum on the new side": "1",
            "consequence": "der Fremdschlüssel steht in kunde",
            "needs a role name": True,
            "columns": ["knr", "knr_alt"],
            "alternative": "eine eigene Relation, wenn die Beziehung "
                           "später Attribute bekommen soll"}
