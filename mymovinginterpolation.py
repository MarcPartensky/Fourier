# Show interpolations being made while moving the points.

# Imports
from myinterpolation import PolynomialInterpolation
from mycurves import Trajectory
from mycontext import Context
from myabstract import Point
import mycolors
import random

context = Context()
l = 10
points = [Point(2 * x, random.randint(-5, 5)) for x in range(l)]
n = 0
ncp = 200  # number construction points

while context.open:
    context.check()
    context.control()
    context.clear()
    context.show()

    n = (n + 1) % (ncp + 1)
    Point.turnPoints([1 / 1000 for i in range(l)], points)

    pi1 = PolynomialInterpolation(points)
    pi2 = PolynomialInterpolation(points)
    # pi2.createPolynomialsRespectingDistance()
    ti = Trajectory(points)
    p1 = Point(*pi1(n / ncp))
    p2 = Point(*pi2(n / ncp))
    p3 = Point(*ti(n / ncp))

    # l1=Line.createFromTwoPoints(p1,p2)

    pi1.show(context, n=200)
    ti.show(context)
    p1.show(context, color=mycolors.YELLOW, radius=0.1, fill=True)
    p2.show(context, color=mycolors.YELLOW, radius=0.1, fill=True)
    p3.show(context, color=mycolors.YELLOW, radius=0.1, fill=True)

    context.flip()
