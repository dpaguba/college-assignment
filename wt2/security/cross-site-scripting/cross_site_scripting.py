"""Cross-site scripting: was die Ausgabe mit fremdem Text machen darf."""

import html
from html.parser import HTMLParser


class _TagCollector(HTMLParser):
    """Sammelt die Elemente, die ein Browser ausführen würde."""

    def __init__(self):
        """Legt den Sammler an."""
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attributes):
        """Vermerkt ein Element, wenn es Kode ausführen kann."""
        if tag in ("script", "iframe", "object", "embed"):
            self.found.append(tag)
        for name, _ in attributes:
            if name.lower().startswith("on"):
                self.found.append(name.lower())


def executable_tags(page):
    """Nennt die Elemente und Ereignisse, die der Browser ausführen würde.

    Die Seite wird mit dem Parser der Standardbibliothek gelesen, nicht
    mit einem eigenen Muster: was hier gefunden wird, ist das, was ein
    Leser der Seite findet.
    """
    collector = _TagCollector()
    collector.feed(page)
    return collector.found


def render(text, escape=True):
    """Setzt fremden Text in eine Seite ein.

    Args:
        text: der Text, der aus einer Eingabe stammt.
        escape: ob die Sonderzeichen ersetzt werden.

    Returns:
        Die fertige Seite.
    """
    content = html.escape(text) if escape else text
    return "<html><body><p>%s</p></body></html>" % content


def render_attribute(value, escape=True):
    """Setzt fremden Text in ein Attribut ein.

    Im Attribut genügt das Ersetzen der spitzen Klammern nicht: ein
    Anführungszeichen beendet den Wert und alles danach wird zu weiteren
    Attributen.
    """
    content = html.escape(value, quote=True) if escape else value
    return '<html><body><img src="x" alt="%s"></body></html>' % content


def kinds():
    """Nennt die drei Arten und wo der Text herkommt."""
    return {"stored": "the text was saved and is shown to everyone",
            "reflected": "the text comes back from the request itself",
            "dom based": "the page builds the markup from a value in the "
                         "browser, the server never sees it"}


def policy_blocks_inline(policy):
    """Prüft, ob eine Richtlinie eingebetteten Kode verbietet.

    Eine Richtlinie, die eingebetteten Kode ausdrücklich erlaubt, hebt
    ihren eigenen Schutz auf.
    """
    return "'unsafe-inline'" not in policy


def contexts():
    """Nennt die Stellen, an denen jeweils anders ersetzt werden muss."""
    return {"element content": "escape < > &",
            "attribute value": "escape the quotes as well",
            "url": "check the scheme, javascript: is a scheme",
            "script": "no user text belongs there at all",
            "style": "no user text belongs there either"}


def defence_order():
    """Nennt die Massnahmen in der Reihenfolge ihrer Wirkung."""
    return ["escape at the point of output, for that context",
            "validate the input, as a second net",
            "a content security policy, as a third",
            "the http only flag, so a script cannot read the cookie"]
