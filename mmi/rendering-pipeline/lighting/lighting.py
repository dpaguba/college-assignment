"""Local illumination: how bright is this point, given these lights.

Local means the model looks only at the point, the light and the camera. It
knows nothing about the rest of the scene, so it cannot produce shadows or
reflections; those need [ray-tracing](../ray-tracing/) or a separate pass. What
it buys is that the cost is constant per pixel, which is why it ran the whole
of real-time graphics for thirty years.

The Phong model is a sum of three terms with no physical derivation behind it:
ambient for what the model cannot compute, diffuse for the part that scatters
equally in all directions, specular for the highlight.
"""

from __future__ import annotations

import math


def dot(a, b):
    """Dot product of two 3-vectors."""
    return sum(x * y for x, y in zip(a, b))


def normalise(vector):
    """Scale a vector to unit length."""
    length = math.sqrt(dot(vector, vector))
    if length < 1e-12:
        return (0.0, 0.0, 0.0)
    return tuple(component / length for component in vector)


def subtract(a, b):
    """Componentwise difference of two 3-vectors."""
    return tuple(x - y for x, y in zip(a, b))


def scale(vector, factor):
    """Multiply a vector by a scalar."""
    return tuple(component * factor for component in vector)


def add(*vectors):
    """Componentwise sum of any number of 3-vectors."""
    return tuple(sum(components) for components in zip(*vectors))


def reflect(incident, normal):
    """Mirror a direction about a normal: `d - 2 (d.n) n`.

    Both the specular term and the reflection ray in a ray tracer use this, and
    it is the one piece of the lighting model that is genuinely physical.
    """
    return subtract(incident, scale(normal, 2 * dot(incident, normal)))


def lambert(normal, light_direction):
    """Diffuse reflection: brightness falls off with the cosine of the angle.

    A rough surface scatters light equally in every direction, so the viewer's
    position does not matter. What does matter is how obliquely the light
    arrives: a beam hitting at an angle spreads its energy over a larger patch,
    and the cosine is exactly that spreading factor.

    Negative values mean the light is behind the surface, and are clamped to
    zero rather than allowed to darken the result.
    """
    return max(0.0, dot(normal, light_direction))


def phong_specular(normal, light_direction, view_direction, shininess):
    """Highlight from the angle between the reflected light and the viewer.

    Not derived from anything, just a function that peaks when the viewer is
    aligned with the mirror direction and falls off at a rate the exponent
    controls. Higher shininess gives a smaller, sharper highlight, which reads
    as a smoother surface.
    """
    mirrored = reflect(scale(light_direction, -1), normal)
    return max(0.0, dot(mirrored, view_direction)) ** shininess


def blinn_specular(normal, light_direction, view_direction, shininess):
    """Highlight from the half vector, the cheaper and better-behaved variant.

    The half vector bisects the light and view directions, and the highlight
    uses its angle to the normal. It avoids the reflection computation, and for
    a distant light and a distant viewer the half vector is constant over the
    whole surface, so it can be computed once per light rather than per pixel.

    At grazing angles the two differ visibly in shape. The Phong highlight
    stays radially symmetric no matter how oblique the view; the Blinn
    highlight stretches out along the surface, which is what a real rough
    surface does and the reason the substitution stuck.

    The exponents are not comparable between the two: the half-vector angle is
    roughly half the reflection angle, so matching a Phong highlight needs
    about four times the exponent.
    """
    half = normalise(add(light_direction, view_direction))
    return max(0.0, dot(normal, half)) ** shininess


def attenuation(distance, constant=1.0, linear=0.0, quadratic=0.0):
    """How light weakens with distance: `1 / (c + l d + q d^2)`.

    Physically only the quadratic term is real, since a point light spreads its
    energy over a sphere whose area grows with the square. The other two are
    there to be tuned, because the pure inverse square blows up next to the
    light and dies too fast further away, once tone mapping is involved.
    """
    return 1.0 / (constant + linear * distance + quadratic * distance * distance)


def phong(point, normal, camera, light, material, model="blinn"):
    """The full Phong illumination model for one point and one light.

    The material carries ambient, diffuse and specular coefficients plus a
    shininess. The light carries a position and an intensity. Each of the three
    terms is computed independently and summed, which is the model's strength
    (each is separately tunable) and its weakness (nothing conserves energy, so
    a surface can reflect more than it receives).
    """
    normal = normalise(normal)
    to_light = subtract(light["position"], point)
    distance = math.sqrt(dot(to_light, to_light))
    light_direction = normalise(to_light)
    view_direction = normalise(subtract(camera, point))

    falloff = attenuation(distance, *light.get("attenuation", (1.0, 0.0, 0.0)))
    intensity = light.get("intensity", 1.0) * falloff

    ambient = material["ambient"]
    diffuse = material["diffuse"] * lambert(normal, light_direction) * intensity

    if lambert(normal, light_direction) <= 0.0:
        specular = 0.0
    elif model == "phong":
        specular = material["specular"] * intensity * phong_specular(
            normal, light_direction, view_direction, material["shininess"])
    else:
        specular = material["specular"] * intensity * blinn_specular(
            normal, light_direction, view_direction, material["shininess"])

    return ambient + diffuse + specular


def flat_shade(vertices, normal, camera, light, material):
    """One colour for the whole face, computed at its centroid.

    Cheapest, and it makes the faceting visible, which is correct for a cube and
    wrong for a sphere approximated by polygons.
    """
    centroid = scale(add(*vertices), 1 / len(vertices))
    return phong(centroid, normal, camera, light, material)


def gouraud_shade(vertices, normals, weights, camera, light, material):
    """Shade at the vertices, then interpolate the results across the face.

    Three lighting computations per triangle instead of one per pixel, which is
    why it was the standard when pixels were expensive. It fails on exactly one
    thing: a highlight smaller than a triangle falls between the vertices, so
    it either disappears entirely or smears across the whole face as the object
    turns.
    """
    intensities = [phong(vertex, normal, camera, light, material)
                   for vertex, normal in zip(vertices, normals)]
    return sum(weight * value for weight, value in zip(weights, intensities))


def phong_shade(vertices, normals, weights, camera, light, material):
    """Interpolate the normals across the face, then shade at each pixel.

    Interpolating a normal does not preserve its length, so it has to be
    renormalised, and that is the whole extra cost over Gouraud besides the
    per-pixel lighting itself. In return the highlight lands wherever the
    geometry puts it, regardless of how coarse the mesh is.
    """
    point = tuple(sum(weight * vertex[axis] for weight, vertex in zip(weights, vertices))
                  for axis in range(3))
    normal = normalise(tuple(sum(weight * n[axis] for weight, n in zip(weights, normals))
                             for axis in range(3)))
    return phong(point, normal, camera, light, material)


def face_normal(a, b, c):
    """Normal of a triangle from the cross product of two of its edges.

    The direction depends on the vertex order, which is how a renderer knows
    which side of a face is the outside, and hence which faces to cull.
    """
    u, v = subtract(b, a), subtract(c, a)
    return normalise((u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]))
