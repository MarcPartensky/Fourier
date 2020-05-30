from math import pi, sqrt, cos, sin
from cmath import polar
from mytools import timer

import itertools
import mycolors
import random
import math
import copy

average = mean = lambda x: sum(x) / len(x)

digits = 2  # Number of digits of precision of the objects when displayed


class Point:
    """Representation of a point that can be displayed on screen."""

    @classmethod
    def sum(cls, points, **kwargs):
        """Return the points which components are the respectives sums of the
        components of the given points."""
        p = Point.null(**kwargs)
        for point in points:
            p += point
        return p

    @classmethod
    def average(cls, points):
        """Return the point which position is the average of
        the position of the given points"""
        return Point.sum(points) / len(points)

    @classmethod
    def origin(cls, d=2, **kwargs):
        """Return the origin."""
        return cls([0 for i in range(d)], **kwargs)

    null = neutral = zero = origin

    @classmethod
    def random(cls, d=2, borns=[-1, 1], **kwargs):
        """Create a random point using optional minimum and maximum."""
        components = [random.uniform(*borns) for i in range(d)]
        return cls(*components, **kwargs)

    @staticmethod
    def distance(p1, p2):
        """Return the distance between the two points."""
        return math.hypot(p1.x-p2.x, p1.y-p2.y)

    @staticmethod
    def turnPoints(angles, points):
        """Turn the points around themselves."""
        l = len(points)
        for i in range(l - 1):
            points[i].turn(angles[i], points[i + 1:])

    @staticmethod
    def showPoints(surface, points):
        """Show the points on the surface."""
        for point in points:
            point.show(surface)

    @staticmethod
    def closest(point, points):
        """Return the point of the list of points that is the closest to the given point."""
        pts = [(Point.distance(point, p), p) for p in points]
        pts.sort()
        return pts[0][1]

    @staticmethod
    def farthest(point, points):
        """Return the point of the list of points that is the farthest to the given point."""
        # print(point)
        pts = [(Point.distance(point, p), p) for p in points]
        pts.sort()
        # print(" ".join(map(lambda pt: str(pt[0])[:5]+","+str(pt[1]), pts)))
        return pts[-1][1]

    @classmethod
    def createFromVector(cls, vector):
        """Create a point from a vector."""
        return cls(vector.x, vector.y)

    def __init__(self, *components, mode=0, size=[0.1, 0.1], width=1, radius=0.02, fill=False, color=mycolors.WHITE,
                 conversion=True):
        """Create a point using its components and optional radius, fill, color and conversion."""
        if components != ():
            if type(components[0]) == list:
                components = components[0]
        self.components = list(components)
        self.mode = mode
        self.size = size
        self.width = width
        self.radius = radius
        self.fill = fill
        self.color = color
        self.conversion = conversion

    def __hash__(self):
        """Return a single number using the hash of its attributes."""
        hash(self.components)

    def set(self, point):
        """Set the components of the point to the components of an other given point."""
        self.components = [c for c in point]

    def __len__(self):
        """Return the number of components of the point."""
        return len(self.components)

    def setX(self, value):
        """Set the x component."""
        self.components[0] = value

    def getX(self):
        """Return the x component."""
        return self.components[0]

    def delX(self):
        """Delete the x component and so shifting to a new one."""
        del self.components[0]

    def setY(self, value):
        """Set the y component."""
        self.components[1] = value

    def getY(self):
        """Return the y component."""
        return self.components[1]

    def delY(self):
        """Delete the y component."""
        del self.components[1]

    x = property(getX, setX, delX, "Allow the user to manipulate the x component easily.")
    y = property(getY, setY, delY, "Allow the user to manipulate the y component easily.")

    def __eq__(self, other):
        """Determine if two points are equals by comparing its components."""
        return abs(self - other) < 10e-10

    def __ne__(self, other):
        """Determine if two points are unequals by comparing its components."""
        return tuple(self) != tuple(other)

    def __rmul__(self, r):
        """Multiplication by a scalar like vectors."""
        return Point(*[r * c for c in self.components])

    def __truediv__(self, r):
        """Divide a points by a scalar."""
        return Point(*[c / r for c in self.components])

    def __contains__(self, other):
        """Determine if an object is in the point."""
        x, y = other
        return self.radius >= sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def __getitem__(self, index):
        """Return x or y value using given index."""
        return self.components[index]

    def __setitem__(self, index, value):
        """Change x or y value using given index and value."""
        self.components[index] = value

    def __abs__(self):
        """Return the distance of the point to the origin."""
        return Vector.createFromPoint(self).norm

    def __tuple__(self):
        """Return the components in tuple form."""
        return tuple(self.components)

    def __list__(self):
        """Return the components."""
        return self.components

    def rotate(self, angle=pi, point=None):
        """Rotate the point using the angle and the center of rotation.
        Uses the origin for the center of rotation by default."""
        if not point: point = Point.origin(d=self.dimension)
        v = Vector.createFromTwoPoints(point, self)
        v.rotate(angle)
        self.components = v(point).components

    def turn(self, angle=pi, points=[]):
        """Turn the points around itself."""
        for point in points:
            point.rotate(angle, self)

    def move(self, *step):
        """Move the point using given step."""
        self.x += step[0]
        self.y += step[1]

    def around(self, point, distance):
        """Determine if a given point is in a radius 'distance' of the point."""
        return self.distance(point) <= distance

    def showCross(self, window, color=None, size=None, width=None, conversion=None):
        """Show the point under the form of a cross using the window."""
        if not color: color = self.color
        if not size: size = self.size
        if not width: width = self.width
        if not conversion: conversion = self.conversion
        x, y = self
        sx, sy = size
        xmin = x - sx / 2
        ymin = y - sy / 2
        xmax = x + sx / 2
        ymax = y + sy / 2
        window.draw.line(window.screen, color, [xmin, ymin], [xmax, ymax], width, conversion)
        window.draw.line(window.screen, color, [xmin, ymax], [xmax, ymin], width, conversion)

    def showCircle(self, window, color=None, radius=None, fill=None, conversion=None):
        """Show a point under the form of a circle using the window."""
        if not color: color = self.color
        if not radius: radius = self.radius
        if not fill: fill = self.fill
        if not conversion: conversion = self.conversion
        window.draw.circle(window.screen, color, [self.x, self.y], radius, fill, conversion)

    def show(self, window, color=None, mode=None, fill=None, radius=None, size=None, width=None, conversion=None):
        """Show the point on the window."""
        if not mode: mode = self.mode
        if mode == 0 or mode == "circle":
            self.showCircle(window, color, radius, fill, conversion)
        if mode == 1 or mode == "cross":
            self.showCross(window, color, size, width, conversion)

    def showText(self, context, text, size=1, color=mycolors.WHITE, conversion=True):
        """Show the text next to the point on the window."""
        context.print(text, self.components, size, color=color, conversion=conversion)

    def __add__(self, other):
        """Add two points."""
        return Point([c1 + c2 for (c1, c2) in zip(self, other)])

    def __iadd__(self, other):
        """Add a point to the actual point."""
        self.components = [c1 + c2 for (c1, c2) in zip(self, other)]
        return self

    __radd__ = __add__

    def __sub__(self, other):
        """Add a point to the actual point."""
        return Point([c1 - c2 for (c1, c2) in zip(self, other)])

    def __isub__(self, other):
        """Add a point to the actual point."""
        self.components = [c1 - c2 for (c1, c2) in zip(self, other)]
        return self

    __rsub__ = __sub__

    def __sub__(self, other):
        """Substract the components of 2 objects."""
        return Point(self.x - other[0], self.y - other[1])

    def __ge__(self, other):
        """Determine if a point is farther to the origin."""
        return self.x ** 2 + self.y ** 2 >= other.x ** 2 + other.y ** 2

    def __gt__(self, other):
        """Determine if a point is farther to the origin."""
        return self.x ** 2 + self.y ** 2 > other.x ** 2 + other.y ** 2

    def __le__(self, other):
        """Determine if a point is the nearest to the origin."""
        return self.x ** 2 + self.y ** 2 <= other.x ** 2 + other.y ** 2

    def __lt__(self, other):
        """Determine if a point is the nearest to the origin."""
        return self.x ** 2 + self.y ** 2 < other.x ** 2 + other.y ** 2

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < len(self.components):
            self.iterator += 1
            return self.components[self.iterator - 1]
        else:
            raise StopIteration

    def truncate(self):
        """Truncate the position of the point by making the x and y components integers."""
        for i in range(self.dimension):
            self.components[i] = int(self.components[i])

    def __str__(self):
        """Return the string representation of a point."""
        return "p(" + ",".join([str(round(c, digits)) for c in self.components]) + ")"

    def getPosition(self):
        """Return the components."""
        return self.components

    def setPosition(self, position):
        """Set the components."""
        self.components = position

    def getDimension(self):
        """Return the dimension of the point."""
        return len(self.components)

    def setDimension(self, dimension):
        """Set the dimension of the point by setting to 0 the new components."""
        self.components = self.components[:dimension]
        self.components += [0 for i in range(dimension - len(self.components))]

    def delDimension(self):
        """Delete the components of the points."""
        self.components = []

    position = property(getPosition, setPosition, "Same as component although only component should be used.")
    dimension = property(getDimension, setDimension, delDimension,
                         "Representation of the dimension point which is the length of the components.")


class Direction:
    """Base class of lines and segments."""
    pass


