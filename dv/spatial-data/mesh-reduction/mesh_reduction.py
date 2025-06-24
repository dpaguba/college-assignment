"""Netzreduktion durch Kantenkontraktion mit quadratischer Fehlermetrik."""

import itertools


def example_mesh(size=3):
    """Liefert ein Dreiecksnetz über dem Paraboloid z = x² + y².

    Die Fläche ist gekrümmt, also haben benachbarte Dreiecke verschiedene
    Normalen; auf einer ebenen Fläche wäre jede Kontraktion fehlerfrei und
    die Metrik ohne Aussage.

    Args:
        size: Zahl der Gitterpunkte je Achse.

    Returns:
        Abbildung mit ``vertices`` und ``triangles``.
    """
    vertices = []
    for row in range(size):
        for column in range(size):
            x = column / (size - 1)
            y = row / (size - 1)
            vertices.append((x, y, x * x + y * y))
    triangles = []
    for row in range(size - 1):
        for column in range(size - 1):
            first = row * size + column
            triangles.append((first, first + 1, first + size))
            triangles.append((first + 1, first + size + 1, first + size))
    return {"vertices": vertices, "triangles": triangles}


def plane_of(triangle, vertices):
    """Bestimmt die Ebenengleichung eines Dreiecks als (a, b, c, d).

    Der Normalenvektor wird auf die Länge eins gebracht, damit der
    Abstand eines Punktes zur Ebene direkt aus der Gleichung folgt.

    Raises:
        ValueError: bei einem entarteten Dreieck.
    """
    a, b, c = (vertices[index] for index in triangle)
    first = tuple(b[axis] - a[axis] for axis in range(3))
    second = tuple(c[axis] - a[axis] for axis in range(3))
    normal = (first[1] * second[2] - first[2] * second[1],
              first[2] * second[0] - first[0] * second[2],
              first[0] * second[1] - first[1] * second[0])
    length = sum(value * value for value in normal) ** 0.5
    if length < 1e-12:
        raise ValueError("entartetes Dreieck")
    normal = tuple(value / length for value in normal)
    offset = -sum(normal[axis] * a[axis] for axis in range(3))
    return normal + (offset,)


def quadric(planes):
    """Summiert die äusseren Produkte der Ebenengleichungen.

    Die entstehende symmetrische 4×4-Matrix misst den quadrierten Abstand
    eines Punktes zu allen beteiligten Ebenen zugleich.
    """
    matrix = [[0.0] * 4 for _ in range(4)]
    for plane in planes:
        for row in range(4):
            for column in range(4):
                matrix[row][column] += plane[row] * plane[column]
    return matrix


def quadric_error(matrix, point):
    """Wertet die Fehlermetrik an einem Punkt aus."""
    vector = (point[0], point[1], point[2], 1.0)
    return sum(vector[row] * matrix[row][column] * vector[column]
               for row in range(4) for column in range(4))


def vertex_quadrics(mesh):
    """Berechnet für jeden Knoten die Summe der Ebenen seiner Dreiecke."""
    planes = {index: [] for index in range(len(mesh["vertices"]))}
    for triangle in mesh["triangles"]:
        try:
            plane = plane_of(triangle, mesh["vertices"])
        except ValueError:
            continue
        for index in triangle:
            planes[index].append(plane)
    return {index: quadric(entries) for index, entries in planes.items()}


def edges(mesh):
    """Sammelt die Kanten des Netzes als sortierte Indexpaare."""
    found = set()
    for triangle in mesh["triangles"]:
        for first, second in itertools.combinations(triangle, 2):
            found.add(tuple(sorted((first, second))))
    return sorted(found)


def collapse_cost(mesh, edge):
    """Kosten einer Kontraktion: der Fehler am Mittelpunkt der Kante."""
    quadrics = vertex_quadrics(mesh)
    first, second = edge
    combined = [[quadrics[first][row][column] + quadrics[second][row][column]
                 for column in range(4)] for row in range(4)]
    a = mesh["vertices"][first]
    b = mesh["vertices"][second]
    middle = tuple((a[axis] + b[axis]) / 2 for axis in range(3))
    return quadric_error(combined, middle)


def collapse(mesh, edge):
    """Zieht eine Kante auf ihren Mittelpunkt zusammen.

    Dreiecke, die beide Endpunkte enthalten, verschwinden; die übrigen
    verweisen danach auf den neuen Punkt.

    Returns:
        Das reduzierte Netz.

    Raises:
        ValueError: wenn die Kante nicht im Netz liegt.
    """
    first, second = sorted(edge)
    if (first, second) not in edges(mesh):
        raise ValueError("Kante gehoert nicht zum Netz")
    a = mesh["vertices"][first]
    b = mesh["vertices"][second]
    middle = tuple((a[axis] + b[axis]) / 2 for axis in range(3))
    vertices = []
    mapping = {}
    for index, vertex in enumerate(mesh["vertices"]):
        if index == second:
            continue
        mapping[index] = len(vertices)
        vertices.append(middle if index == first else vertex)
    mapping[second] = mapping[first]
    triangles = []
    for triangle in mesh["triangles"]:
        moved = tuple(mapping[index] for index in triangle)
        if len(set(moved)) < 3:
            continue
        if tuple(sorted(moved)) in [tuple(sorted(other))
                                    for other in triangles]:
            continue
        triangles.append(moved)
    return {"vertices": vertices, "triangles": triangles}


def collapse_once(mesh):
    """Kontrahiert die billigste Kante des Netzes."""
    best = min(edges(mesh), key=lambda edge: collapse_cost(mesh, edge))
    return collapse(mesh, best)


def chooses_the_cheapest():
    """Prüft, dass die gewählte Kante wirklich die billigste ist.

    Returns:
        Abbildung mit den Kosten der gewählten und der teuersten Kante.
    """
    mesh = example_mesh()
    costs = {edge: collapse_cost(mesh, edge) for edge in edges(mesh)}
    chosen = min(costs, key=costs.get)
    return {"chosen": chosen, "cost": costs[chosen],
            "most expensive": max(costs.values()),
            "cheapest first": costs[chosen] == min(costs.values())}


def distance_to_mesh(mesh, point):
    """Kleinster Abstand eines Punktes zu den Ebenen der Dreiecke."""
    smallest = None
    for triangle in mesh["triangles"]:
        try:
            plane = plane_of(triangle, mesh["vertices"])
        except ValueError:
            continue
        distance = abs(sum(plane[axis] * point[axis] for axis in range(3))
                       + plane[3])
        smallest = distance if smallest is None else min(smallest, distance)
    return 0.0 if smallest is None else smallest


def error_grows_with_reduction(size=4):
    """Misst den Abstand der ursprünglichen Knoten zum reduzierten Netz.

    Gemessen wird nach jedem Schritt der grösste Abstand eines
    ursprünglichen Knotens zur nächstgelegenen Dreiecksebene des
    reduzierten Netzes.

    Returns:
        Abbildung mit den Werten nach zwei und nach vier Kontraktionen und
        dem ganzen Verlauf.
    """
    mesh = example_mesh(size)
    original = list(mesh["vertices"])
    history = {}
    for step in range(1, 5):
        mesh = collapse_once(mesh)
        history[step] = max(distance_to_mesh(mesh, point)
                            for point in original)
    return {"after two": history[2], "after four": history[4],
            "history": history}


def error_measures():
    """Nennt die Fehlermasse, die die Vorlesung für Netze aufführt."""
    return {"vertex to plane": "the quadric used here",
            "hausdorff": "largest distance between the two surfaces",
            "volume": "difference of the enclosed volumes"}
