"""Wordspotting mit einer aus Text erzeugten Anfrage."""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))
for _name in (("..", "word-segmentation"),
              ("..", "retrieval-evaluation"),
              ("..", "query-by-example")):
    sys.path.insert(0, os.path.join(_HERE, *_name))

import query_by_example as qbe
import retrieval_evaluation as ev
import word_segmentation as ws

QUERY_FONTS = ("/System/Library/Fonts/Supplemental/Georgia.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
               "/Library/Fonts/Arial.ttf")


def _font(size):
    """Sucht eine Schrift für die Anfrage.

    Genommen wird bewusst eine andere als die der Seite. Im Projekt ist
    die Vorlage eine Handschrift und die Anfrage gesetzt; wer beide aus
    derselben Datei zeichnet, misst nicht die Aufgabe, sondern den
    Zufall, dass die Bilder gleich sind.
    """
    for path in QUERY_FONTS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render(text, height=44, padding=6):
    """Zeichnet ein Anfragebild aus einer Zeichenkette.

    Raises:
        ValueError: bei einer leeren Kette oder einer nicht positiven
            Höhe.
    """
    if not text:
        raise ValueError("leere Zeichenkette")
    if height <= 0:
        raise ValueError("die Höhe muss positiv sein")
    font = _font(height)
    canvas = Image.new("L", (height * len(text) + 4 * padding,
                             height * 3), color=255)
    draw = ImageDraw.Draw(canvas)
    draw.text((padding, height), text, font=font, fill=0)
    field = np.asarray(canvas, dtype=float)
    rows = np.where((field < 128).sum(axis=1) > 0)[0]
    columns = np.where((field < 128).sum(axis=0) > 0)[0]
    if not len(rows) or not len(columns):
        raise ValueError("die Schrift zeichnet nichts")
    return field[rows[0]:rows[-1] + 1, columns[0]:columns[-1] + 1]


def gaussian_kernel(sigma):
    """Baut einen eindimensionalen Gausskern.

    Raises:
        ValueError: bei einem nicht positiven Sigma.
    """
    if sigma <= 0.0:
        raise ValueError("Sigma muss positiv sein")
    radius = max(1, int(np.ceil(3.0 * sigma)))
    offsets = np.arange(-radius, radius + 1, dtype=float)
    kernel = np.exp(-(offsets ** 2) / (2.0 * sigma ** 2))
    return kernel / kernel.sum()


def blur(image, sigma=1.0):
    """Glättet ein Bild mit einem trennbaren Gausskern.

    Die Anfrage aus gesetzter Schrift hat scharfe Kanten, die Vorlage
    nicht. Das Glätten gleicht diesen Unterschied an, bevor die
    Gradienten gerechnet werden.

    Raises:
        ValueError: bei einem nicht positiven Sigma oder einem leeren
            Bild.
    """
    field = np.asarray(image, dtype=float)
    if field.ndim != 2 or field.size == 0:
        raise ValueError("leeres oder falsch geformtes Bild")
    kernel = gaussian_kernel(sigma)
    radius = len(kernel) // 2
    padded = np.pad(field, ((0, 0), (radius, radius)), mode="edge")
    rows = sum(kernel[index] * padded[:, index:index + field.shape[1]]
               for index in range(len(kernel)))
    padded = np.pad(rows, ((radius, radius), (0, 0)), mode="edge")
    return sum(kernel[index] * padded[index:index + field.shape[0], :]
               for index in range(len(kernel)))


def evaluate(sigma=1.0, vocabulary_size=32, levels=2, measure="cosine",
             seed=0, step=5, window=12, height=44):
    """Synthetisiert jede Anfrage aus ihrem Wort und misst die AP.

    Returns:
        Abbildung mit der mittleren Average Precision.

    Raises:
        ValueError: bei einem unbekannten Mass.
    """
    field, boxes, labels = ws.page()
    images = qbe.word_images(field, boxes)
    centroids = qbe.vocabulary(images, size=vocabulary_size, seed=seed,
                               step=step, window=window)
    built = [qbe.represent(image, centroids, levels, step, window)
             for image in images]
    runs = []
    shares = []
    for word in sorted(set(labels)):
        drawn = render(word, height=height)
        if sigma > 0.0:
            drawn = blur(drawn, sigma)
        query = qbe.represent(drawn, centroids, levels, step, window)
        order = qbe.ranking(query, built, measure)
        results = [1 if labels[index] == word else 0 for index in order]
        relevant = sum(results)
        runs.append((results, relevant))
        shares.append(relevant / len(results))
    return {"mAP": ev.mean_average_precision(runs),
            "queries": len(runs), "chance": float(np.mean(shares)),
            "sigma": sigma, "measure": measure}


def blur_helps():
    """Misst, wie viel das Glätten der Anfrage bringt.

    Returns:
        Abbildung mit der mittleren AP je Sigma.
    """
    tried = {0.0: evaluate(sigma=0.0)["mAP"]}
    for sigma in (0.5, 1.0, 1.5, 2.0, 3.0):
        tried[sigma] = evaluate(sigma=sigma)["mAP"]
    best = max(tried, key=lambda key: tried[key])
    return {"tried": tried, "best sigma": best, "best": tried[best],
            "without blur": tried[0.0],
            "why": "die gesetzte Schrift hat schärfere Kanten als die "
                   "Vorlage"}


def the_gap_to_query_by_example():
    """Vergleicht die beiden Arten der Anfrage.

    Die Anfrage aus einer Zeichenkette ist die nützlichere: wer sucht,
    hat ein Wort im Kopf und selten ein Bild davon. Sie ist zugleich die
    schwierigere, weil das erzeugte Bild aus einer anderen Schrift
    stammt als die Vorlage und die Gradienten deshalb anders liegen.

    Returns:
        Abbildung mit beiden Werten.
    """
    first = qbe.evaluate()["mAP"]
    second = evaluate()["mAP"]
    return {"query by example": first, "query by string": second,
            "difference": first - second,
            "why the string is harder": "das erzeugte Bild stammt aus "
                                        "einer anderen Schrift",
            "why it is used anyway": "wer sucht, hat ein Wort und "
                                     "selten ein Bild"}
