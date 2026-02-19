"""Ray tracing: following light backwards from the eye.

Rasterisation asks, for each triangle, which pixels it covers. Ray tracing asks
the transposed question: for each pixel, which surface is there. The loops swap
places, and with them everything else.

Because a ray can be cast from any point in any direction, shadows, mirrors and
refraction are all the same operation applied again from a new origin. That is
the whole reason to pay the cost: in a rasteriser each of those is a separate
mechanism with its own approximation.
"""

from __future__ import annotations

import math

EPSILON = 1e-9


def dot(a, b):
    """Dot product of two 3-vectors."""
    return sum(x * y for x, y in zip(a, b))


def subtract(a, b):
    """Componentwise difference of two 3-vectors."""
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    """Componentwise sum of two 3-vectors."""
    return tuple(x + y for x, y in zip(a, b))


def scale(vector, factor):
    """Multiply a vector by a scalar."""
    return tuple(component * factor for component in vector)


def cross(a, b):
    """Cross product of two 3-vectors."""
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def normalise(vector):
    """Scale a vector to unit length."""
    length = math.sqrt(dot(vector, vector))
    return tuple(component / length for component in vector)


def at(origin, direction, t):
    """The point at parameter `t` along a ray."""
    return add(origin, scale(direction, t))


def intersect_plane(origin, direction, normal, offset):
    """Where a ray meets a plane, or `None` if it runs parallel to it.

    One dot product and one division. The denominator vanishing means the ray
    is parallel; if the numerator vanishes too the ray lies in the plane, which
    is treated as a miss because there is no single intersection point.
    """
    denominator = dot(normal, direction)
    if abs(denominator) < EPSILON:
        return None
    t = (offset - dot(normal, origin)) / denominator
    return t if t > EPSILON else None


def intersect_sphere(origin, direction, centre, radius):
    """Where a ray meets a sphere, as the nearer positive root.

    Substituting the ray into the sphere equation gives a quadratic in `t`. The
    discriminant decides: negative for a miss, zero for a grazing touch, and
    positive for the two crossings. Returning the smaller positive root is what
    makes the camera see the front of the sphere rather than the inside of its
    back.
    """
    to_centre = subtract(origin, centre)
    b = 2 * dot(direction, to_centre)
    c = dot(to_centre, to_centre) - radius * radius
    a = dot(direction, direction)

    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return None

    root = math.sqrt(discriminant)
    for t in ((-b - root) / (2 * a), (-b + root) / (2 * a)):
        if t > EPSILON:
            return t
    return None


def intersect_triangle(origin, direction, a, b, c):
    """Moller-Trumbore: intersection and barycentric coordinates at once.

    Solving for the ray parameter and the two barycentric coordinates
    simultaneously by Cramer's rule. It never builds the plane of the triangle,
    so it needs no per-triangle storage, and the barycentric coordinates it
    produces are needed anyway to interpolate normals and texture coordinates.

    Returns `(t, u, v)`, with the weights of the vertices being
    `(1 - u - v, u, v)`.
    """
    edge1, edge2 = subtract(b, a), subtract(c, a)
    pvec = cross(direction, edge2)
    determinant = dot(edge1, pvec)

    if abs(determinant) < EPSILON:
        return None

    inverse = 1.0 / determinant
    tvec = subtract(origin, a)
    u = dot(tvec, pvec) * inverse
    if u < 0.0 or u > 1.0:
        return None

    qvec = cross(tvec, edge1)
    v = dot(direction, qvec) * inverse
    if v < 0.0 or u + v > 1.0:
        return None

    t = dot(edge2, qvec) * inverse
    return (t, u, v) if t > EPSILON else None


def intersect_box(origin, direction, minimum, maximum):
    """Slab test against an axis-aligned box, the workhorse of every accelerator.

    Each axis gives an interval of `t` during which the ray is between that
    pair of planes. The ray hits the box exactly when all three intervals
    overlap, so the test is three divisions and a running intersection, with no
    branching on which face is hit.

    Bounding volume hierarchies are built out of this test alone: it is not
    used to draw anything, only to discard most of the scene per ray.
    """
    enter, leave = -math.inf, math.inf

    for axis in range(3):
        if abs(direction[axis]) < EPSILON:
            if origin[axis] < minimum[axis] or origin[axis] > maximum[axis]:
                return None
            continue
        inverse = 1.0 / direction[axis]
        first = (minimum[axis] - origin[axis]) * inverse
        second = (maximum[axis] - origin[axis]) * inverse
        if first > second:
            first, second = second, first
        enter, leave = max(enter, first), min(leave, second)
        if enter > leave:
            return None

    return enter if enter > EPSILON else (leave if leave > EPSILON else None)


