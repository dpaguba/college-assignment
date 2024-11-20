"""Ein kleines Netz und sein Gradient."""

import numpy as np


def sigmoid(value):
    """Die logistische Funktion."""
    return 1.0 / (1.0 + np.exp(-np.clip(value, -500.0, 500.0)))


def sigmoid_slope(output):
    """Die Ableitung, ausgedrückt durch den Ausgabewert selbst.

    Das ist der Grund, warum die Funktion so beliebt war: für die
    Rückwärtsrechnung genügt der schon berechnete Ausgabewert, es muss
    nichts zusätzlich gespeichert werden.
    """
    return output * (1.0 - output)


def build(sizes, seed=0, scale=1.0):
    """Legt ein Netz mit zufälligen Gewichten an.

    Raises:
        ValueError: bei weniger als zwei Schichten oder einer Schicht
            ohne Neuronen.
    """
    if len(sizes) < 2:
        raise ValueError("ein Netz braucht Eingabe und Ausgabe")
    if any(size <= 0 for size in sizes):
        raise ValueError("jede Schicht braucht Neuronen")
    rng = np.random.default_rng(seed)
    return [{"weights": rng.normal(size=(one, two))
             * scale / np.sqrt(one),
             "bias": np.zeros(two)}
            for one, two in zip(sizes, sizes[1:])]


def forward(model, inputs):
    """Rechnet das Netz vorwärts und behält die Zwischenwerte.

    Returns:
        Abbildung mit der Ausgabe und den Aktivierungen jeder Schicht.
    """
    values = np.asarray(inputs, dtype=float)
    activations = [values]
    for layer in model:
        values = sigmoid(values @ layer["weights"] + layer["bias"])
        activations.append(values)
    return {"output": values, "activations": activations}


def loss(model, inputs, targets):
    """Der mittlere quadratische Fehler."""
    got = forward(model, inputs)["output"]
    return float(np.mean((got - np.asarray(targets, dtype=float)) ** 2))


def gradients(model, inputs, targets):
    """Rechnet die Ableitungen durch Rückwärtsrechnen aus.

    Der Fehler wird von der Ausgabe her durch die Schichten
    zurückgereicht, jeweils multipliziert mit der Ableitung der
    Aktivierung und mit den Gewichten der nächsten Schicht. Mehr ist die
    Kettenregel nicht, und mehr ist Backpropagation nicht.

    Returns:
        Liste der Ableitungen je Schicht.
    """
    values = np.asarray(inputs, dtype=float)
    wanted = np.asarray(targets, dtype=float)
    report = forward(model, values)
    activations = report["activations"]
    count = values.shape[0] * wanted.shape[1]
    delta = 2.0 * (activations[-1] - wanted) / count
    delta = delta * sigmoid_slope(activations[-1])
    found = [None] * len(model)
    for index in range(len(model) - 1, -1, -1):
        found[index] = {"weights": activations[index].T @ delta,
                        "bias": delta.sum(axis=0)}
        if index > 0:
            delta = (delta @ model[index]["weights"].T
                     * sigmoid_slope(activations[index]))
    return found


def gradient_check(sizes=(3, 4, 2), points=5, step=1e-6, seed=0):
    """Prüft den Gradienten gegen den Differenzenquotienten.

    Jeder einzelne Parameter wird um ein kleines Stück nach oben und
    nach unten verschoben, und die Änderung des Fehlers geteilt durch
    die Schrittweite muss die berechnete Ableitung ergeben. Das ist die
    einzige Prüfung, die eine falsche Rückwärtsrechnung sicher findet:
    ein Vorzeichenfehler lässt das Netz weiter lernen, nur langsamer,
    und fällt sonst nicht auf.

    Returns:
        Abbildung mit der grössten Abweichung.

    Raises:
        ValueError: bei einer nicht positiven Schrittweite.
    """
    if step <= 0:
        raise ValueError("die Schrittweite muss positiv sein")
    rng = np.random.default_rng(seed)
    model = build(sizes, seed=seed)
    inputs = rng.normal(size=(points, sizes[0]))
    targets = rng.uniform(size=(points, sizes[-1]))
    found = gradients(model, inputs, targets)
    worst = 0.0
    checked = 0
    for index, layer in enumerate(model):
        for name in ("weights", "bias"):
            values = layer[name]
            for position in np.ndindex(values.shape):
                original = values[position]
                values[position] = original + step
                high = loss(model, inputs, targets)
                values[position] = original - step
                low = loss(model, inputs, targets)
                values[position] = original
                measured = (high - low) / (2.0 * step)
                worst = max(worst, abs(measured
                                       - found[index][name][position]))
                checked += 1
    return {"largest difference": worst, "parameters checked": checked,
            "step": step}


