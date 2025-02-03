"""Formatzeichenketten: wenn der Text vom Benutzer das Format bestimmt."""

import re

SPECIFIERS = re.compile(r"%[-+ #0-9.]*([diouxXeEfgGcspn%])")


def specifiers(text):
    """Nennt die Formatangaben in einer Zeichenkette."""
    return [match.group(1) for match in SPECIFIERS.finditer(text)
            if match.group(1) != "%"]


def can_write(specifier):
    """Sagt, ob eine Formatangabe schreiben kann.

    Die Angabe ``%n`` schreibt die Zahl der bisher ausgegebenen Zeichen an
    eine Adresse, die als Argument erwartet wird. Sie ist damit die
    einzige, die aus einem Leseproblem ein Schreibproblem macht.
    """
    return specifier.strip("%") == "n" or specifier == "%n"


def render(text, stack, arguments=()):
    """Wertet eine Formatzeichenkette gegen einen Stapel aus.

    Fehlen Argumente, so liest die Ausgabefunktion weiter im Stapel: sie
    weiss nicht, wie viele übergeben wurden.

    Args:
        text: die Formatzeichenkette.
        stack: die Werte, die hinter den Argumenten auf dem Stapel liegen.
        arguments: die tatsächlich übergebenen Argumente.

    Returns:
        Abbildung mit der Zahl der gelesenen Stapelwerte und der Ausgabe.
    """
    found = specifiers(text)
    values = list(arguments)
    read_from_stack = 0
    output = []
    for specifier in found:
        if values:
            output.append(str(values.pop(0)))
        elif read_from_stack < len(stack):
            output.append(str(stack[read_from_stack]))
            read_from_stack += 1
        else:
            output.append("?")
    return {"specifiers": len(found), "read": read_from_stack,
            "printed": " ".join(output) if found else text}


def count_mismatch():
    """Zeigt, dass die Zahl der Argumente nie geprüft wird.

    Returns:
        Abbildung mit der Zahl der Angaben, der Argumente und dem Befund.
    """
    text = "%x %x %x %x"
    report = render(text, stack=[0xdead, 0xbeef, 0xcafe, 0xbabe],
                    arguments=[1])
    return {"specifiers": report["specifiers"], "arguments": 1,
            "reads past the arguments": report["read"] > 0,
            "read from the stack": report["read"]}


def safe_form(user_text):
    """Zeigt die richtige Aufrufform.

    Der Text des Benutzers gehört als Argument übergeben, nicht als
    Format. Dann wird er ausgegeben, statt gedeutet zu werden.

    Returns:
        Abbildung mit dem Befund.
    """
    report = render("%s", stack=[0xdead], arguments=[user_text])
    return {"read": 0, "printed": user_text,
            "call": 'printf("%s", user_text)',
            "the mistake": 'printf(user_text)'}


def what_an_attacker_gains():
    """Nennt, was sich mit einer eigenen Formatzeichenkette erreichen lässt."""
    return {"read the stack": "%x repeatedly, which reveals canaries, "
                              "pointers and the layout",
            "read any address": "%s with an address placed in the buffer",
            "write any address": "%n, which turns the leak into a write",
            "count the output": "the width field controls what %n writes"}


def why_it_still_happens():
    """Erklärt, warum die Klasse nicht ausgestorben ist.

    Der Aufruf sieht harmlos aus und tut das Richtige, solange der Text
    keine Prozentzeichen enthält. Übersetzer warnen inzwischen, aber nur
    dort, wo sie die Zeichenkette zur Übersetzungszeit sehen.
    """
    return {"looks correct": True, "works until the text contains a percent":
            True, "warning exists": "only for literals the compiler sees"}
