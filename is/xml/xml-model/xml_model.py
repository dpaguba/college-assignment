"""XML als geordneter Baum, im Gegensatz zur ungeordneten Relation."""

import xml.etree.ElementTree as elements


def parse(text):
    """Liest ein Dokument und gibt seine Wurzel zurück.

    Raises:
        xml.etree.ElementTree.ParseError: wenn der Text nicht wohlgeformt ist.
    """
    return elements.fromstring(text)


def name(node):
    """Gibt den Elementnamen eines Knotens zurück."""
    return node.tag


def children(node):
    """Gibt die Kindelemente in Dokumentreihenfolge zurück."""
    return list(node)


def child_names(node):
    """Gibt die Namen der Kindelemente in Dokumentreihenfolge zurück."""
    return [child.tag for child in node]


def attributes(node):
    """Gibt die Attribute eines Knotens als Abbildung zurück."""
    return dict(node.attrib)


def is_irregular(node):
    """Sagt, ob gleichnamige Geschwister verschiedene Strukturen haben.

    Geprüft werden Attributnamen und Kindnamen: unterscheiden sie sich
    zwischen zwei Elementen desselben Namens, ist das Dokument
    unregelmässig.
    """
    shapes = {}
    for child in node:
        shape = (tuple(sorted(child.attrib)), tuple(child_names(child)))
        if child.tag in shapes and shapes[child.tag] != shape:
            return True
        shapes[child.tag] = shape
    return False


def is_well_formed(text):
    """Prüft die Wohlgeformtheit eines Dokuments.

    Wohlgeformt heißt: ein Wurzelelement, geschachtelte und geschlossene
    Elemente, gültige Namen. Ob es einem Schema entspricht, ist eine
    andere Frage.
    """
    try:
        elements.fromstring(text)
    except elements.ParseError:
        return False
    return True


def order_matters():
    """Beschreibt den Unterschied zur Relation.

    In einem Dokument trägt die Reihenfolge der Geschwister Bedeutung, in
    einer Relation ist die Tupelmenge ungeordnet.
    """
    return {"xml": "ordered", "relation": "unordered"}


def schema_languages():
    """Nennt die Sprachen, in denen sich Gültigkeit beschreiben lässt."""
    return ["DTD", "XML Schema", "Relax NG"]
