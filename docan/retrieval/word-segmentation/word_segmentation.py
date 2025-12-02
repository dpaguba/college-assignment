"""Binarisierung und Projektionsprofile zur Wortsegmentierung."""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = ("/System/Library/Fonts/Supplemental/Times New Roman.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "/Library/Fonts/Arial.ttf")

TEXT = (("letter", "orders", "colonel", "camp", "river"),
        ("march", "powder", "horse", "letter", "orders"),
        ("colonel", "camp", "river", "march", "powder"),
        ("horse", "letter", "orders", "colonel", "camp"),
        ("river", "march", "powder", "horse", "letter"),
        ("orders", "colonel", "camp", "river", "march"))

LINES = len(TEXT)

MARGIN = 24
WORD_GAP = 34
LINE_HEIGHT = 56


def _font(size=30):
    """Sucht eine Schrift und weicht auf die eingebaute aus."""
    for path in FONTS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_word(word, font, rng, angle=3.0, scale=0.12):
    """Zeichnet ein Wort mit leichter Drehung und Grössenänderung.

    Ohne diese Streuung wären alle Abbilder desselben Worts bis auf das
    Rauschen gleich, und jede Suche fände sie fehlerfrei. Genau das ist
    an einer gedruckten Vorlage der Unterschied zu einer Handschrift,
    für die das Verfahren gedacht ist.
    """
    size = font.size if hasattr(font, "size") else 30
    canvas = Image.new("L", (size * len(word) + 40, size * 3), color=255)
    draw = ImageDraw.Draw(canvas)
    draw.text((20, size), word, font=font, fill=0)
    factor = 1.0 + rng.uniform(-scale, scale)
    canvas = canvas.resize((max(1, int(canvas.width * factor)),
                            max(1, int(canvas.height * factor))))
    canvas = canvas.rotate(rng.uniform(-angle, angle), expand=True,
                           fillcolor=255)
    field = np.asarray(canvas, dtype=float)
    rows = np.where((field < 128).sum(axis=1) > 0)[0]
    columns = np.where((field < 128).sum(axis=0) > 0)[0]
    if not len(rows) or not len(columns):
        return field, (0, 0, field.shape[0], field.shape[1])
    return (field[rows[0]:rows[-1] + 1, columns[0]:columns[-1] + 1],
            (0, 0, int(rows[-1] - rows[0]) + 1,
             int(columns[-1] - columns[0]) + 1))


def page(size=30, seed=0, noise=3.0):
    """Zeichnet eine Seite und gibt die Rahmen der Wörter mit.

    Der Datensatz des Fachprojekts liegt nicht bei, deshalb wird die
    Seite erzeugt. Das hat einen Vorteil: die Ground Truth ist nicht
    geschätzt, sondern bekannt, und jede Segmentierung lässt sich exakt
    dagegen halten. Jedes Wort wird leicht gedreht und skaliert, damit
    zwei Abbilder desselben Worts nicht identisch sind.

    Args:
        size: die Schriftgrösse.
        seed: der Startwert des Zufallsgenerators.
        noise: die Stärke des Rauschens.

    Returns:
        Ein Tripel aus Bild, Rahmen und Wörtern.
    """
    font = _font(size)
    rng = np.random.default_rng(seed)
    height = MARGIN * 2 + LINE_HEIGHT * len(TEXT)
    field = np.full((height, 1000), 255.0)
    boxes = []
    labels = []
    for row, line in enumerate(TEXT):
        top = MARGIN + row * LINE_HEIGHT
        left = MARGIN
        for word in line:
            patch, _ = _draw_word(word, font, rng)
            high, wide = patch.shape
            place = top + max(0, (LINE_HEIGHT - 12 - high) // 2)
            piece = field[place:place + high, left:left + wide]
            field[place:place + high, left:left + wide] = np.minimum(
                piece, patch[:piece.shape[0], :piece.shape[1]])
            boxes.append((place, left, place + piece.shape[0],
                          left + piece.shape[1]))
            labels.append(word)
            left += wide + WORD_GAP
    if noise > 0.0:
        field = np.clip(field + rng.normal(size=field.shape) * noise,
                        0.0, 255.0)
    return field, boxes, labels


def _grey(image):
    """Prüft ein Graubild.

    Raises:
        ValueError: bei einem leeren Bild.
    """
    field = np.asarray(image, dtype=float)
    if field.ndim != 2 or field.size == 0:
        raise ValueError("leeres oder falsch geformtes Bild")
    return field


def otsu(image):
    """Sucht die Schwelle nach Otsu.

    Gesucht wird die Schwelle, die die Varianz zwischen den beiden
    Klassen maximiert. Gerechnet wird über die laufenden Summen des
    Histogramms, sodass ein Durchlauf genügt.

    Raises:
        ValueError: bei einem leeren Bild.
    """
    field = _grey(image)
    counted = np.bincount(np.clip(field, 0, 255).astype(int).reshape(-1),
                          minlength=256).astype(float)
    total = counted.sum()
    weights = np.cumsum(counted) / total
    values = np.cumsum(counted * np.arange(256)) / total
    mean = values[-1]
    with np.errstate(invalid="ignore", divide="ignore"):
        between = ((mean * weights - values) ** 2
                   / (weights * (1.0 - weights)))
    between[~np.isfinite(between)] = -1.0
    return int(np.argmax(between))


def otsu_by_search(image):
    """Sucht dieselbe Schwelle durch vollständiges Durchprobieren.

    Die Rechnung über die laufenden Summen ist schnell und undurchsichtig;
    diese hier ist langsam und liest sich wie die Definition. Dass beide
    dieselbe Schwelle liefern, ist die Probe.

    Raises:
        ValueError: bei einem leeren Bild.
    """
    field = _grey(image)
    values = np.clip(field, 0, 255).astype(int).reshape(-1)
    best = (-1.0, 0)
    for threshold in range(256):
        dark = values[values <= threshold]
        light = values[values > threshold]
        if len(dark) == 0 or len(light) == 0:
            continue
        share = len(dark) / len(values)
        spread = share * (1.0 - share) * (dark.mean() - light.mean()) ** 2
        if spread > best[0]:
            best = (spread, threshold)
    return best[1]


def binarise(image, threshold=None):
    """Trennt Tinte von Papier.

    Returns:
        Abbildung mit dem Binärbild, der Schwelle und den beiden
        Mittelwerten.

    Raises:
        ValueError: bei einem leeren Bild.
    """
    field = _grey(image)
    threshold = otsu(field) if threshold is None else threshold
    binary = (field <= threshold).astype(int)
    ink = field[binary == 1]
    paper = field[binary == 0]
    return {"binary": binary, "threshold": threshold,
            "ink mean": float(ink.mean()) if ink.size else float("nan"),
            "paper mean": float(paper.mean()) if paper.size
            else float("nan"),
            "ink share": float(binary.mean())}


def _runs(profile, gap):
    """Findet die Abschnitte, die durch genügend grosse Lücken getrennt
    sind.
    """
    found = []
    start = None
    empty = 0
    for index, value in enumerate(profile):
        if value > 0:
            if start is None:
                start = index - empty if empty and found else index
                if found and index - empty <= found[-1][1]:
                    start = index
            empty = 0
        elif start is not None:
            empty += 1
            if empty >= gap:
                found.append((start, index - empty + 1))
                start = None
                empty = 0
    if start is not None:
        found.append((start, len(profile) - empty))
    return found


def lines(image, gap=8):
    """Findet die Zeilen über das waagerechte Projektionsprofil.

    Gezählt wird je Zeile die Menge der Tinte. Zwischen zwei Textzeilen
    steht eine Folge leerer Bildzeilen, und die trennt.

    Raises:
        ValueError: bei einem leeren Bild.
    """
    binary = binarise(image)["binary"]
    return _runs(binary.sum(axis=1), gap)


def words(image, gap=14, line_gap=8):
    """Findet die Wörter über das senkrechte Profil je Zeile.

    Innerhalb einer Zeile trennt eine Lücke von genügend vielen leeren
    Spalten zwei Wörter. Die Grenze zwischen dem Abstand zweier
    Buchstaben und dem Abstand zweier Wörter ist der einzige Parameter,
    und sie ist eine Setzung.

    Returns:
        Liste der Rahmen als oben, links, unten, rechts.

    Raises:
        ValueError: bei einem leeren Bild.
    """
    binary = binarise(image)["binary"]
    found = []
    for top, bottom in _runs(binary.sum(axis=1), line_gap):
        band = binary[top:bottom]
        for left, right in _runs(band.sum(axis=0), gap):
            piece = band[:, left:right]
            rows = np.where(piece.sum(axis=1) > 0)[0]
            if not len(rows):
                continue
            found.append((top + int(rows[0]), left,
                          top + int(rows[-1]) + 1, right))
    return found


def the_gap_decides():
    """Zeigt, dass der Abstand allein über die Wortzahl entscheidet.

    Mit einer kleinen Lücke zerfallen Wörter in Buchstabengruppen, mit
    einer grossen wachsen benachbarte Wörter zusammen. Dazwischen liegt
    ein Bereich, in dem die Zahl stimmt, und wie breit dieser Bereich
    ist, hängt an der Schrift: eine enge Handschrift lässt ihn
    verschwinden, und dann ist die Segmentierung über Profile am Ende.

    Returns:
        Abbildung mit der Wortzahl bei verschiedenen Lücken.
    """
    field, boxes, _ = page()
    counted = {gap: len(words(field, gap=gap))
               for gap in (2, 6, 10, 14, 20, 30, 45, 60)}
    return {"counted": counted, "truth": len(boxes),
            "words at a small gap": counted[6],
            "words at a large gap": counted[60],
            "the range that works": [gap for gap, value
                                     in counted.items()
                                     if value == len(boxes)],
            "what ends the method": "eine Handschrift ohne klare "
                                    "Wortabstände"}


def why_the_profile_is_enough_here():
    """Sagt, wofür das Verfahren reicht und wofür nicht.

    Ein Projektionsprofil setzt voraus, dass die Zeilen waagerecht
    laufen und sich nicht überschneiden. Auf einer gedruckten oder
    sauber geschriebenen Seite trifft das zu. Sobald die Zeilen schräg
    stehen oder Unter- und Oberlängen ineinandergreifen, verschmelzen
    die Zeilen im Profil, und es hilft nur noch, die Seite vorher
    geradezurücken.
    """
    return {"assumes": "waagerechte, getrennte Zeilen",
            "fails on": "schräge Zeilen und ineinandergreifende "
                        "Ober- und Unterlängen",
            "the usual fix": "die Seite vorher geraderücken",
            "cost": "ein Parameter für die Lücke, den niemand herleiten "
                    "kann"}
