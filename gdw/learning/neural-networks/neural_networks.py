"""Neural networks: the boundary a layer can draw.

A single neuron computes a weighted sum and a threshold, so it draws a line
and can learn anything a line separates. The exclusive or is the standard
counterexample, and the perceptron rule never converges on it, which the
module demonstrates rather than asserts.

A hidden layer fixes it, and only because the activation is not linear:
composing linear maps gives a linear map, so a network of linear layers is a
single layer however deep it is. That is the whole reason for the activation
function.
"""

import math
import random


def perceptron(examples, steps=2000, rate=0.1):
    """The perceptron rule, reporting whether it converged."""
    weights = [0.0] * len(examples[0][0])
    bias = 0.0
    for _ in range(steps):
        errors = 0
        for features, label in examples:
            score = sum(weight * value
                        for weight, value in zip(weights, features)) + bias
            predicted = 1 if score > 0 else 0
            if predicted != label:
                errors += 1
                change = rate * (label - predicted)
                weights = [weight + change * value
                           for weight, value in zip(weights, features)]
                bias += change
        if errors == 0:
            return {"converged": True, "weights": weights, "bias": bias}
    return {"converged": False, "weights": weights, "bias": bias}


def two_layer_xor(seed=0, steps=20000, rate=0.5):
    """A network with one hidden layer trained on the exclusive or."""
    generator = random.Random(seed)
    examples = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
    hidden = [[generator.uniform(-1, 1) for _ in range(3)] for _ in range(2)]
    output = [generator.uniform(-1, 1) for _ in range(3)]
    for _ in range(steps):
        for features, label in examples:
            activations = [_sigmoid(row[0] * features[0] + row[1] * features[1]
                                    + row[2]) for row in hidden]
            prediction = _sigmoid(output[0] * activations[0]
                                  + output[1] * activations[1] + output[2])
            error = label - prediction
            delta = error * prediction * (1 - prediction)
            for index in range(2):
                inner = delta * output[index] * activations[index] \
                    * (1 - activations[index])
                hidden[index][0] += rate * inner * features[0]
                hidden[index][1] += rate * inner * features[1]
                hidden[index][2] += rate * inner
            output[0] += rate * delta * activations[0]
            output[1] += rate * delta * activations[1]
            output[2] += rate * delta
    correct = 0
    for features, label in examples:
        activations = [_sigmoid(row[0] * features[0] + row[1] * features[1]
                                + row[2]) for row in hidden]
        prediction = _sigmoid(output[0] * activations[0]
                              + output[1] * activations[1] + output[2])
        correct += int((prediction > 0.5) == bool(label))
    return {"accuracy": correct / len(examples)}


def _sigmoid(value):
    """The logistic activation."""
    return 1 / (1 + math.exp(-max(-60.0, min(60.0, value))))


def linear_layers_collapse():
    """Whether stacking linear layers gives anything a single layer cannot.

    Composing two linear maps gives a linear map, so the answer is no, and
    the module checks it numerically by comparing a two-layer linear network
    with the single layer that has the product of the matrices.
    """
    first = [[2.0, 1.0], [0.5, -1.0]]
    second = [[1.0, 3.0]]
    combined = [[sum(second[0][index] * first[index][column]
                     for index in range(2)) for column in range(2)]]
    for point in ((1.0, 0.0), (0.0, 1.0), (2.0, -3.0)):
        hidden = [sum(row[index] * point[index] for index in range(2))
                  for row in first]
        stacked = sum(second[0][index] * hidden[index] for index in range(2))
        direct = sum(combined[0][index] * point[index] for index in range(2))
        if abs(stacked - direct) > 1e-9:
            return False
    return True


def vanishing_gradient(depth):
    """How much of the gradient survives a stack of saturating activations.

    The derivative of the logistic function is at most a quarter, so the
    gradient is multiplied by at most that at every layer and falls
    exponentially with the depth. That is why deep networks needed a
    different activation before they could be trained.
    """
    shallow = 0.25 ** 2
    deep = 0.25 ** depth
    return {"shallow": shallow, "deep": deep, "ratio": deep / shallow}
