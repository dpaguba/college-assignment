"""Wordspotting ohne vorherige Segmentierung."""

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _name in (("..", "word-segmentation"),
              ("..", "retrieval-evaluation"),
              ("..", "query-by-example"),
              ("..", "..", "image-features", "lloyd-clustering")):
    sys.path.insert(0, os.path.join(_HERE, *_name))

import lloyd_clustering
import query_by_example as qbe
import retrieval_evaluation as ev
import word_segmentation as ws

SOBEL_H = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)

SOBEL_V = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)

_CACHE = {}


def _correlate(field, mask):
    """Kreuzkorrelation mit fortgesetztem Rand."""
    high = mask.shape[0] // 2
    wide = mask.shape[1] // 2
    padded = np.pad(field, ((high, high), (wide, wide)), mode="edge")
    result = np.zeros_like(field)
    for row in range(mask.shape[0]):
        for column in range(mask.shape[1]):
            result += mask[row][column] * padded[
                row:row + field.shape[0], column:column + field.shape[1]]
    return result


def _descriptors(field, step, window, cells, bins):
    """Beschreibt die Seite an allen Gitterpunkten auf einmal.

    Die Gradienten werden für die ganze Seite einmal gerechnet und dann
    ausgeschnitten. Jeder Ausschnitt einzeln zu behandeln wäre dieselbe
    Rechnung, nur so oft wiederholt, wie sich die Fenster überlappen.

    Returns:
        Ein Tripel aus Deskriptoren, Zeilen und Spalten des Gitters.
    """
    horizontal = _correlate(field, SOBEL_V)
    vertical = _correlate(field, SOBEL_H)
    magnitude = np.sqrt(horizontal ** 2 + vertical ** 2)
    angle = np.arctan2(vertical, horizontal) % (2.0 * np.pi)
    index = np.minimum((angle / (2.0 * np.pi) * bins).astype(int),
                       bins - 1)
    half = window // 2
    rows = list(range(half, field.shape[0] - half + 1, step))
    columns = list(range(half, field.shape[1] - half + 1, step))
    built = np.zeros((len(rows), len(columns), cells * cells * bins))
    for one, row in enumerate(rows):
        for two, column in enumerate(columns):
            piece = (slice(row - half, row - half + window),
                     slice(column - half, column - half + window))
            weights = magnitude[piece]
            classes = index[piece]
            parts = []
            for block_row in np.array_split(np.arange(window), cells):
                for block_column in np.array_split(np.arange(window),
                                                   cells):
                    cut = np.ix_(block_row, block_column)
                    parts.append(np.bincount(classes[cut].reshape(-1),
                                             weights=weights[cut].reshape(-1),
                                             minlength=bins))
            built[one][two] = np.concatenate(parts)
    lengths = np.linalg.norm(built, axis=2, keepdims=True)
    built = np.divide(built, lengths, out=np.zeros_like(built),
                      where=lengths > 1e-9)
    return built, rows, columns


