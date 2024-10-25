"""Enterprise-Resource-Planning: ein System, eine Datenbank."""

MODULES = ("Finanzwesen", "Controlling", "Materialwirtschaft",
           "Produktion", "Vertrieb", "Personalwesen", "Instandhaltung",
           "Qualitätsmanagement")


def modules():
    """Nennt die üblichen Module eines ERP-Systems."""
    return list(MODULES)


def why():
    """Nennt das Problem, das ERP löst.

    Grosse Unternehmen haben viele spezifische Anwendungssysteme, und
    jedes hat meist eigene Datenbestände ohne automatischen Austausch.
    Führungskräfte bekommen deshalb kein Gesamtbild, ohne Zahlen von Hand
    zusammenzusuchen. Ein integriertes System hält die Daten einmal.
    """
    return {"problem": "die Systeme haben eigene Datenbestände und "
                       "tauschen nicht automatisch aus",
            "symptom": "Führungskräfte stellen Zahlen von Hand zusammen",
            "one database": True,
            "consequence": "eine Buchung wirkt sofort in allen Modulen"}


def make_or_buy(users, licence, project, own_cost):
    """Vergleicht Standardsoftware mit Eigenentwicklung.

    Die Standardsoftware kostet je Benutzer eine Lizenz und einmal ein
    Einführungsprojekt. Die Eigenentwicklung kostet einen festen Betrag,
    der nicht mit der Zahl der Benutzer wächst. Daraus folgt die Schwelle:
    unterhalb einer bestimmten Benutzerzahl lohnt das eigene System,
    darüber die Lizenz.

    Args:
        users: die Zahl der Benutzer.
        licence: die Lizenzkosten je Benutzer.
        project: die einmaligen Kosten der Einführung.
        own_cost: die Kosten der Eigenentwicklung.

    Returns:
        Abbildung mit beiden Beträgen, der günstigeren Wahl und der
        Schwelle.

    Raises:
        ValueError: bei einem negativen Betrag oder einer negativen
            Benutzerzahl.
    """
    for value in (users, licence, project, own_cost):
        if value < 0:
            raise ValueError("negativer Betrag")
    buy = users * licence + project
    build = own_cost
    threshold = None
    if licence > 0 and own_cost >= project:
        threshold = int((own_cost - project) / licence)
    return {"buy": buy, "build": build,
            "cheaper": "buy" if buy < build else "build",
            "break even users": threshold,
            "note": "die Rechnung lässt den Betrieb aussen vor, und der "
                    "trifft die Eigenentwicklung härter"}


def customising():
    """Trennt das Anpassen vom Programmieren.

    Customising heisst, das Standardsystem über Einstellungen an das
    Unternehmen anzupassen: Kontenpläne, Belegarten, Freigabegrenzen.
    Der Quelltext bleibt unberührt, und deshalb übersteht die Anpassung
    das nächste Update. Wer stattdessen programmiert, zahlt bei jedem
    Update erneut.
    """
    return {"changes the source code": False,
            "changes": "Einstellungen, Stammdaten, Belegarten",
            "survives an update": True,
            "the alternative": "Erweiterung im Quelltext, die bei jedem "
                               "Update nachgezogen werden muss",
            "rule of thumb": "erst den Prozess an die Software anpassen, "
                             "dann die Software an den Prozess"}


def risks():
    """Nennt die Risiken einer ERP-Einführung."""
    return ["das Projekt ist gross und schwer umkehrbar",
            "die Software bringt ihre eigenen Prozesse mit",
            "Anpassungen im Quelltext verteuern jedes Update",
            "die Datenmigration aus den Altsystemen wird unterschätzt",
            "die Beschäftigten müssen anders arbeiten als vorher"]
