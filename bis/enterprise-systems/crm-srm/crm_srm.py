"""Kunden- und Lieferantenbeziehungen um das ERP herum."""

CRM_KINDS = ("operativ", "analytisch", "kollaborativ")

CRM = {
    "operativ": {"does": "unterstützt den täglichen Kontakt: Angebote, "
                         "Aufträge, Beschwerden",
                 "uses": "die Vorgangsdaten des laufenden Geschäfts"},
    "analytisch": {"does": "wertet das Verhalten der Kunden aus: "
                           "Segmentierung, Abwanderung, Wert eines Kunden",
                   "uses": "ein Data Warehouse über alle Kanäle"},
    "kollaborativ": {"does": "führt die Kanäle zusammen, damit der Kunde "
                             "nicht dreimal dasselbe erzählt",
                     "uses": "Telefon, Mail, Web, Filiale in einer Sicht"},
}


def crm_kinds():
    """Nennt die drei Ausprägungen des CRM."""
    return list(CRM_KINDS)


def describe_crm(kind):
    """Beschreibt eine Ausprägung.

    Raises:
        ValueError: bei einer unbekannten Ausprägung.
    """
    if kind not in CRM:
        raise ValueError("unbekannte CRM-Ausprägung")
    return dict(CRM[kind])


def crm():
    """Beschreibt das Customer Relationship Management."""
    return {"direction": "downstream", "partner": "der Kunde",
            "goal": "den Kunden halten, weil ein neuer teurer ist",
            "kinds": list(CRM_KINDS)}


def srm():
    """Beschreibt das Supplier Relationship Management.

    Dieselbe Idee, in die andere Richtung: nicht der Absatz, sondern die
    Beschaffung. Wo CRM den Kunden halten will, will SRM den Lieferanten
    bewerten, die Zahl der Lieferanten steuern und den Einkauf bündeln.
    """
    return {"direction": "upstream", "partner": "der Lieferant",
            "goal": "Bezugsquellen bewerten, bündeln und absichern",
            "typical functions": ["Lieferantenbewertung",
                                  "Ausschreibung und Vergabe",
                                  "Rahmenverträge",
                                  "Katalogbeschaffung"]}


def landscape():
    """Ordnet CRM, ERP und SRM zueinander.

    Das ERP steht in der Mitte und führt die eigenen Vorgänge; SRM sitzt
    davor an der Beschaffungsseite, CRM dahinter an der Absatzseite. Alle
    drei greifen auf dieselben Stammdaten zu, sonst entsteht genau die
    Insel, die das ERP beseitigen sollte.
    """
    return {"centre": "ERP", "upstream": "SRM", "downstream": "CRM",
            "shared": "die Stammdaten",
            "risk": "drei Systeme mit drei Kundenstammdaten"}


def why_keeping_a_customer_is_cheaper():
    """Nennt die Rechnung hinter dem CRM.

    Ein neuer Kunde kostet Werbung, Beratung und Anlaufaufwand; ein
    bestehender kostet den laufenden Kontakt. Deshalb zielt das CRM auf
    die Bindung und nicht nur auf den Abschluss, und deshalb ist die
    Abwanderungsrate die Kennzahl, an der es gemessen wird.
    """
    return {"new customer": "Werbung, Beratung, Anlauf",
            "existing customer": "laufender Kontakt",
            "measure": "die Abwanderungsrate",
            "consequence": "das CRM zielt auf die Bindung, nicht auf den "
                           "einzelnen Abschluss"}
