"""Das Reifegradmodell von Richardson."""

LEVELS = {
    0: "one endpoint, one method, the action is in the body",
    1: "many resources, still one method",
    2: "the http methods carry the meaning",
    3: "the answers carry links to what can be done next",
}


def levels():
    """Nennt die vier Stufen mit ihrer Beschreibung."""
    return dict(LEVELS)


def level(paths, methods, hypermedia):
    """Ordnet eine Schnittstelle einer Stufe zu.

    Args:
        paths: die angebotenen Adressen.
        methods: die benutzten HTTP-Methoden.
        hypermedia: ob die Antworten Verweise enthalten.

    Returns:
        Die Stufe von null bis drei.

    Raises:
        ValueError: wenn weder Adressen noch Methoden genannt sind.
    """
    if not paths or not methods:
        raise ValueError("weder Adressen noch Methoden genannt")
    if hypermedia:
        return 3
    meaningful = {method for method in methods
                  if method in ("GET", "PUT", "DELETE", "PATCH")}
    if meaningful:
        return 2
    if len(set(paths)) > 1:
        return 1
    return 0


def hypermedia_example():
    """Zeigt eine Antwort der dritten Stufe.

    Der Aufrufer muss die Folgeadressen nicht kennen; er liest sie aus
    der Antwort. Das ist der Punkt, an dem sich Server und Aufrufer
    unabhängig ändern können.

    Returns:
        Eine Antwort mit Feldern und Verweisen.
    """
    return {"id": 7, "title": "Der Prozess",
            "links": {"self": "/books/7", "author": "/authors/3",
                      "reviews": "/books/7/reviews"}}


def what_each_level_buys():
    """Beschreibt, was jede Stufe gegenüber der vorigen gewinnt."""
    return {1: "resources can be cached and addressed separately",
            2: "the method says what happens, so intermediaries understand it",
            3: "the client follows links instead of building addresses"}
