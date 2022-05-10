"""Das Actor-Modell: die drei Grundoperationen und ihre Zusicherungen."""

PRIMITIVES = {
    "create": "einen neuen Aktor erzeugen und seine Adresse erhalten",
    "send": "eine Nachricht an eine bekannte Adresse schicken",
    "become": "das eigene Verhalten für die nächste Nachricht festlegen",
}


def primitives():
    """Nennt die drei Operationen, aus denen alles besteht."""
    return dict(PRIMITIVES)


def properties():
    """Nennt die Eigenschaften, die einen Aktor ausmachen.

    Ein Aktor hat einen privaten Zustand, den niemand sonst sieht, eine
    Adresse, unter der er erreichbar ist, und einen Posteingang. Er
    bearbeitet immer genau eine Nachricht zur Zeit; daraus folgt, dass
    es innerhalb eines Aktors keine Nebenläufigkeit gibt und deshalb
    auch keine Sperren.
    """
    return {"private state": True, "shared memory": False,
            "one message at a time": True,
            "needs locks": False,
            "address": "die einzige Art, einen Aktor zu erreichen",
            "consequence": "wer eine Adresse nicht kennt, kann den Aktor "
                           "nicht stören"}


def what_a_message_may_carry():
    """Sagt, was in einer Nachricht stehen darf.

    Werte und Adressen. Adressen sind der Punkt: wer eine Adresse
    weitergibt, ändert damit, wer mit wem reden kann. Das ist dieselbe
    Beweglichkeit wie im pi-Kalkül, und deshalb lässt sich das eine im
    anderen ausdrücken.
    """
    return {"values": True, "addresses": True,
            "references to state": False,
            "why not state": "sonst wäre der Zustand geteilt und die "
                             "Grundannahme des Modells hin",
            "same idea as": "der pi-Kalkül, in dem Namen fliessen"}


def guarantees():
    """Trennt, was das Modell zusichert, von dem, was es nicht zusichert.

    Agha sichert zu, dass jede abgeschickte Nachricht irgendwann
    ankommt; das heisst Fairness. Er sichert nicht zu, in welcher
    Reihenfolge zwei Nachrichten ankommen, auch nicht zwischen
    denselben zwei Aktoren. Verbreitete Umsetzungen sind strenger:
    zwischen einem Paar von Aktoren bleibt die Reihenfolge erhalten,
    dafür kann eine Nachricht verlorengehen.

    Wer gegen das Modell programmiert, darf sich auf die Reihenfolge
    nicht verlassen; wer gegen die Umsetzung programmiert, darf es, und
    hat dann Code, der auf einer anderen Umsetzung bricht.
    """
    return {"Agha 1985": {"eventual delivery": True,
                          "order between two actors": False,
                          "loss": False},
            "typical implementation": {"eventual delivery": False,
                                       "order between two actors": True,
                                       "loss": True},
            "advice": "keine Annahme über die Reihenfolge, wenn sie nicht "
                      "erzwungen wird"}


def against_shared_memory():
    """Stellt das Modell dem gemeinsamen Speicher gegenüber.

    Beim gemeinsamen Speicher greifen mehrere Ausführungsfäden auf
    dieselben Daten zu, und die Korrektheit hängt an Sperren. Beim
    Aktormodell gibt es nichts Gemeinsames, und die Korrektheit hängt am
    Protokoll: welche Nachrichten in welcher Reihenfolge zulässig sind.
    Die Schwierigkeit verschwindet nicht, sie wandert.
    """
    return {"shared memory": {"problem": "gleichzeitiger Zugriff",
                              "tool": "Sperren",
                              "failure": "Verklemmung, verlorene "
                                         "Aktualisierung"},
            "actors": {"problem": "das Protokoll",
                       "tool": "Zustandsautomat je Aktor",
                       "failure": "eine Nachricht, mit der der Aktor in "
                                  "diesem Zustand nicht rechnet"},
            "moved, not removed": True}


def why_become_and_not_assignment():
    """Erklärt, warum das Modell von Verhalten statt von Zustand spricht.

    ``become`` legt fest, wie die **nächste** Nachricht bearbeitet wird.
    Der Unterschied zur Zuweisung ist, dass die Änderung erst nach der
    laufenden Nachricht gilt: es gibt keinen Zeitpunkt, an dem ein
    halb geänderter Zustand sichtbar wäre, weil niemand hineinsehen
    kann.
    """
    return {"become": "gilt ab der nächsten Nachricht",
            "assignment": "gilt sofort",
            "why it matters": "der Aktor bearbeitet eine Nachricht ganz "
                              "oder gar nicht",
            "name": "das nennt sich atomar, ohne dass eine Sperre nötig "
                    "wäre"}