class Vector:
    @classmethod
    def null(cls, d=2):
        """Return the null vector."""
        return cls(*[0 for i in range(d)])

    neutral = zero = null

    @classmethod
    def random(cls, d=2, borns=[-1, 1], **kwargs):
        """Create a random vector using optional min and max."""
        components = [random.uniform(*borns) for i in range(d)]
        return cls(*components, **kwargs)

    @classmethod
    def sum(cls, vectors):
        """Return the vector that correspond to the sum of all the vectors."""
        result = cls.null()
        for vector in vectors:
            result += vector
        return result

    @classmethod
    def average(cls, vectors):
        """Return the vector that correspond to the mean of all the vectors."""
        return cls.sum(vectors) / len(vectors)

    mean = average

    @classmethod
    def collinear(cls, *vectors, e=10e-10):
        """Determine if all the vectors are colinear."""
        l = len(vectors)
        if l == 2:
            v1 = vectors[0]
            v2 = vectors[1]
            return abs(v1.x * v2.y - v1.y - v2.x) < e
        else:
            for i in range(l):
                for j in range(i + 1, l):
                    if not cls.collinear(vectors[i], vectors[j]):
                        return False
            return True

    @classmethod
    def sameDirection(cls, *vectors, e=10e-10):
        """Determine if all the vectors are in the same direction."""
        l = len(vectors)
        if l == 2:
            v1 = vectors[0]
            v2 = vectors[1]
            return (abs(v1.angle - v2.angle) % (2 * math.pi)) < e
        else:
            for i in range(l):
                for j in range(i + 1, l):
                    if not cls.sameDirection(vectors[i], vectors[j]):
                        return False
            return True

    @classmethod
    def createFromPolar(cls, norm, angle, **kwargs):
        """Create a vector using norm and angle from polar coordonnates."""
        x, y = cls.cartesian([norm, angle])
        return cls(x, y, **kwargs)

    @classmethod
    def createFromSegment(cls, segment, **kwargs):
        """Create a vector from a segment."""
        return cls.createFromTwoPoints(segment.p1, segment.p2, **kwargs)

    @classmethod
    def createFromTwoPoints(cls, point1, point2, **kwargs):
        """Create a vector from 2 points."""
        return cls([c2 - c1 for (c1, c2) in zip(point1, point2)], **kwargs)

    @classmethod
    def createFromTwoTuples(cls, tuple1, tuple2, **kwargs):
        """Create a vector from 2 tuples."""
        return cls([c2 - c1 for (c1, c2) in zip(tuple1, tuple2)], **kwargs)

    @classmethod
    def createFromPoint(cls, point, **kwargs):
        """Create a vector from a single point."""
        return cls(point.x, point.y, **kwargs)

    @classmethod
    def createFromLine(cls, line, **kwargs):
        """Create a vector from a line."""
        angle = line.angle
        x, y = cls.cartesian([1, angle])
        return cls(x, y, **kwargs)

    @staticmethod
    def polar(position):
        """Return the polar position [norm,angle] using cartesian position [x,y]."""
        return list(polar(complex(position[0], position[1])))

    @staticmethod
    def cartesian(position):
        """Return the cartesian position [x,y] using polar position [norm,angle]."""
        return [position[0] * cos(position[1]), position[0] * sin(position[1])]

    def __init__(self, *components, color=mycolors.WHITE, width=1, arrow=[0.1, 0.5]):
        """Create a vector."""
        if components:
            if isinstance(components[0], list):
                components = components[0]
        self.components = list(components)
        self.color = color
        self.width = width
        self.arrow = arrow

    def set(self, v):
        """Set a vector to the values of another without changing its color, with or arrow."""
        self.components = v.components

    def setNull(self):
        """Set the components of the vector to zero."""
        self.components = [0 for i in range(len(self.components))]

    # X component
    def setX(self, value):
        """Set the x component."""
        self.components[0] = value

    def getX(self):
        """Return the x component."""
        return self.components[0]

    def delX(self):
        """Delete the x component and so shifting to a new one."""
        del self.components[0]

    # Y component
    def setY(self, value):
        """Set the y component."""
        self.components[1] = value

    def getY(self):
        """Return the y component."""
        return self.components[1]

    def delY(self):
        """Delete the y component."""
        del self.components[1]

    # Angle
    def getAngle(self):
        """Return the angle of a vector in polar coordinates."""
        x, y = self.components
        return math.atan2(y, x)

    def setAngle(self, value):
        """Change the angle of the points without changing its norm."""
        n, a = Vector.polar(self.components)
        self.components = Vector.cartesian([n, value])

    def delAngle(self):
        """Set to zero the angle of the vector."""
        self.setAngle(0)

    # Norm
    def getNorm(self, norm=lambda l: (sum(map(lambda x: x ** 2, l))) ** (1 / 2)):
        """Return the euclidian norm of the vector by default."""
        return norm(self.components)

    def setNorm(self, value):
        """Change the angle of the points without changing its norm."""
        n, a = Vector.polar(self.components)
        self.components = Vector.cartesian([value, a])

    # Position
    def getPosition(self):
        """Return the components."""
        return self.components

    def setPosition(self, position):
        """Set the components."""
        self.components = position

    def delPosition(self):
        """Set the vector to the null vector."""
        self.components = [0 for i in range(len(self.components))]

    x = property(getX, setX, delX, doc="Allow the user to manipulate the x component easily.")
    y = property(getY, setY, delY, doc="Allow the user to manipulate the y component easily.")
    norm = property(getNorm, setNorm, doc="Allow the user to manipulate the norm of the vector easily.")
    angle = property(getAngle, setAngle, doc="Allow the user to manipulate the angle of the vector easily.")
    position = property(getPosition, setPosition, doc="Same as components.")

    def limit(self, n):
        """Limit the norm of the vector by n."""
        if self.norm > n:
            self.norm = n

    def show(self, context, p=Point.neutral(), color=None, width=None):
        """Show the vector."""
        if not color: color = self.color
        if not width: width = self.width
        q = self(p)
        v = -self * self.arrow[0]  # wtf
        v1 = v % self.arrow[1]
        v2 = v % -self.arrow[1]
        a = v1(q)
        b = v2(q)
        context.draw.line(context.screen, color, p.components, q.components, width)
        context.draw.line(context.screen, color, q.components, a.components, width)
        context.draw.line(context.screen, color, q.components, b.components, width)

    def showFromTuple(self, context, t=(0, 0), **kwargs):
        """Show a vector from a tuple."""
        p = Point(*t)
        self.show(context, p, **kwargs)

    def showText(self, surface, point, text, color=None, size=20):
        """Show the text next to the vector."""
        if not color: color = self.color
        v = self / 2
        point = v(point)
        surface.print(text, tuple(point), color=color, size=size)

    def __len__(self):
        """Return the number of components."""
        return len(self.components)

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < len(self.components):
            self.iterator += 1
            return self.components[self.iterator - 1]
        else:
            raise StopIteration

    def __neg__(self):
        """Return the negative vector."""
        return Vector([-c for c in self.components])

    def colinear(self, other, e=10e-10):
        """Return if two vectors are colinear."""
        return abs(self.x * other.y - self.y * other.x) < e

    __floordiv__ = colinear

    def scalar(self, other):
        """Return the scalar product between two vectors."""
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        """Determine if a vector crosses another using dot product."""
        return self.scalar(other) == 0

    def __mul__(self, factor):
        """Multiply a vector by a given factor."""
        if type(factor) == int or type(factor) == float:
            return Vector([c * factor for c in self.components])
        else:
            raise NotImplementedError
            raise Exception("Type " + str(type(factor)) + " is not valid. Expected float or int types.")

    __imul__ = __rmul__ = __mul__  # Allow front extern multiplication using back extern multiplication with scalars

    def __truediv__(self, factor):
        """Multiply a vector by a given factor."""
        if type(factor) == Vector:
            raise NotImplementedError
        else:
            return Vector([c / factor for c in self.components])

    def __itruediv__(self, factor):
        """Divide the components of a vector by a given factor."""
        self.components = [c / factor for c in self.components]
        return self

    def __add__(self, other):
        """Add two vector together."""
        return Vector([c1 + c2 for (c1, c2) in zip(self.components, other.components)])

    def __sub__(self, other):
        """Sub two vector together."""
        return Vector([c1 - c2 for (c1, c2) in zip(self.components, other.components)])

    def __iadd__(self, other):
        """Add a vector to another."""
        self.components = [c1 + c2 for (c1, c2) in zip(self.components, other.components)]
        return self

    def __isub__(self, other):
        """Substract a vector to another."""
        self.components = [c1 - c2 for (c1, c2) in zip(self.components, other.components)]
        return self

    __radd__ = __add__
    __rsub__ = __sub__

    def rotate(self, angle):
        """Rotate a vector using the angle of rotation."""
        n, a = Vector.polar([self.x, self.y])
        a += angle
        self.x = n * cos(a)
        self.y = n * sin(a)

    def __mod__(self, angle):
        """Return the rotated vector using the angle of rotation."""
        n, a = Vector.polar([self.x, self.y])
        a += angle
        return Vector(n * cos(a), n * sin(a), color=self.color, width=self.width, arrow=self.arrow)

    __imod__ = __mod__

    def __getitem__(self, index):
        """Return x or y value using given index."""
        return self.position[index]

    def __setitem__(self, index, value):
        """Change x or y value using given index and value."""
        self.position[index] = value

    def __call__(self, *points):
        """Return points by applying the vector on those."""
        if points != ():
            if type(points[0]) == list:
                points = points[0]
        if len(points) == 0:
            raise Exception("A vector can only be applied to a point or a list of points.")
        elif len(points) == 1:
            return points[0] + self
        else:
            return [point + self for point in points]

    def applyToPoint(self, point):
        """Return the point after applying the vector to it."""
        return self + point

    def applyToPoints(self, points):
        """Return the points after applying the vector to those."""
        return [point + self for point in points]

    def __xor__(self, other):
        """Return the angle between two vectors."""
        return self.angle - other.angle

    def __invert__(self):
        """Return the unit vector."""
        a = self.angle
        x, y = Vector.cartesian([1, a])
        return Vector(x, y)

    unit = property(__invert__)

    def __str__(self):
        """Return a string description of the vector."""
        return "v(" + ",".join([str(round(c, digits)) for c in self.components]) + ")"

    def __tuple__(self):
        """Return the components in tuple form."""
        return tuple(self.components)

    def __list__(self):
        """Return the components."""
        return self.components