def reflect(direction, normal):
    """Mirror a direction about a normal."""
    return subtract(direction, scale(normal, 2 * dot(direction, normal)))


def refract(direction, normal, eta_from, eta_to):
    """Bend a direction through a boundary by Snell's law, or return `None`.

    `None` means total internal reflection: going from dense to thin past the
    critical angle, the sine the law demands exceeds one and no refracted ray
    exists. That is why the underside of a water surface is a mirror beyond
    about 49 degrees, and a ray tracer gets that effect for free rather than
    having to special-case it.
    """
    ratio = eta_from / eta_to
    cosine = -dot(normal, direction)
    sine_squared = ratio * ratio * (1.0 - cosine * cosine)

    if sine_squared > 1.0:
        return None

    return add(scale(direction, ratio),
               scale(normal, ratio * cosine - math.sqrt(1.0 - sine_squared)))


def fresnel(cosine, eta_from, eta_to):
    """Schlick's approximation of how much light reflects instead of refracting.

    The exact Fresnel equations need the polarisation; Schlick's fit costs one
    fifth power and is within a percent of them. What it captures is the effect
    that matters visually: glass seen face on is nearly transparent, and seen
    at a glancing angle is nearly a mirror.
    """
    reflectance = ((eta_from - eta_to) / (eta_from + eta_to)) ** 2
    return reflectance + (1 - reflectance) * (1 - cosine) ** 5


def trace(origin, direction, spheres, lights, depth=3, ambient=0.05):
    """Cast one ray and return the light coming back along it.

    Each hit contributes local shading, a shadow test per light, and one
    reflected ray if the surface reflects. The recursion is what a rasteriser
    cannot do: the reflected ray is an ordinary ray, cast from the hit point,
    and answering it requires the same search over the whole scene again.

    Cost grows with the number of rays, so depth is capped rather than run to
    convergence. Two bounces are usually indistinguishable from ten.
    """
    if depth <= 0:
        return 0.0

    nearest, hit = math.inf, None
    for sphere in spheres:
        t = intersect_sphere(origin, direction, sphere["centre"], sphere["radius"])
        if t is not None and t < nearest:
            nearest, hit = t, sphere

    if hit is None:
        return 0.0

    point = at(origin, direction, nearest)
    normal = normalise(subtract(point, hit["centre"]))
    colour = ambient * hit.get("diffuse", 1.0)

    for light in lights:
        to_light = subtract(light["position"], point)
        distance = math.sqrt(dot(to_light, to_light))
        light_direction = scale(to_light, 1 / distance)

        if in_shadow(add(point, scale(normal, 1e-6)), light_direction, distance, spheres):
            continue

        lambert = max(0.0, dot(normal, light_direction))
        colour += hit.get("diffuse", 1.0) * lambert * light.get("intensity", 1.0)

    if hit.get("reflective", 0.0) > 0.0:
        bounced = reflect(direction, normal)
        colour += hit["reflective"] * trace(add(point, scale(normal, 1e-6)),
                                            bounced, spheres, lights, depth - 1, ambient)

    return colour


def in_shadow(origin, direction, distance, spheres):
    """Whether anything blocks the straight path to a light.

    A shadow ray, and the reason ray traced shadows are exact rather than
    approximated: the question "is there something between here and the light"
    is answered by asking it, not by rendering a depth map from the light and
    comparing.

    The origin is offset along the normal by a small amount. Without that, the
    surface finds itself at `t` near zero and shadows itself, which produces
    the speckled pattern known as shadow acne.
    """
    for sphere in spheres:
        t = intersect_sphere(origin, direction, sphere["centre"], sphere["radius"])
        if t is not None and t < distance:
            return True
    return False


def render(width, height, camera, spheres, lights, fov=math.pi / 3, depth=3):
    """Cast one ray per pixel through the image plane.

    The loop is over pixels, not over objects, and every pixel is independent,
    which is why ray tracing parallelises perfectly and why it took dedicated
    hardware rather than cleverness to make it real time.
    """
    aspect = width / height
    scale_factor = math.tan(fov / 2)
    image = []

    for y in range(height):
        row = []
        for x in range(width):
            ndc_x = (2 * (x + 0.5) / width - 1) * aspect * scale_factor
            ndc_y = (1 - 2 * (y + 0.5) / height) * scale_factor
            direction = normalise((ndc_x, ndc_y, -1.0))
            row.append(trace(camera, direction, spheres, lights, depth))
        image.append(row)

    return image
