"""IaaS, PaaS und SaaS: wer welche Schicht betreibt."""

LAYERS = ("Anwendung", "Daten", "Laufzeitumgebung", "Middleware",
          "Betriebssystem", "Virtualisierung", "Server", "Speicher",
          "Netzwerk")

MODELS = {
    "IaaS": 5,
    "PaaS": 2,
    "SaaS": 0,
}


def models():
    """Nennt die drei Dienstmodelle von unten nach oben."""
    return ["IaaS", "PaaS", "SaaS"]


def layers():
    """Nennt die Schichten von oben nach unten."""
    return list(LAYERS)


def managed_by_customer(model):
    """Nennt die Schichten, die beim Kunden bleiben.

    Die drei Modelle unterscheiden sich nur darin, wo der Schnitt liegt.
    Bei IaaS bekommt der Kunde die Maschine und alles darüber ist seine
    Sache; bei PaaS auch noch die Laufzeitumgebung; bei SaaS nichts
    ausser der Benutzung.

    Raises:
        ValueError: bei einem unbekannten Modell.
    """
    if model not in MODELS:
        raise ValueError("unbekanntes Dienstmodell")
    return list(LAYERS[:MODELS[model]])


def split(model):
    """Teilt alle Schichten zwischen Kunde und Anbieter auf.

    Raises:
        ValueError: bei einem unbekannten Modell.
    """
    customer = managed_by_customer(model)
    return {"customer": customer,
            "provider": [name for name in LAYERS if name not in customer],
            "model": model}


def example(model):
    """Nennt ein Beispiel je Modell.

    Raises:
        ValueError: bei einem unbekannten Modell.
    """
    examples = {"IaaS": "Amazon EC2, eine virtuelle Maschine",
                "PaaS": "eine Laufzeitumgebung, in die nur der Code kommt",
                "SaaS": "Salesforce: no hardware, no software"}
    if model not in examples:
        raise ValueError("unbekanntes Dienstmodell")
    return examples[model]


def what_changes_with_the_cut():
    """Sagt, was mit dem Schnitt wandert.

    Nach oben wandern Bequemlichkeit und Abhängigkeit gemeinsam. Bei IaaS
    lässt sich der Anbieter mit Mühe wechseln, weil nur die Maschine
    seine ist; bei SaaS liegen Daten, Prozesse und Oberfläche bei ihm, und
    ein Wechsel ist ein Projekt.
    """
    return {"upwards": ["weniger eigener Betrieb", "mehr Abhängigkeit"],
            "IaaS": "der Wechsel kostet Aufwand",
            "SaaS": "der Wechsel ist ein Projekt",
            "question to ask first": "wo liegen die Daten und wie kommen "
                                     "sie wieder heraus"}
