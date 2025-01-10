"""Schlüsselvereinbarung: Diffie-Hellman und Merkles Rätsel."""


def diffie_hellman(prime, generator, first_secret, second_secret):
    """Führt eine Schlüsselvereinbarung nach Diffie und Hellman aus.

    Jede Seite wählt eine Zahl, schickt die Potenz des Erzeugers darüber
    und potenziert das Empfangene mit der eigenen Zahl. Beide landen bei
    derselben Potenz, die nie übertragen wurde.

    Args:
        prime: der Modul.
        generator: der Erzeuger.
        first_secret, second_secret: die geheim gehaltenen Exponenten.

    Returns:
        Abbildung mit beiden Schlüsseln und dem, was auf der Leitung war.

    Raises:
        ValueError: bei einem Modul kleiner als drei.
    """
    if prime < 3:
        raise ValueError("der Modul ist zu klein")
    first_public = pow(generator, first_secret, prime)
    second_public = pow(generator, second_secret, prime)
    return {"first key": pow(second_public, first_secret, prime),
            "second key": pow(first_public, second_secret, prime),
            "on the wire": [prime, generator, first_public, second_public],
            "never sent": "the two secrets and the shared key"}


def hardness():
    """Nennt, worauf die Sicherheit der beiden Verfahren beruht.

    Diffie-Hellman lebt davon, dass aus g^a mod p kein Weg zurück zu a
    bekannt ist. Merkles Rätsel lebt allein davon, dass der Angreifer mehr
    Rätsel lösen muss als die beiden Beteiligten: es steckt kein
    schwieriges Problem dahinter, nur Fleissarbeit.
    """
    return {"diffie hellman": "discrete logarithm",
            "merkle puzzles": "brute force only",
            "difference": "one is believed hard, the other is merely "
                          "laborious"}


def merkle_puzzles(count):
    """Rechnet den Aufwand von Merkles Rätseln aus.

    Eine Seite schickt so viele schwach verschlüsselte Rätsel, wie sie
    erzeugen kann; die andere löst eines davon und nennt dessen Kennung.
    Der Mithörer weiss nicht, welches gelöst wurde, und muss im Mittel die
    Hälfte aller lösen. Der Abstand ist damit quadratisch: er ist gross
    genug, um die Idee zu zeigen, und zu klein für den Einsatz.

    Raises:
        ValueError: bei einer nicht positiven Anzahl.
    """
    if count < 1:
        raise ValueError("die Anzahl muss positiv sein")
    return {"puzzles sent": count, "legitimate work": count,
            "attacker work": count * count, "gap": "quadratic",
            "why it is not used": "doubling the attacker's cost needs four "
                                  "times the legitimate work"}


def man_in_the_middle(signed=False, prime=23, generator=5):
    """Zeigt den Angriff auf die unbeglaubigte Vereinbarung.

    Wer die Leitung beherrscht, führt zwei Vereinbarungen: eine mit jeder
    Seite. Beide glauben, mit der anderen zu sprechen, und beide reden mit
    ihm. Die Rechnung ist in Ordnung, es fehlt die Antwort auf die Frage,
    wessen Potenz da ankommt.

    Args:
        signed: ob die öffentlichen Werte signiert übertragen werden.
        prime, generator: die Parameter.

    Returns:
        Abbildung mit dem Befund.
    """
    first_secret, second_secret, attacker_secret = 6, 15, 9
    if signed:
        return {"succeeded": False,
                "what is missing": None,
                "why": "the public value is signed, so a substituted value "
                       "fails verification",
                "what is still needed": "a way to know the right public key"}
    left = diffie_hellman(prime, generator, first_secret, attacker_secret)
    right = diffie_hellman(prime, generator, attacker_secret, second_secret)
    return {"succeeded": left["first key"] == left["second key"]
            and right["first key"] == right["second key"],
            "what is missing": "authentication",
            "key with the first party": left["first key"],
            "key with the second party": right["second key"],
            "both sides believe": "they share a key with each other"}


def forward_secrecy():
    """Erklärt, was eine kurzlebige Vereinbarung einbringt.

    Werden die Exponenten je Verbindung neu gewählt und danach vergessen,
    so hilft ein später gestohlener Langzeitschlüssel nicht mehr, alte
    Aufzeichnungen zu entschlüsseln: der Sitzungsschlüssel lässt sich aus
    ihm nicht ableiten.
    """
    return {"ephemeral keys": True,
            "past traffic stays safe after a key theft": True,
            "cost": "one exchange per connection",
            "without it": "one stolen key opens every recorded session"}


def parameter_choice():
    """Nennt, worauf bei den Parametern zu achten ist."""
    return {"prime size": "at least 2048 bit for the classic form",
            "small subgroup": "check the received value, or use a group "
                              "without small subgroups",
            "fixed parameters": "shared primes have been precomputed and "
                                "attacked",
            "elliptic curves": "shorter keys at the same strength"}
