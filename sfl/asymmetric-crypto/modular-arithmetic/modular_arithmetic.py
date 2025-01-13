"""Rechnen modulo n: die Grundlage der Verfahren mit öffentlichem Schlüssel."""

import math


def totient(number):
    """Berechnet die Eulersche Funktion durch Abzählen der Teilerfremden.

    Raises:
        ValueError: bei einer nicht positiven Zahl.
    """
    if number < 1:
        raise ValueError("Zahl muss positiv sein")
    return sum(1 for value in range(1, number + 1)
               if math.gcd(value, number) == 1)


def extended_euclid(first, second):
    """Erweiterter euklidischer Algorithmus.

    Returns:
        Tripel (ggT, x, y) mit first·x + second·y = ggT.
    """
    if second == 0:
        return first, 1, 0
    divisor, x, y = extended_euclid(second, first % second)
    return divisor, y, x - (first // second) * y


def inverse(value, modulus):
    """Bestimmt das multiplikative Inverse modulo dem Modul.

    Raises:
        ValueError: wenn Wert und Modul nicht teilerfremd sind.
    """
    divisor, x, _ = extended_euclid(value % modulus, modulus)
    if divisor != 1:
        raise ValueError("kein Inverses, ggT ist %d" % divisor)
    return x % modulus


def power_slow(base, exponent, modulus):
    """Potenziert durch wiederholtes Multiplizieren.

    Der langsame Weg dient als Prüfstein für den schnellen; für grosse
    Exponenten ist er unbrauchbar, weil er so viele Schritte braucht, wie
    der Exponent gross ist.

    Raises:
        ValueError: bei einem negativen Exponenten.
    """
    if exponent < 0:
        raise ValueError("negativer Exponent")
    result = 1
    for _ in range(exponent):
        result = (result * base) % modulus
    return result


def power(base, exponent, modulus):
    """Potenziert durch fortgesetztes Quadrieren.

    Die Zahl der Schritte wächst mit der Zahl der Stellen des Exponenten,
    nicht mit seinem Wert; erst das macht die Verfahren praktisch.

    Raises:
        ValueError: bei einem negativen Exponenten.
    """
    if exponent < 0:
        raise ValueError("negativer Exponent")
    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result


def exponentiation_agrees(trials=40):
    """Vergleicht beide Wege der Potenzierung.

    Returns:
        Wahr, wenn sie für alle geprüften Fälle übereinstimmen.
    """
    for base in range(2, 8):
        for exponent in range(trials):
            for modulus in (7, 11, 77, 91):
                if power(base, exponent, modulus) \
                        != power_slow(base, exponent, modulus):
                    return False
    return True


def identity_holds(number, limit=12):
    """Prüft eine der Identitäten aus Aufgabe 6.1 durch Nachrechnen.

    Die erste Identität sagt, dass die Basis vor dem Potenzieren reduziert
    werden darf; die zweite, dass eine zweite Reduktion nichts ändert.
    Beide gelten ohne weitere Voraussetzung.

    Args:
        number: 1 oder 2.
        limit: Schranke der geprüften Werte.

    Returns:
        Wahr, wenn die Identität für alle geprüften Werte gilt.

    Raises:
        ValueError: bei einer anderen Nummer.
    """
    if number not in (1, 2):
        raise ValueError("nur die ersten beiden Identitaeten")
    for base in range(1, limit):
        for exponent in range(1, limit):
            for modulus in range(2, limit):
                left = pow(base, exponent, modulus)
                if number == 1:
                    right = pow(base % modulus, exponent, modulus)
                else:
                    right = pow(base, exponent, modulus) % modulus
                if left != right:
                    return False
    return True


def identity_three_report(limit=14):
    """Prüft die dritte Identität aus Aufgabe 6.1.

    Sie lautet a^b mod n = a^(b mod φ(n)) mod n für n = pq. Aus dem Satz
    von Euler folgt sie, sobald a und n teilerfremd sind: dann ist
    a^φ(n) ≡ 1, und der Exponent darf modulo φ(n) gerechnet werden. Ohne
    Teilerfremdheit gilt sie nicht, wie das Gegenbeispiel zeigt.

    Returns:
        Abbildung mit beiden Befunden und einem Gegenbeispiel.
    """
    primes = [2, 3, 5, 7, 11, 13]
    coprime_ok = True
    counterexample = None
    for first in primes:
        for second in primes:
            if first == second:
                continue
            modulus = first * second
            phi = (first - 1) * (second - 1)
            for base in range(2, limit):
                for exponent in range(1, limit):
                    left = pow(base, exponent, modulus)
                    right = pow(base, exponent % phi, modulus)
                    if math.gcd(base, modulus) == 1:
                        if left != right:
                            coprime_ok = False
                    elif left != right and counterexample is None:
                        counterexample = {"a": base, "b": exponent,
                                          "n": modulus, "phi": phi,
                                          "left": left, "right": right}
    return {"holds when coprime": coprime_ok,
            "holds in general": counterexample is None,
            "counterexample": counterexample,
            "reason": "Euler needs a and n to be coprime"}


def fermat_little(prime, limit=20):
    """Prüft den kleinen Satz von Fermat für eine Primzahl.

    Für eine Primzahl p und ein dazu teilerfremdes a gilt a^(p−1) ≡ 1.
    """
    for base in range(1, limit):
        if math.gcd(base, prime) != 1:
            continue
        if pow(base, prime - 1, prime) != 1:
            return False
    return True


def why_it_is_hard_to_reverse():
    """Nennt die Probleme, auf denen die Verfahren beruhen."""
    return {"factoring": "given n = pq, find p and q",
            "discrete logarithm": "given g^a mod p, find a",
            "both": "easy in one direction, no known fast way back",
            "warning": "no proof that they are hard, only that nobody has "
                       "published a fast method"}