class Segment(Direction):
    @classmethod
    def null(cls):
        """Return the segment whoose points are both the origin."""
        return cls(*[Point.origin() for i in range(2)])

    @classmethod
    def random(cls, d=2, borns=[-1, 1], **kwargs):
        """Create a random segment."""
        p1 = Point.random(d, borns)
        p2 = Point.random(d, borns)
        return cls(*[p1, p2], **kwargs)

    @classmethod
    def createFromTuples(cls, *tps, **kwargs):
        """Create a segment using tuples and optional arguments."""
        pts = [Point(*tp) for tp in tps]
        return cls(*pts, **kwargs)

    def __init__(self, *points, width=1, color=mycolors.WHITE, conversion=True):
        """Create the segment using 2 points, width and color."""
        if len(points) > 0:  # Extracting the points arguments under the same list format
            if type(points[0]) == list:
                points = points[0]
        if len(points) == 1: points = points[0]
        if len(points) != 2: raise Exception("A segment must have 2 points.")
        self.points = list(points)
        self.width = width
        self.color = color
        self.conversion = conversion

    def __str__(self):
        """Return the string representation of a segment."""
        return "s(" + str(self.p1) + "," + str(self.p2) + ")"

    def __call__(self, t=1 / 2):
        """Return the point C of the segment so that Segment(p1,C)=t*Segment(p1,p2)."""
        return (t * self.vector)(self.p1)

    def sample(self, n, include=True):
        """Sample n points of the segment.
        It is also possible to include the last point if wanted."""
        return [self(t / n) for t in range(n + int(include))]

    __rmul__ = __imul__ = __mul__ = lambda self, t: Segment(self.p1, self(t))

    def getCenter(self):
        """Return the center of the segment in the general case."""
        return Point.average(self.points)

    def setCenter(self, np):
        """Set the center of the segment."""
        p = self.getCenter()
        v = Vector.createFromTwoPoints(p, np)
        for i in range(len(self.points)):
            self.points[i] = v(self.points[i])

    def getAngle(self):
        """Return the angle of the segment."""
        return self.vector.angle

    def setAngle(self, angle):
        """Set the angle of the segment."""
        self.vector.angle = angle

    def show(self, context, color=None, width=None, conversion=None):
        """Show the segment using window."""
        if color is None:
            color = self.color
        if width is None:
            width = self.width
        if conversion is None:
            conversion = self.conversion
        context.draw.line(context.screen, color, self.p1, self.p2, width, conversion=conversion)

    def showInBorders(self, window, color=None, width=None):
        """Show the segment within the boundaries of the window."""
        # It it really slow and it doesn't work as expected.
        xmin, ymin, xmax, ymax = window.getCorners()
        p = [Point(xmin, ymin), Point(xmax, ymin), Point(xmax, ymax), Point(xmin, ymax)]
        f = Form(p)
        if (self.p1 in f) and (self.p2 in f):
            window.draw.line(window.screen, color, [self.p1.x, self.p1.y], [self.p2.x, self.p2.y], width)
        elif (self.p1 in f) and not (self.p2 in f):
            v = Vector.createFromTwoPoints(self.p1, self.p2)
            hl = HalfLine(self.p1, v.angle)
            p = f.crossHalfLine(hl)
            if p:
                print(len(p))
                p = p[0]
                window.draw.line(window.screen, color, [self.p1.x, self.p1.y], [p.x, p.y], width)
        elif not (self.p1 in f) and (self.p2 in f):
            v = Vector.createFromTwoPoints(self.p2, self.p1)
            hl = HalfLine(self.p2, v.angle)
            p = f.crossHalfLine(hl)
            if p:
                print(len(p))
                p = p[0]
                window.draw.line(window.screen, color, [p.x, p.y], [self.p2.x, self.p2.y], width)
        else:
            ps = f.crossSegment(self)
            if len(ps) == 2:
                p1, p2 = ps
                window.draw.line(window.screen, color, [p1.x, p1.y], [p2.x, p2.y], width)

    def __contains__(self, point, e=1e-10):
        """Determine if a point is in a segment."""
        if point == self.p1:
            return True
        v1 = Vector.createFromTwoPoints(self.p1, point)
        v2 = self.getVector()
        return (abs(v1.angle - v2.angle) % (2 * math.pi) < e) and (v1.norm <= v2.norm)

    def __len__(self):
        """Return the number of points."""
        return len(self.points)

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return the next point through an iteration."""
        if self.iterator < len(self.points):
            self.iterator += 1
            return self.points[self.iterator-1]
        else:
            raise StopIteration

    def __getitem__(self, index):
        """Return the point corresponding to the index given."""
        return [self.points][index]

    def __setitem__(self, index, value):
        """Change the value the point corresponding value and index given."""
        self.points[index] = value

    def getLine(self, **kwargs):
        """Return the line through the end points of the segment."""
        return Line(self.p1, self.angle, **kwargs)

    def getVector(self):
        """Return the vector that goes from p1 to p2."""
        return Vector.createFromTwoPoints(self.p1, self.p2)

    def setVector(self, vector):
        """Set the vector that goes from p1 to p2."""
        self.p2 = vector(self.p1)

    def getLength(self):
        """Return the length of the segment."""
        return self.vector.norm

    def setLength(self, length):
        """Set the length of the segment."""
        self.vector.norm = length

    def rotate(self, angle, point=None):
        """Rotate the segment using an angle and an optional point of rotation."""
        if not point:
            point = self.middle
        self.p1.rotate(angle, point)
        self.p2.rotate(angle, point)

    def __or__(self, other):
        """Return bool for (2 segments are crossing)."""
        if isinstance(other, Segment):
            return self.crossSegment(other)
        elif isinstance(other, Line):
            return self.crossLine(other)
        elif isinstance(other, HalfLine):
            return other.crossSegment(self)
        elif isinstance(other, Form):
            return other.crossSegment(self)
        else:
            raise TypeError("The collisions {}|{} are not dealt with.".format(type(self), type(other)))

    def getXmin(self):
        """Return the minimum of x components of the 2 end points."""
        return min(self.p1.x, self.p2.x)

    def getYmin(self):
        """Return the minimum of y components of the 2 ends points."""
        return min(self.p1.y, self.p2.y)

    def getXmax(self):
        """Return the maximum of x components of the 2 end points."""
        return max(self.p1.x, self.p2.x)

    def getYmax(self):
        """Return the maximum of y components of the 2 end points."""
        return max(self.p1.y, self.p2.y)

    def getMinimum(self):
        """Return the lower point"""
        v1 = Vector(*self.p1)
        v2 = Vector(*self.p2)
        if v1.angle < v2.angle:
            return self.p1
        else:
            return self.p2

    def getMaximum(self):
        """Return the upper point."""
        v1 = Vector(*self.p1)
        v2 = Vector(*self.p2)
        if v1.angle >= v2.angle:
            return self.p1
        else:
            return self.p2

    def getCorners(self):
        """Return the minimum and maximum of x and y components of the 2 end points."""
        return self.minimum.components + self.maximum.components

    def parallel(self, other):
        """Determine if the line is parallel to another object (line or segment)."""
        return other.angle == self.angle

    def cross(self, other, **kwargs):
        if isinstance(other, Segment):
            return self.crossSegment(other, **kwargs)
        elif isinstance(other, Line):
            return other.crossSegment(self, **kwargs)
        else:
            raise TypeError("The collisions {}|{} are not dealt with.".format(type(self), type(other)))

    def crossSegment(self, other, e=1e-14):
        """Return the intersection point of the segment with another segment."""
        sl = self.getLine()
        ol = other.getLine()
        point = sl.crossLine(ol)
        if point is not None:
            if self.__contains__(point, e) and other.__contains__(point, e):
                return point

    def crossLine(self, other):
        """Return the intersection point of the segment with a line."""
        if self.parallel(other): return None
        line = self.getLine()
        point = other.crossLine(line)
        if point is not None:
            if point in self and point in other:
                return point

    def getP1(self):
        """Return the first point of the segment."""
        return self.points[0]

    def setP1(self, p1):
        """Set the first point of the segment."""
        self.points[0] = p1

    def getP2(self):
        """Return the second point of the segment."""
        return self.points[1]

    def setP2(self, p2):
        """Set the second point of the segment."""
        self.points[1] = p2

    p1 = property(getP1, setP1, doc="First point of the segment.")
    p2 = property(getP2, setP2, doc="Second point of the segment.")
    middle = center = property(getCenter, setCenter, doc="Center of the segment.")
    vector = property(getVector, setVector, doc="Unit vector of the segment.")
    angle = property(getAngle, setAngle, doc="Angle of the segment.")
    length = property(getLength, setLength, doc="Length of the segment.")
    line = property(getLine, doc="Line passing by both extremities.")
    xmin = property(getXmin, doc="xmin")
    ymin = property(getYmin, doc="ymin")
    xmax = property(getXmax, doc="xmax")
    ymax = property(getYmax, doc="ymax")
    minimum = property(getMinimum, doc="Point at the right")
    maximum = property(getMaximum, doc="Point at the left")


class Line(Direction):
    @classmethod
    def random(cls, borns=[-1, 1], angle_borns=[-math.pi, math.pi], **kwargs):
        """Return a random line."""
        point = Point.random(borns=borns)
        angle = random.uniform(*angle_borns)
        return cls(point, angle, **kwargs)

    @classmethod
    def createFromPointAndVector(cls, point, vector, **kwargs):
        """Create a line using a point and a vector with optional features."""
        return cls(point, vector.angle, **kwargs)

    @classmethod
    def createFromTwoPoints(cls, point1, point2, **kwargs):
        """Create a line using two points with optional features."""
        vector = Vector.createFromTwoPoints(point1, point2)
        return cls(point1, vector.angle, **kwargs)

    def __init__(self, point, angle, width=1, color=mycolors.WHITE, correct=True):
        """Create the line using a point and a vector with optional width and color.
        The line is uses a unique system of components [neighbour point, angle].
        The neighbour point is the nearest point to (0,0) that belongs to the line.
        The angle is the orientated angle between the line itself and another line parallel
        to the x-axis and crossing the neighbour point. Its range is [-pi/2,pi/2[ which makes it unique."""
        if correct:
            self.angle = angle
            self.point = point
        else:
            self._angle = angle
            self._point = point
        self.width = width
        self.color = color

    def __str__(self, precision=2):
        """Return a string representation of the line."""
        return "l(a=" + str(round(self.slope, precision)) + \
               ",b=" + str(round(self.ordinate, precision)) + ")"

    def __call__(self, x):
        """Evaluate the line like a linear function in cartesian coordinates."""
        return self.slope * x + self.ordinate

    def __eq__(self, l):
        """Determine if two lines are the same."""
        return l.point == self.point and l.angle == self.angle

    def getCompleteCartesianCoordonnates(self):
        """Return a,b,c according to the cartesian equation of the line: ax+by+c=0."""
        v = self.vector
        p1 = self.point
        p2 = v(self.point)
        if v.x == 0:
            a = 1
            b = 0
            c = -p1.x
        else:
            a = -(p1.y - p2.y) / (p1.x - p2.x)
            b = 1
            c = -(a * p1.x + b * p1.y)
        return a, b, c

    def getReducedCartesianCoordonnates(self):
        """Return a,b according to the reduced cartesian equation of the line: y=ax+b."""
        return self.slope, self.ordinate

    def getAngle(self):
        """Return the angle of the line."""
        return self._angle

    def setAngle(self, angle):
        """Set the angle of the line."""
        self._angle = (angle + math.pi / 2) % math.pi - math.pi / 2
        # self._angle = angle % (2*math.pi)

    angle = property(getAngle, setAngle, doc="Representation of the angle of the line after correction.")

    def rotate(self, angle, point=Point(0, 0)):
        """Rotate the line."""
        self.angle += angle   # Incomplete

    def getPoint(self):
        """Return the neighbour point."""
        return self._point

    def setPoint(self, point):
        """Set the neighbour point to another one."""
        self._point = point
        self._point = self.projectPoint(Point.origin(point.dimension))

    point = property(getPoint,setPoint, doc="Neighbour point of the line.")

    def getUnitVector(self):
        """Return the unit vector of the line."""
        return Vector.createFromPolar(1, self.angle)

    def setUnitVector(self, vector):
        """Set the unit vector of the line."""
        self.angle = vector.angle

    def getNormalVector(self):
        """Return the normal vector of the line."""
        vector = self.unit_vector
        vector.rotate(math.pi / 2)
        return vector

    def setNormalVector(self, vector):
        """Set the normal vector of the line."""
        self.angle = vector.angle + math.pi / 2

    def getSlope(self):
        """Return the slope of the line."""
        return math.tan(self.angle)

    def setSlope(self, slope):
        """Set the slope of the line by changing its angle and point."""
        self.angle = math.atan(slope)

    def getOrdinate(self):
        """Return the ordinate of the line."""
        return self.point.y - self.slope * self.point.x

    def setOrdinate(self, ordinate):
        """Set the ordinate of the line by changing its position."""
        if abs(self.angle) == math.pi / 2:
            raise ValueError("Impossible to set an ordinate because the line is parallel to the y axis. ")
        self.point.y += ordinate

    def getFunction(self):
        """Return the affine function that correspond to the line."""
        return lambda x: self.slope * x + self.ordinate

    def setFunction(self, function):
        """Set the function of the line by changing its slope and ordinate."""
        self.ordinate = function(0)
        self.slope = function(1) - function(0)

    def getReciproque(self):
        """Return the reciproque of the affine function that correspond to the line."""
        return lambda y: (y - self.ordinate) / self.slope

    def setReciproque(self, reciproque):
        """Return the reciproque function of the affine function."""
        x0, x1 = reciproque(0), reciproque(1)
        self.slope = 1 / (x1 - x0)
        self.ordinate = - x0 * self.slope

    def evaluate(self, x):
        """Evaluate the line as a affine function."""
        return self.function(x)

    def devaluate(self, y):
        """Evaluate the reciproque function of the affine funtion of the line."""
        return self.reciproque(y)

    def cross(self, other):
        """Return the point of intersection between the line and another object."""
        if isinstance(other, Line):
            return self.crossLine(other)
        elif isinstance(other, Segment):
            return self.crossSegment(other)
        elif isinstance(other, HalfLine):
            return other.crossLine(self)
        elif isinstance(other, Form):
            return other.crossLine(self)
        else:
            raise TypeError("The collisions {}|{} are not dealt with.".format(type(self), type(other)))

    __or__ = cross

    def crossSegment(self, other, e=1e-14, **kwargs):
        """Return the point of intersection between a segment and the line."""
        # Determine the point of intersection between the line of the given segment ang the line
        line = other.getLine()
        point = self.crossLine(line)
        if point is None:
            return None
        x, y = point
        # Determine if the point of intersection belongs to both the segment and the line
        if other.xmin - e <= point.x <= other.xmax + e and other.ymin - e <= y <= other.ymax + e:
            return Point(x, y, **kwargs)
        # By default if nothing is returned the function returns None

    def crossLine(self, other):
        """Return the point of intersection between two lines with vectors
        calculation. Works in all cases even with vertical lines."""
        a, b = self.point
        c, d = other.point
        m, n = self.vector
        o, p = other.vector
        if n * o == m * p:  # The lines are parallels
            return None
        elif self.angle == -math.pi / 2:
            return Point(a, d)
        elif other.angle == -math.pi / 2:
            return Point(b, c)
        else:
            x = (a * n * o - b * m * o - c * m * p + d * m * o) / (n * o - m * p)
            y = (x - a) * n / m + b
            return Point(x, y)

    def parallel(self, other):
        """Determine if the line is parallel to another object (line or segment)."""
        return other.angle == self.angle

    def __contains__(self, point, e=10e-10):
        """Determine if a point belongs to the line."""
        v1 = self.vector
        v2 = Vector.createFromTwoPoints(self.point, point)
        return v1.colinear(v2, e)

    def getHeight(self, point):
        """Return the height line between the line and a point."""
        return Line(point, self.normal_vector.angle)

    def distanceFromPoint(self, point):
        """Return the distance between a point and the line."""
        return Vector.createFromTwoPoints(point, self.crossLine(self.getHeight(point))).norm

    def projectPoint(self, point):
        """Return the projection of the point on the line."""
        vector = self.normal_vector
        angle = vector.angle
        line = Line(point, angle, correct=False)
        projection = self.crossLine(line)
        return projection

    def projectPoints(self, points):
        """Return the projections of the points on the line."""
        return [self.projectPoint(point) for point in points]

    def projectSegment(self, segment):
        """Return the projection of a segment on the line."""
        points = self.projectPoints(segment.points)
        return Segment(*points, segment.width, segment.color)

    def getSegmentWithinCorners(self, corners):
        """Return the segment made of the points of the line which are in the area
        delimited by the corners."""
        xmin, ymin, xmax, ymax = corners
        p1 = Point(xmin, ymin)
        p2 = Point(xmax, ymin)
        p3 = Point(xmax, ymax)
        p4 = Point(xmin, ymax)
        s1 = Segment(p1, p2)
        s2 = Segment(p2, p3)
        s3 = Segment(p3, p4)
        s4 = Segment(p4, p1)
        pts = []
        for s in [s1, s2, s3, s4]:
            cross = self.crossSegment(s)
            if cross:
                pts.append(cross)
        if len(pts) == 2:
            return Segment(*pts)

    def getPointsWithinCorners(self, corners):
        """Return the segment made of the points of the line which are in the area
        delimited by the corners."""
        xmin, ymin, xmax, ymax = corners
        p1 = Point(xmin, ymin)
        p2 = Point(xmax, ymin)
        p3 = Point(xmax, ymax)
        p4 = Point(xmin, ymax)
        v1 = Vector(p1, p2)
        v2 = Vector(p2, p3)
        v3 = Vector(p3, p4)
        v4 = Vector(p4, p1)
        l1 = Line.createFromPointAndVector(p1, v1)
        l2 = Line.createFromPointAndVector(p2, v2)
        l3 = Line.createFromPointAndVector(p3, v3)
        l4 = Line.createFromPointAndVector(p4, v4)
        lines = [l1, l3]
        points = []
        for line in lines:
            cross = self.crossLine(line)
            if cross:
                points.append(cross)
        if not points:
            lines = [l2, l4]
            for line in lines:
                cross = self.crossLine(line)
                if cross:
                    points.append(cross)
        return points

    def show(self, context, width=None, color=None):
        """Show the line on the context by drawing a segment greater than
        the size of the context."""
        if not color:
            color = self.color
        if not width:
            width = self.width
        s = max(context.size)
        u = min(context.units)
        n = s/u
        p = Point(*context.point())
        p = self.projectPoint(p)
        v1 = Vector.createFromPolar(n, self.angle)
        v2 = -v1
        s = Segment(v1(p), v2(p), color=color, width=width, conversion=True)
        s.show(context)

    def showWithinCorners(self, context, width=None, color=None):
        if not color:
            color = self.color
        if not width:
            width = self.width
        s = self.getSegmentWithinCorners(context.corners)
        s.show(context)

    vector = unit_vector = property(getUnitVector, setUnitVector, doc="Unit vector of the line.")
    normal_vector = property(getNormalVector, setNormalVector, doc="Normal vector of the line.")
    slope = property(getSlope, setSlope, doc="Slope of the line in cartesian system.")
    ordinate = property(getOrdinate, setOrdinate, doc="Ordinate of the line in cartesian system.")
    function = property(getFunction, setFunction, doc="Linear function of the line in cartesian system.")
    reciproque = property(getReciproque, setReciproque, doc="Reciproque of the function of the line in cartesian system.")


class HalfLine(Line):
    def createFromLine(line):
        """Create a half line."""
        return HalfLine(line.point, line.angle)

    def __init__(self, point, angle, color=mycolors.WHITE, width=1):
        """Create a half line."""
        super().__init__(point, angle, color=color, width=width, correct=False)

    def getLine(self, correct=True):
        """Return the line that correspond to the half line."""
        return Line(self.point, self.angle, correct=correct)

    def getPoint(self):
        """Return the point of the half line."""
        return self.point

    def setPoint(self, point):
        """Set the point of the half line."""
        self.point = point

    def show(self, context, width=None, color=None):
        """Show the line on the surface."""
        if not color:
            color = self.color
        if not width:
            width = self.width
        xmin, ymin, xmax, ymax = context.corners
        form = Form.createFromTuples([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)])
        points = form.crossHalfLine(self)
        points += [self.point] * (2 - len(points))
        if len(points) > 0:
            context.draw.line(context.screen, color, points[0], points[1], width)

    def __contains__(self, point, e=10e-10):
        """Determine if a point is in the half line."""
        v1 = self.vector
        v2 = Vector.createFromTwoPoints(self.point, point)
        return abs(v1.angle - v2.angle) < e

    def cross(self, other):
        """Return the intersection point between the half line and another object."""
        if isinstance(other, Line):
            return self.crossLine(other)
        if isinstance(other, Segment):
            return self.crossSegment(other)
        if isinstance(other, HalfLine):
            return self.crossHalfLine(other)
        if isinstance(other, Form):
            return other.crossHalfLine(self)

    __or__  = cross

    def crossHalfLine(self, other):
        """Return the point of intersection of the half line with another."""
        ml = self.getLine(correct=False)
        ol = other.getLine(correct=False)
        point = ml.crossLine(ol)
        if point:
            if (point in self) and (point in other):
                return point

    def crossLine(self, other):
        """Return the point of intersection of the half line with a line."""
        ml = self.getLine(correct=False)
        point = ml.crossLine(other)
        if point:
            if (point in self) and (point in other):
                return point

    def crossSegment(self, other):
        """Return the point of intersection of the half line with a segment."""
        ml = self.getLine(correct=False)
        ol = other.getLine(correct=False)
        point = ml.crossLine(ol)
        if point:
            if (point in self) and (point in other):
                return point

    def __str__(self):
        """Return the string representation of a half line."""
        return "hl(" + str(self.point) + "," + str(self.angle) + ")"


class Form:
    @classmethod
    def random(cls, n=random.randint(5, 10), d=2, borns=[-1, 1], **kwargs):
        """Create a random form using the number of points 'n', the dimension
        of the points 'p' and their borns with optional arguments."""
        points = [Point.random(d=d, borns=borns) for i in range(n)]
        form = cls(points, **kwargs)
        form.makeSparse()
        return form

    def anyCrossing(forms):
        """Determine if any of the forms are crossing."""
        if len(forms) == 1: forms = forms[0]
        l = len(forms)
        for i in range(l):
            for j in range(i + 1, l):
                if forms[i].crossForm(forms[j]):
                    return True
        return False

    def allCrossing(forms):
        """Determine if all the forms are crossing."""
        if len(forms) == 1: forms = forms[0]
        l = len(forms)
        for i in range(l):
            for j in range(i + 1, l):
                if not forms[i].crossForm(forms[j]):
                    return False
        return True

    def cross(form1, form2):
        """Return the points of intersection between the crossing forms."""
        for point in form1.points:
            if point in form2:
                return True
        for point in form2.points:
            if point in form1:
                return True
        return

    @classmethod
    def intersectionTwoForms(cls, form1, form2):
        """Return the form which is the intersection of two forms."""
        if form1 == None: return form2
        if form2 == None: return form1
        if form1 == form2 == None: return None
        points = form1.crossForm(form2)
        if not points: return None
        for point in form1.points:
            if point in form2:
                points.append(point)
        for point in form2.points:
            if point in form1:
                points.append(point)
        form = cls(points)
        form.makeSparse()
        return form

    @classmethod
    def intersection(cls, forms):
        """Return the form which is the intersection of all the forms."""
        result = forms[0]
        for form in forms[1:]:
            result = cls.intersectionTwoForms(result, form)
        return result

    @classmethod
    def unionTwoForms(cls, form1, form2):
        """Return the union of two forms."""
        intersection_points = set(form1.crossForm(form2))
        if intersection_points:
            all_points = set(form1.points + form2.points)
            points = all_points.intersection(intersection_points)
            return [cls(points)]
        else:
            return [form1, form2]

    @classmethod
    def union(cls, forms):
        """Return the union of all forms."""
        """This function must be recursive."""
        if len(forms) == 2:
            return cls.unionTwoForms(forms[0], forms[1])
        else:
            pass

        result = forms[0]
        for form in forms[1:]:
            result.extend(cls.union(form, result))
        return result

    @classmethod
    def createFromTuples(cls, tps, conversion=True, radius=0.01, **kwargs):
        """Create a form from the tuples 'tps' and some optional arguments."""
        pts = [Point(*t, conversion=conversion, radius=0.01) for t in tps]
        return cls(pts, **kwargs)

    def __init__(self, points,
                 fill=False,
                 point_mode=0,
                 point_size=[0.01, 0.01],
                 point_radius=0.01,
                 point_width=1,
                 point_fill=False,
                 side_width=1,
                 color=None,
                 point_color=mycolors.WHITE,
                 side_color=mycolors.WHITE,
                 area_color=mycolors.WHITE,
                 cross_point_color=mycolors.WHITE,
                 cross_point_radius=0.01,
                 cross_point_mode=0,
                 cross_point_width=1,
                 cross_point_size=[0.1, 0.1],
                 point_show=True,
                 side_show=True,
                 area_show=False):
        """Create the form object using points."""
        self.points = points

        self.point_mode = point_mode
        self.point_size = point_size
        self.point_width = point_width
        self.point_radius = point_radius
        self.point_color = point_color or color
        self.point_show = point_show
        self.point_fill = point_fill

        self.side_width = side_width
        self.side_color = side_color or color
        self.side_show = side_show

        self.area_color = area_color or color
        self.area_show = area_show or fill

        self.cross_point_color = cross_point_color
        self.cross_point_radius = cross_point_radius
        self.cross_point_mode = cross_point_mode
        self.cross_point_width = cross_point_width
        self.cross_point_size = cross_point_size

    def __str__(self):
        """Return the string representation of the form."""
        return "f(" + ",".join([str(p) for p in self.points]) + ")"

    def setFill(self, fill):
        """Set the form to fill its area when shown."""
        self.area_show = fill

    def getFill(self):
        """Return if the area is filled."""
        return self.area_show

    fill = property(getFill, setFill, doc="Allow the user to manipulate easily if the area is filled.")

    def __iadd__(self, point):
        """Add a point to the form."""
        self.points.append(point)
        return self

    def __isub__(self, point):
        """Remove a point to the form."""
        self.points.remove(point)
        return self

    def __mul__(self, n):
        """Return a bigger form."""
        vectors = [n * Vector(*(p - self.center)) for p in self.points]
        return Form([vectors[i](self.points[i]) for i in range(len(self.points))])

    def __imul__(self, n):
        """Return a bigger form."""
        vectors = [n * Vector(*(p - self.center)) for p in self.points]
        self.points = [vectors[i](self.points[i]) for i in range(len(self.points))]
        return self

    __rmul__ = __mul__

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < len(self.points):
            iterator = self.iterator
            self.iterator += 1
            return self.points[iterator]
        else:
            raise StopIteration

    def __eq__(self, other):
        """Determine if 2 forms are the same which check the equalities of their components."""
        return sorted(self.points) == sorted(other.points)

    def getCenter(self):
        return Point.average(self.points)

    def setCenter(self, center):
        """Set the center of the form."""
        p = center - self.center
        for i in range(len(self.points)):
            self.points[i] += p

    def getCentroid(self):
        """Return the point of the center.
        This only works for 2 dimensional forms obviously."""
        if len(self.points) == 0:
            # None
            return None
        elif len(self.points) == 1:
            # Same point
            return self.points[0]
        elif len(self.points) == 2:
            # Middle of a segment
            return Segment(*self.points).middle
        elif len(self.points) == 3:
            # Intersection point of 2 medians
            return Point.average(self.points)
        else:
            # Geometric decomposition to compute centroids (wikipedia)
            n = len(self.points)  # n is the number of points
            # There are n-2 forms
            forms = [Form([self.points[0]] + self.points[i:i + 2]) for i in range(1, n - 1)]
            # So n-2 centroids and areas, except if some of the points are one upon another, no area is null
            centroids = [form.center for form in forms]
            areas = [form.area for form in forms]
            # we compute the average centroid weighted by the areas
            weighted_centroid = Point.sum([a * c for (c, a) in zip(centroids, areas)])
            centroid = weighted_centroid / sum(areas)
            return centroid

    def setCentroid(self, center):
        """Set the center of the form."""
        p = center - self.centroid
        for i in range(len(self.points)):
            self.points[i] += p

    def recenter(self, point=(0, 0)):
        """Recenter a form using the new center point."""
        self.center = Point(*point)

    def enlarge(self, n=2):
        """Enlarge the form by a factor of n."""
        c = self.center
        for i in range(len(self.points)):
            v = Vector.createFromTwoPoints(c, self.points[i])
            self.points[i].set((n * v)(c))

    def spread(self, n=2):
        """Take away the form by a factor of n."""
        for point in self.points:
            point *= n

    def getSegments(self):
        """"Return the list of the form sides."""
        l = len(self.points)
        return [Segment(self.points[i % l], self.points[(i + 1) % l], \
                        color=self.side_color, width=self.side_width) for i in range(l)]

    def setSegments(self, segments):
        """Set the segments of the form by setting its points to new values."""
        for point, segment in zip(self.points, segments):
            point.set(segment.p1)

    def getVectors(self):
        """Return the list of the form vectors."""
        l = len(self.points)
        return [Vector.createFromTwoPoints(self.points[i % l], self.points[(i + 1) % l], \
                        color=self.side_color, width=self.side_width) for i in range(l)]

    def setVectors(self, vectors):
        """Return the list of the form vectors."""
        l = len(self.points)
        for point, vector in zip(self.points, vectors):
            point.set(vector.components)

    def showAll(self, surface, **kwargs):
        """Show the form using a window."""
        # ,window,point_color=None,side_color=None,area_color=None,side_width=None,point_radius=None,color=None,fill=None,point_show=None,side_show=None
        if not "point_show" in kwargs:
            kwargs["point_show"] = self.point_show
        if not "side_show" in kwargs:
            kwargs["side_show"] = self.side_show
        if not "area_show" in kwargs:
            kwargs["area_show"] = self.area_show
        if kwargs["area_show"]:
            self.showAllArea(surface, **kwargs)
        if kwargs["side_show"]:
            self.showAllSegments(surface, **kwargs)
        if kwargs["point_show"]:
            self.showAllPoints(surface, **kwargs)

    def showFast(self, surface, point=None, segment=None, area=None):
        """Show the form using the surface and optional objects to show."""
        if point:
            self.showPoints(surface)
        if segment:
            self.showSegments(surface)
        if area:
            self.showArea(surface)

    def show(self, surface):
        """Show the form using the surface and optional objects to show."""
        if self.area_show:
            self.showArea(surface)
        if self.side_show:
            self.showSegments(surface)
        if self.point_show:
            self.showPoints(surface)

    def showFastArea(self, surface, color=None):
        """Show the area of the form using optional parameters such as the area
        of the color."""
        if not color: color = self.area_color
        ps = [tuple(p) for p in self.points]
        if len(ps) > 1:
            surface.draw.polygon(surface.screen, color, ps, False)

    def showAllArea(self, surface, **kwargs):
        """Show the area of the form using optional parameters such as the area
        of the color. This function is slower than the previous one because it
        checks if the dictionary or attributes contains the area_color."""
        if not "area_color" in kwargs:
            kwargs["area_color"] = self.area_color
        ps = [tuple(p) for p in self.points]
        if len(ps) > 1:
            surface.draw.polygon(surface.screen, kwargs["area_color"], ps, False)

    def showArea(self, surface):
        """Show the area of the form."""
        ps = [tuple(p) for p in self.points]
        if len(ps) > 1:
            surface.draw.polygon(surface.screen, self.area_color, ps, False)

    def showPoints(self, surface):
        """Show the points."""
        for point in self.points:
            point.show(surface)

    def showFastPoints(self, surface,
                       color=None,
                       mode=None,
                       radius=None,
                       size=None,
                       width=None,
                       fill=None):
        """Show the points of the form using optional parameters."""
        if color is None:
            color = self.point_color
        if radius is None:
            radius = self.point_radius
        if mode is None:
            mode = self.point_mode
        if size is None:
            size = self.point_size
        if width is None:
            width = self.point_width
        if fill is None:
            fill = self.point_fill
        for point in self.points:
            point.show(surface, color, mode, fill, radius, size, width)

    def showAllPoints(self, surface, **kwargs):
        """Show the points of the form using optional parameters.
        This method is slower than the previous one because it checks if the
        dictionary of attributes contains the arguments."""
        if not "point_color" in kwargs:
            kwargs["point_color"] = self.point_color
        if not "point_radius" in kwargs:
            kwargs["point_radius"] = self.point_radius
        if not "point_mode" in kwargs:
            kwargs["point_mode"] = self.point_mode
        if not "point_size" in kwargs:
            kwargs["point_size"] = self.point_size
        if not "point_width" in kwargs:
            kwargs["point_width"] = self.point_width
        if not "point_fill" in kwargs:
            kwargs["point_fill"] = self.point_fill
        for point in self.points:
            point.show(surface,
                       color=kwargs["point_color"],
                       mode=kwargs["point_mode"],
                       fill=kwargs["point_fill"],
                       radius=kwargs["point_radius"],
                       size=kwargs["point_size"],
                       width=kwargs["point_width"])

    @timer
    def showFastSegments(self, context, color=None, width=None):
        """Show the segments of the form."""
        if not color:
            color = self.segment_color
        if not width:
            width = self.segment_width
        for segment in self.segments:
            segment.show(context, color, width)

    def showSegments(self, surface):
        """Show the segments without its parameters."""
        for segment in self.segments:
            segment.show(surface)

    def showAllSegments(self, surface, **kwargs):
        """Show the segments of the form."""
        if not "side_color" in kwargs:
            kwargs["side_color"] = self.side_color
        if not "side_width" in kwargs:
            kwargs["side_width"] = self.side_width
        for segment in self.segments:
            segment.show(surface, color=kwargs["side_color"], width=kwargs["side_width"])

    def showFastCrossPoints(self, surface, color=None, mode=None, radius=None, width=None, size=None):
        """Show the intersection points of the form crossing itself."""
        points = self.crossSelf()
        if not color:
            color = self.cross_point_color
        if not mode:
            mode = self.cross_point_mode
        if not radius:
            radius = self.cross_point_radius
        if not width:
            width = self.cross_point_width
        if not size:
            size = self.cross_point_size
        for point in points:
            point.show(surface, color=color, mode=mode, radius=radius, width=width, size=size)

    def showCrossPoints(self, surface):
        """Show the intersection points of the form crossing itself."""
        for point in self.cross_points:
            point.show(surface)

    def cross(self, other):
        """Return the points of intersections with the form and another object."""
        if isinstance(other, Form):
            return self.crossForm(other)
        elif isinstance(other, Segment):
            return self.crossSegment(other)
        elif isinstance(other, Line):
            return self.crossLine(other)
        elif isinstance(other, HalfLine):
            return self.crossHalfLine(other)
        else:
            raise TypeError("The collisions {}|{} are not dealt with.".format(type(self), type(other)))

    __or__ = cross

    def crossForm(self, other):
        """Return the bool: (2 sides are crossing)."""
        points = []
        for s1 in self.sides:
            for s2 in other.sides:
                point = s1.crossSegment(s2)
                if point:
                    points.append(point)
        return points

    def crossDirection(self, other):
        """Return the list of the points of intersection between the form and a segment or a line."""
        points = []
        for side in self.sides:
            cross = side | other
            if cross:
                points.append(cross)
        return points

    def crossHalfLine(self, other):
        """Return the list of points of intersection in order between the form and a half line."""
        points = []
        for segment in self.segments:
            cross = other.crossSegment(segment)
            if cross:
                points.append(cross)
        hp = other.point
        objects = [(p, Point.distance(p, hp)) for p in points]
        objects = sorted(objects, key=lambda x: x[1])
        return [p for (p, v) in objects]

    def crossLine(self, other):
        """Return the list of the points of intersection between the form and a line."""
        points = []
        for segment in self.segments:
            cross = segment.crossLine(other)
            if cross:
                points.append(cross)
        return points

    def crossSegment(self, other):
        """Return the list of the points of intersection between the form and a segment."""
        points = []
        for side in self.sides:
            point = side.crossSegment(other)
            if point:
                points.append(point)
        return points

    def crossSelf(self, e=1e-10):
        """Return the list of the points of intersections between the form and itself."""
        results = []
        l = len(self.segments)
        for i in range(l):
            for j in range(i + 1, l):
                point = self.segments[i].crossSegment(self.segments[j])
                if point:
                    if point in self.points:
                        results.append(point)
        return results

    def convex(self):
        """Return the bool (the form is convex)."""
        x, y = self.center
        angles = []
        l = len(self.points)
        for i in range(l - 1):
            A = self.points[(i + l - 1) % l]
            B = self.points[i % l]
            C = self.points[(i + 1) % l]
            u = Vector.createFromTwoPoints(A, B)
            v = Vector.createFromTwoPoints(C, B)
            angle = v ^ u
            if angle > pi:
                return True
        return False

    def getSparse(self):  # as opposed to makeSparse which keeps the same form and return nothing
        """Return the form with the most sparse points."""
        return copy.deepcopy(self.makeSparse())

    def makeSparse(self):
        """Change the form into the one with the most sparse points."""
        center = self.center
        l = []
        for point in self.points:
            angle = Vector.createFromTwoPoints(point, center).angle
            l.append((angle, copy.deepcopy(point)))
        l = sorted(l, key=lambda x: x[0])
        for i in range(len(l)):
            self.points[i].set(l[i][1])

    def __contains__(self, point):
        """Return the boolean: (the point is in the form)."""
        h = HalfLine(point, 0)
        ps = self.crossHalfLine(h)
        return len(ps) % 2 == 1

    def rotate(self, angle, point=None):
        """Rotate the form by rotating its points from the center of rotation.
        Use center of the shape as default center of rotation."""
        # Actually not working
        if not point:
            point = self.center
        for i in range(len(self.points)):
            self.points[i].rotate(angle, point)

    def move(self, step):
        """Move the object by moving all its points using step."""
        for point in self.points:
            l = min(len(step), len(point.position))
            for i in range(l):
                point.position[i] = step[i]

    def addPoint(self, point):
        """Add a point to the form."""
        self.points.append(point)

    def addPoints(self, points):
        """Add points to the form."""
        self.points.extend(points)

    append = addPoint
    extend = addPoints

    def removePoint(self, point):
        """Remove a point to the form."""
        self.points.remove(point)

    __remove__ = removePoint

    def __getitem__(self, index):
        """Return the point of index index."""
        return self.points[index]

    def __setitem__(self, index, value):
        """Change the points of a form."""
        self.points[index] = value

    @property
    def perimeter(self):
        """Return the perimeter of the form."""
        return sum([s.length for s in self.segments])

    @property  # This can only be a getter
    def area(self):
        """Return the area of the form using its own points.
        General case in 2d only for now..."""
        l = len(self.points)
        if l < 3:  # The form has no point, is a single point or a segment, so it has no area.
            return 0
        elif l == 3:  # The form is a triangle, so we can calculate its area.
            a, b, c = [Vector.createFromSegment(segment) for segment in self.sides]
            A = 1 / 4 * sqrt(4 * a.norm ** 2 * b.norm ** 2 - (a.norm ** 2 + b.norm ** 2 - c.norm ** 2) ** 2)
            return A
        else:  # The form has more points than 3, so we can cut it in triangles.
            area = 0
            C = self.center
            for i in range(l):
                A = self.points[i]
                B = self.points[(i + 1) % l]
                triangle = Form([A, B, C])
                area += triangle.area
            return area

    @property
    def angles(self):
        ags = []
        vectors = self.vectors
        ag = (- vectors[-1]).angle
        for v in vectors:
            ang = ((v.angle - ag))
            ag = (-v).angle
            ags.append(ang)
        return ags

    @property
    def abs_angles(self):
        ags = []
        vectors = self.vectors
        ag = (- vectors[-1]).angle
        for v in vectors:
            dag = abs(v.angle - ag)
            ang = min(dag, 2 * math.pi - dag)
            ag = (-v).angle
            ags.append(ang)
        return ags

    def getCircleDiameter(self):
        """Return the circle which diameter is the largest segment of the form.."""
        segments = []
        for (i, p1) in enumerate(self.points):
            for p2 in self.points[i+1:]:
                segments.append(Segment(p1, p2))
        s = max(segments, key=lambda s: s.length)
        return Circle(*s.middle, radius=s.length/2)

    def getBornCircle(self):
        distances = []
        for p1 in self.points:
            distance = sum([Point.distance(p1, p2) for p2 in self.points])
            distances.append((distance, p1))
        pt1 = max(distances)[1]
        pt2 = Point.farthest(pt1, self.points)
        distances = []
        for p in self.points:
            if not p in [pt1, pt2]:
                distance = max(Point.distance(p, pt1), Point.distance(p, pt2))
                distances.append((distance, p))
        pt3 = max(distances)[1]
        triangle = Form([pt1, pt2, pt3])
        return triangle.getBornCircleTriangle()

    def getBornCircle2(self):
        if len(self.points) == 3:
            return self.getBornCircleTriangle()
        else:
            circles = []
            for (p1, p2, p3) in itertools.combinations(self.points, 3):
                form = Form([p1, p2, p3])
                circle = form.getBornCircle2()
                circles.append(circle)
            circles.sort(key=lambda circle: circle.radius, reverse=True)
            return circles[0]

    def getBornCircle3(self):
        triangles = self.getSubForms(3)
        f = max(triangles, key=lambda triangle:triangle.perimeter)
        # f = max(triangles, key=lambda triangle: triangle.area)
        if f.obtusangle:
            return f.getCircleDiameter(), f
        else:
            return f.getCircleCircumscribed(), f

    def getBornCircleSlow(self, e=1e-3):
        for (p1, p2) in self.getSubForms(2):
            segment = Segment(p1, p2)
            l = segment.length / 2
            c = segment.middle
            condition = True
            for p in self.points:
                if Point.distance(p, c) + e > l:
                    condition = False
                    break
            if condition:
                return Circle(*c, radius=l)

        for triangle in self.getSubForms(3):
            circle = triangle.getCircleCircumscribed()
            c = circle.center
            l = circle.radius
            condition = True
            for p in self.points:
                if Point.distance(p, c) + e > l:
                    condition = False
                    break
            if condition:
                print(circle)
                return circle

            print("not found")
            circle.border_color = mycolors.YELLOW
            return circle

    def getSubForms(self, n):
        return list(map(Form, itertools.combinations(self.points, n)))

    @property
    def obtusangle(self):
        for angle in self.abs_angles:
            if 2 * angle >= math.pi:
                return True
        return False

    @property
    def acutangle(self):
        for angle in self.abs_angles:
            if 2 * angle <= math.pi:
                return True
        return False

    def getCircleCircumscribed(self):
        """Return the circumbscribed circle of a triangle."""
        p1, p2, p3 = self.points
        a1 = - (p2.x - p1.x) / (p2.y - p1.y)
        b1 = (p2.x ** 2 - p1.x ** 2 + p2.y ** 2 - p1.y ** 2) / (2 * (p2.y - p1.y))
        a2 = - (p3.x - p2.x) / (p3.y - p2.y)
        b2 = (p3.x ** 2 - p2.x ** 2 + p3.y ** 2 - p2.y ** 2) / (2 * (p3.y - p2.y))
        x = (b1 - b2) / (a2 - a1)
        y = a1 * x + b1
        radius = math.hypot(p1.x - x, p1.y - y)
        return Circle(x, y, radius=radius)

    def __len__(self):
        """Return number of points."""
        return len(self.points)

    def __xor__(self, other):
        """Return the list of forms that are in the union of 2 forms."""
        if type(other) == Form:
            other = [other]
        return Form.union([other, self])

    def __and__(self, other):
        """Return the list of forms that are in the intersection of 2 forms."""
        points = self.crossForm(other)
        points += [point for point in self.points if point in other]
        points += [point for point in other.points if point in self]
        if points: return Form(points)

    # Color
    def setColor(self, color):
        """Color the whole form with a new color."""
        self.point_color = color
        self.side_color = color
        self.area_color = color

    def getColor(self):
        """Return the color of the segments because it is the more widely used."""
        return self.side_color

    def setPointColor(self, color):
        """Set the color of the points of the form."""
        for point in self.points:
            point.color = color

    def getPointColor(self):
        """Return the common color of the points."""
        l = [point.color for point in self.points]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The colors of the points must be the same otherwise it makes no sense.")

    def setPointMode(self, mode):
        """Set the mode of the points."""
        for point in self.points:
            point.mode = mode

    def getPointMode(self):
        """Return the common mode of the points."""
        l = [point.mode for point in self.points]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The modes of the points must be the same otherwise it makes no sense.")

    def setPointFill(self, fill):
        """Set the fill of the points."""
        for point in self.points:
            point.fill = fill

    def getPointFill(self):
        """Return the common fill attribute of the points."""
        l = [point.fill for point in self.points]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The fill attributes of the points must be the same otherwise it makes no sense.")

    def setPointRadius(self, radius):
        """Set the radius of the points."""
        for point in self.points:
            point.radius = radius

    def getPointRadius(self):
        """Return the common radius of the points."""
        l = [point.radius for point in self.points]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The radiuses of the points must be the same otherwise it makes no sense.")

    def setPointSize(self, size):
        """Set the size of the points."""
        for point in self.points:
            point.size = size

    def getPointSize(self):
        """Return the common size of the points."""
        l = [point.size for point in self.points]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The sizes of the points must be the same otherwise it makes no sense.")

    def setPointWidth(self, width):
        """Set teh width of the points."""
        for point in self.points:
            point.width = width

    def getPointWidth(self):
        """Return the common width of the points."""
        l = [point.width for point in self.points]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The widths of the points must be the same otherwise it makes no sense.")

    def setSegmentColor(self, color):
        """Set teh color of the segments."""
        for segment in self.segments:
            segment.color = color

    def getSegmentColor(self):
        """Return the common color of the segments."""
        l = [segment.color for segment in self.segments]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The colors of the points must be the same otherwise it makes no sense.")

    def setSegmentWidth(self, width):
        """Set the width of the segments."""
        for segment in self.segments:
            segment.width = width

    def getSegmentWidth(self):
        """Return the common width of the segments."""
        l = [segment.width for segment in self.segments]
        if l.count(l[0]) == len(l):
            return l[0]
        else:
            raise ValueError("The widths of the segments must be the same otherwise it makes no sense.")

    getCrossPoints = crossSelf

    sides = segments = property(getSegments, setSegments, doc="Represents the segments.")
    vectors = property(getVectors, setVectors)
    center = property(getCenter, setCenter, doc="Center of the form.")
    centroid = property(getCentroid, setCentroid, doc="Centroid of the form.")
    color = property(getColor, setColor, doc="Segment color.")
    cross_points = property(getCrossPoints, doc="Points of intersection of the sides of the form itself.")
    point_color = property(getPointColor, setPointColor, doc="Set the color of the points.")
    point_mode = property(getPointMode, setPointMode, doc="Mode of the points.")
    point_fill = property(getPointFill, setPointFill, doc="Fill attribute of the circles representing the points.")
    point_radius = property(getPointRadius, setPointRadius, doc="Radius of the circles representing the point.")
    point_size = property(getPointSize, setPointSize, doc="Size of the cross that represents the point.")
    point_width = property(getPointWidth, setPointWidth, doc="Width of the cross that represents the point.")
    segment_color = property(getSegmentColor, setSegmentColor, doc="Color of the segments.")
    segment_width = property(getSegmentWidth, setSegmentWidth, doc="Width of the segments.")


class Circle:
    @classmethod
    def random(cls, borns=[-1, 1], radius_borns=[0, 1], **kwargs):
        """Create a random circle."""
        x = random.uniform(*borns)
        y = random.uniform(*borns)
        r = random.uniform(*radius_borns)
        return cls(x, y, radius=r, **kwargs)

    @classmethod
    def createFromPointAndRadius(cls, point, radius, **kwargs):
        """Create a circle from point."""
        return cls(*point, radius=radius, **kwargs)

    def __init__(self, *args, radius, fill=False, color=mycolors.WHITE, border_color=None, area_color=None,
                 center_color=None, radius_color=None, radius_width=1, text_color=None, text_size=20):
        """Create a circle object using x, y and radius and optional color and width."""
        if len(args) == 1: args = args[0]
        self.position = args
        self.radius = radius
        self.fill = fill
        if color:
            if not border_color: border_color = color
            if not area_color: area_color = color
            if not radius_color: radius_color = color
            if not text_color: text_color = color
        self.border_color = border_color
        self.area_color = area_color
        self.center_color = center_color
        self.radius_color = radius_color
        self.radius_width = radius_width
        self.text_color = text_color
        self.text_size = text_size

    def __str__(self):
        """Str representation of a circle."""
        return "c(pos:" + str(self.position) + ",rad:" + str(self.radius) + ")"

    def __contains__(self, position):
        """Determine if a point is in a circle."""
        return sum([(c1 - c2) ** 2 for (c1, c2) in zip(self.position, position)]) <= self.radius

    def getX(self):
        """Return the x component of the circle."""
        return self.position[0]

    def setX(self, value):
        """Set the x component of the circle."""
        self.position[0] = value

    def getY(self):
        """Return the y component of the circle."""
        return self.position[1]

    def setY(self, value):
        """Set the y component of the circle."""
        self.position[1] = value

    def getPoint(self):
        """Return the point that correspond to the center of the circle."""
        return Point(*self.position)

    def setPoint(self, point):
        """Set the center point of the circle by changing the position of the circle."""
        self.position = point.position

    def getR(self):
        """Return the radius."""
        return self.radius

    def setR(self, radius):
        """Set the radius to the given radius."""
        self.radius = radius

    x = property(getX, setX, "Allow the user to manipulate the x component easily.")
    y = property(getY, setY, "Allow the user to manipulate the y component easily.")
    r = property(getR, setR, "Abbreviation of the radius")
    center = point = property(getPoint, setPoint, "Allow the user to manipulate the point easily.")

    def show(self, window, color=None, border_color=None, area_color=None, fill=None):
        """Show the circle on screen using the window."""
        if color:
            if not area_color: area_color = color
            if not border_color: border_color = color
        if not border_color: border_color = self.border_color
        if not area_color: area_color = self.area_color
        if not fill: fill = self.fill
        window.draw.circle(window.screen, border_color, self.position, self.radius, fill)

    def showCenter(self, window, color=None, mode=None):
        """Show the center of the screen."""
        if not color: color = self.center_color
        if not mode: mode = self.center_mode
        self.center.show(window, mode=mode, color=color)

    def showText(self, window, text, color=None, size=None):
        """Show a text next to the circle."""
        if not color: color = self.text_color
        if not size: size = self.text_size
        self.center.showText(window, text, color=color, size=size)

    def showRadius(self, window, color=None, width=None):
        """Show the radius of the circle."""
        if not color: color = self.radius_color
        if not width: width = self.radius_width
        vector = Vector.createFromPolar(self.radius, 0, color=color)
        vector.show(window, self.center, width=width)
        vector.showText(surface, self.center, "radius", size=20)

    def __call__(self, n):
        """Return the main components of the circle."""
        perimeter = 2 * math.pi
        return Point(math.cos(n / perimeter), math.sin(n / perimeter))

    def isCrossingCircle(self, other):
        """Determine if two circles are crossing."""
        vector = Vector.createFromTwoPoints(self.center, other.center)
        return vector.norm < self.radius + other.radius

    def crossCircle(self, other):
        """Return the intersections points of two circles if crossing else
        return None."""
        if self.isCrossingCircle(other):
            s = Segment(self.center, other.center)
            m = s.middle
            n = math.sqrt(self.radius ** 2 - (s.norm / 2) ** 2)
            a = s.angle + math.pi / 2
            v1 = Vector.createFromPolar(n, a)
            v2 = Vector.createFromPolar(n, -a)
            p1 = v1(m)
            p2 = v2(m)
            return [p1, p2]

    def getArea(self):
        """Return the area of a circle using basic geometry."""
        return math.pi * self.radius ** 2

    area = property(getArea)


if __name__ == "__main__":
    from mycontext import Context

    surface = Context(name="Abstract Demonstration", fullscreen=True)

    p1 = Point(10, 0, radius=0.05, color=mycolors.YELLOW)
    p2 = Point(20, 20, radius=0.05, color=mycolors.YELLOW)
    # origin=Point(0,0)
    origin = Point.origin()

    l1 = HalfLine(origin, math.pi / 4)
    l2 = Line(p1, math.pi / 2, correct=False)
    s1 = Segment(p1, p2)
    print(Point.null())

    while surface.open:
        # Surface specific commands
        surface.check()
        surface.control()
        surface.clear()
        surface.show()

        # Actions
        l1.rotate(0.01, p2)
        l2.rotate(-0.02, p1)
        s1.rotate(0.03)

        p = l1 | l2

        o = Point(0, 0)
        p3 = l2.projectPoint(o)
        f = Form([p1, p2, p3], area_color=mycolors.RED, fill=True)

        # Show
        surface.draw.window.print("l1.angle: " + str(l1.angle), (10, 10))
        surface.draw.window.print("l2.angle: " + str(l2.angle), (10, 30))
        surface.draw.window.print("f.area: " + str(f.area), (10, 50))

        f.show(surface)
        f.center.show(surface)

        s1.show(surface)

        o.show(surface, color=mycolors.GREY)
        o.showText(surface, "origin")

        p3.showText(surface, "origin's projection")
        p3.show(surface, color=mycolors.LIGHTGREY)

        if p:
            p.show(surface, color=mycolors.RED)
            p.showText(surface, "intersection point", color=mycolors.RED)

        p1.show(surface)
        p1.showText(surface, "p1")

        p2.show(surface)
        p2.showText(surface, "p2")

        l1.show(surface, color=mycolors.GREEN)
        l1.point.show(surface, color=mycolors.LIGHTGREEN, mode="cross", width=3)
        l1.vector.show(surface, l1.point, color=mycolors.LIGHTGREEN, width=3)

        l2.show(surface, color=mycolors.BLUE)
        l2.point.show(surface, color=mycolors.LIGHTBLUE, mode="cross", width=3)
        l2.vector.show(surface, l2.point, color=mycolors.LIGHTBLUE, width=3)

        # Flipping the screen
        surface.flip()