def index(step=6, window=12, cells=2, bins=8, vocabulary_size=32, seed=0):
    """Indiziert die ganze Seite mit einem dichten Gitter.

    Args:
        step: der Abstand der Gitterpunkte.
        window: die Kantenlänge eines Fensters.
        cells: die Zellen je Kante eines Deskriptors.
        bins: die Richtungsklassen.
        vocabulary_size: die Grösse des visuellen Vokabulars.
        seed: der Startwert der Clusteranalyse.

    Returns:
        Abbildung mit dem Gitter der zugeordneten Wörter.

    Raises:
        ValueError: bei einer nicht positiven Vokabulargrösse.
    """
    if vocabulary_size <= 0:
        raise ValueError("die Grösse des Vokabulars muss positiv sein")
    key = (step, window, cells, bins, vocabulary_size, seed)
    if key in _CACHE:
        return _CACHE[key]
    field, boxes, labels = ws.page()
    built, rows, columns = _descriptors(field, step, window, cells, bins)
    flat = built.reshape(-1, built.shape[2])
    taken = flat[::7] if len(flat) > 4000 else flat
    centroids = lloyd_clustering.cluster(taken, k=vocabulary_size,
                                         seed=seed)["centroids"]
    measured = ((flat[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    words = np.argmin(measured, axis=1).reshape(len(rows), len(columns))
    report = {"words": words, "rows": rows, "columns": columns,
              "centroids": centroids, "page": field, "boxes": boxes,
              "labels": labels, "patches": int(words.size),
              "vocabulary": vocabulary_size}
    _CACHE[key] = report
    return report


def _pyramid_from_grid(words, size, levels):
    """Baut die Pyramide aus einem rechteckigen Stück des Gitters."""
    parts = []
    for level in range(levels):
        count = 2 ** level
        cells = np.zeros((count, count, size))
        row_blocks = np.array_split(np.arange(words.shape[0]), count)
        column_blocks = np.array_split(np.arange(words.shape[1]), count)
        for one, row_block in enumerate(row_blocks):
            for two, column_block in enumerate(column_blocks):
                if not len(row_block) or not len(column_block):
                    continue
                cut = words[np.ix_(row_block, column_block)].reshape(-1)
                cells[one][two] = np.bincount(cut, minlength=size)
        parts.append(cells.reshape(-1))
    built = np.concatenate(parts)
    total = built.sum()
    return built / total if total > 0 else built


def suppress(boxes, scores, threshold=0.3):
    """Behält von überlappenden Funden nur den stärksten.

    Ohne diesen Schritt steht dasselbe Wort mehrfach in der Liste, weil
    benachbarte Fenster fast dasselbe zeigen. Die Liste sähe dann
    besser aus, als sie ist, denn ein einziger Treffer würde die ersten
    Plätze füllen.

    Args:
        boxes: die Rahmen.
        scores: ihre Bewertungen, grösser ist besser.
        threshold: ab welchem Überlapp unterdrückt wird.

    Gerechnet wird über Felder statt über Paare, weil die Zahl der
    Fenster in die Tausende geht und der paarweise Vergleich quadratisch
    wächst.

    Returns:
        Die Indizes der behaltenen Rahmen, nach Bewertung sortiert.

    Raises:
        ValueError: bei einer leeren Liste, einem Rahmen ohne Fläche
            oder einem Schwellwert ausserhalb von null bis eins.
    """
    if not len(boxes) or len(boxes) != len(scores):
        raise ValueError("leere Liste oder unpassend viele Bewertungen")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("der Schwellwert liegt zwischen null und eins")
    field = np.asarray(boxes, dtype=float)
    if field.ndim != 2 or field.shape[1] != 4:
        raise ValueError("ein Rahmen besteht aus vier Zahlen")
    if np.any(field[:, 2] <= field[:, 0]) or np.any(field[:, 3]
                                                    <= field[:, 1]):
        raise ValueError("ein Rahmen ohne Fläche")
    areas = ((field[:, 2] - field[:, 0]) * (field[:, 3] - field[:, 1]))
    order = list(np.argsort(-np.asarray(scores, dtype=float),
                            kind="stable"))
    kept = []
    while order:
        candidate = order.pop(0)
        kept.append(int(candidate))
        rest = np.asarray(order, dtype=int)
        if not len(rest):
            break
        top = np.maximum(field[candidate][0], field[rest][:, 0])
        left = np.maximum(field[candidate][1], field[rest][:, 1])
        bottom = np.minimum(field[candidate][2], field[rest][:, 2])
        right = np.minimum(field[candidate][3], field[rest][:, 3])
        inside = (np.maximum(0.0, bottom - top)
                  * np.maximum(0.0, right - left))
        union = areas[candidate] + areas[rest] - inside
        measured = np.divide(inside, union, out=np.zeros_like(inside),
                             where=union > 0)
        order = [int(value) for value, keep
                 in zip(rest, measured <= threshold) if keep]
    return kept


def search(word="letter", patch_step=8, levels=2, overlap_threshold=0.5,
           suppression=0.3, length=200, step=6, window=12,
           vocabulary_size=32, seed=0):
    """Sucht ein Wort auf der Seite, ohne sie vorher zu segmentieren.

    Die Seite wird einmal indiziert, dann wird ein Fenster von der Grösse
    des Anfragebilds darüber geschoben. Jede Lage bekommt eine Bewertung,
    die Maxima werden gegen ihre Nachbarn abgesetzt, und die verbleibenden
    Fenster bilden die Rückgabeliste.

    Ein Fundstück zählt nur dann als Treffer, wenn es die Schwelle
    erreicht und das getroffene Wort nicht schon von einem besser
    bewerteten Fenster belegt ist. Ohne diese Regel würde ein einziges
    gefundenes Wort mehrere Treffer liefern, und die Liste sähe umso
    besser aus, je gröber die Unterdrückung eingestellt ist.

    Args:
        word: das gesuchte Wort.
        patch_step: der Abstand zweier Fensterlagen.
        levels: die Stufen der Pyramide.
        overlap_threshold: ab welchem Überlapp ein Fenster als Treffer
            zählt.
        suppression: der Schwellwert der Unterdrückung.
        length: wie viele Fenster die Rückgabeliste umfasst.

    Returns:
        Abbildung mit der Rückgabeliste und ihrer Bewertung.

    Raises:
        ValueError: bei einem unbekannten Wort.
    """
    report = index(step, window, 2, 8, vocabulary_size, seed)
    labels = report["labels"]
    if word not in labels:
        raise ValueError("das Wort steht nicht auf der Seite")
    truth = [box for box, name in zip(report["boxes"], labels)
             if name == word]
    high = int(np.median([box[2] - box[0] for box in truth]))
    wide = int(np.median([box[3] - box[1] for box in truth]))
    rows = np.asarray(report["rows"])
    columns = np.asarray(report["columns"])
    size = report["vocabulary"]

    def piece(top, left):
        """Nennt das Gitterstück eines Fensters."""
        inside_rows = np.where((rows >= top) & (rows < top + high))[0]
        inside_columns = np.where((columns >= left)
                                  & (columns < left + wide))[0]
        if not len(inside_rows) or not len(inside_columns):
            return None
        return report["words"][np.ix_(inside_rows, inside_columns)]

    query_box = truth[0]
    query_piece = piece(query_box[0], query_box[1])
    query = _pyramid_from_grid(query_piece, size, levels)
    boxes = []
    scores = []
    page = report["page"]
    for top in range(0, page.shape[0] - high + 1, patch_step):
        for left in range(0, page.shape[1] - wide + 1, patch_step):
            cut = piece(top, left)
            if cut is None:
                continue
            built = _pyramid_from_grid(cut, size, levels)
            lengths = np.linalg.norm(query) * np.linalg.norm(built)
            score = 0.0 if lengths == 0.0 else float(
                np.dot(query, built) / lengths)
            boxes.append((top, left, top + high, left + wide))
            scores.append(score)
    kept = suppress(boxes, scores, suppression)
    results = []
    best = 0.0
    matched = set()
    for position in kept[:length]:
        overlaps = [ev.overlap(boxes[position], box) for box in truth]
        closest = int(np.argmax(overlaps))
        best = max(best, overlaps[closest])
        hit = (overlaps[closest] >= overlap_threshold
               and closest not in matched)
        if hit:
            matched.add(closest)
        results.append(1 if hit else 0)
    relevant = len(truth)
    return {"scores": scores, "patches": len(scores),
            "kept": len(kept), "results": results,
            "average precision": ev.average_precision(results, relevant),
            "chance": relevant / max(1, len(results)),
            "best overlap": best, "relevant": relevant,
            "word": word, "threshold": overlap_threshold}


def the_threshold_decides():
    """Zeigt, wie stark die Schwelle die gemessene Güte bestimmt.

    Dieselbe Rückgabeliste, zweimal bewertet: bei einer milden Schwelle
    zählen Fenster als Treffer, die das Wort nur zum Teil enthalten, bei
    einer strengen nicht. Die Zahl am Ende sagt deshalb wenig, solange
    die Schwelle nicht dabeisteht.

    Returns:
        Abbildung mit der AP bei verschiedenen Schwellen.
    """
    tried = {value: search(overlap_threshold=value)["average precision"]
             for value in (0.2, 0.3, 0.5, 0.7, 0.8)}
    return {"tried": tried, "at 0.2": tried[0.2], "at 0.8": tried[0.8],
            "spread": tried[0.2] - tried[0.8],
            "why": "eine milde Schwelle zählt Fenster mit, die das Wort "
                   "nur zum Teil enthalten"}


def what_it_costs_to_drop_the_segmentation():
    """Nennt, was der segmentierungsfreie Weg einbringt und kostet.

    Er kommt ohne die Annahme aus, dass sich Wörter über Profile trennen
    lassen, und funktioniert damit auch auf Seiten, an denen die
    Segmentierung scheitert. Dafür wird die Seite an tausenden Stellen
    bewertet statt an dreissig, die Rahmen sitzen nur ungefähr auf den
    Wörtern, und es kommt ein Schritt hinzu, den es vorher nicht gab: die
    Unterdrückung benachbarter Maxima.
    """
    return {"gains": "keine Annahme über trennbare Wortabstände",
            "costs": ["tausende Bewertungen statt dreissig",
                      "die Rahmen sitzen nur ungefähr",
                      "die Unterdrückung kommt als Schritt hinzu"],
            "where it wins": "auf Seiten, an denen die Segmentierung "
                             "scheitert"}