def learn_xor(hidden=4, steps=4000, rate=2.0, seed=0):
    """Lernt das exklusive Oder, mit und ohne verborgene Schicht.

    Ohne verborgene Schicht ist das Netz eine einzige Trennlinie, und
    XOR lässt sich durch keine Gerade trennen. Das ist der Einwand, der
    die Forschung an Netzen einmal für Jahre angehalten hat, und er ist
    richtig; falsch war nur die Folgerung, dass es dabei bleibt.

    Args:
        hidden: die Grösse der verborgenen Schicht, null für keine.
        steps: die Anzahl der Schritte.
        rate: die Schrittweite.
        seed: der Startwert.

    Returns:
        Abbildung mit dem Fehler und der Zahl der richtigen Antworten.

    Raises:
        ValueError: bei einer negativen Grösse oder Schrittzahl.
    """
    if hidden < 0 or steps <= 0:
        raise ValueError("unzulässige Angaben")
    inputs = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    targets = np.array([[0.0], [1.0], [1.0], [0.0]])
    sizes = [2, 1] if hidden == 0 else [2, hidden, 1]
    model = build(sizes, seed=seed, scale=2.0)
    for _ in range(steps):
        found = gradients(model, inputs, targets)
        for layer, change in zip(model, found):
            layer["weights"] -= rate * change["weights"]
            layer["bias"] -= rate * change["bias"]
    got = forward(model, inputs)["output"]
    correct = int(np.sum((got > 0.5) == (targets > 0.5)))
    return {"hidden": hidden, "error": loss(model, inputs, targets),
            "correct": correct, "outputs": [round(float(value), 3)
                                            for value in got.reshape(-1)]}


def deep_gradients(depth=8, width=6, seed=0):
    """Misst, wie der Gradient in die Tiefe hin verschwindet.

    Die Ableitung der logistischen Funktion ist höchstens ein Viertel.
    In einem Netz mit acht Schichten wird der Fehler also achtmal mit
    etwas kleiner als einem Viertel multipliziert, bis er vorne
    ankommt. Die vorderen Schichten lernen dann praktisch nicht mehr,
    und das ist der Grund, warum tiefe Netze andere Aktivierungen
    verwenden.

    Returns:
        Abbildung mit der Grösse des Gradienten je Schicht.
    """
    rng = np.random.default_rng(seed)
    model = build([width] * (depth + 1), seed=seed)
    inputs = rng.normal(size=(20, width))
    targets = rng.uniform(size=(20, width))
    found = gradients(model, inputs, targets)
    sizes = [float(np.abs(layer["weights"]).mean()) for layer in found]
    return {"per layer": sizes, "first layer": sizes[0],
            "last layer": sizes[-1],
            "ratio": sizes[-1] / sizes[0] if sizes[0] > 0 else float("inf"),
            "why": "die Ableitung der logistischen Funktion ist "
                   "höchstens ein Viertel"}


def what_the_output_layer_has_to_match():
    """Nennt die Zuordnung von Ausgabe, Verteilung und Fehlermass.

    Die Folie stellt sie in einer Tabelle zusammen, und ihr Sinn ist,
    dass die Ausgabefunktion zum Wertebereich der Zielgrösse passen
    muss. Ein Sigmoid mit Ausgaben zwischen null und eins kann keine
    Zielgrösse vorhersagen, die auch grösser werden kann, und eine
    lineare Ausgabe kann keine Wahrscheinlichkeit garantieren.
    """
    return {"binär": ("Sigmoid", "Bernoulli", "binäre Kreuzentropie"),
            "kategorial": ("Softmax", "Multinoulli",
                           "diskrete Kreuzentropie"),
            "stetig": ("linear", "Gauss", "quadratischer Fehler"),
            "the rule": "die Ausgabefunktion muss zum Wertebereich der "
                        "Zielgrösse passen"}
