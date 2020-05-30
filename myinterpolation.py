"""
The goal of this program is to make an interpolation of the points of any
curve in order to make it a parametric function.


There are 2 main types of interpolations:
- Polynomial Interpolation:
- Bezier Interpolation:
"""

#Polynomial Interpolation
from polynomial import Polynomial

#Pseudo Bezier Interpolation
from mycurves import BezierCurve
from myabstract import Line,Point
#additional imports for showing the interpolations more easily
from mycurves import Trajectory
import mycolors

#Deprectated function
def directInterpolation(points,t):
    x=[pt[0] for pt in points]
    y=[pt[1] for pt in points]
    plx=Polynomial.createFromInterpolation(range(len(x)),x)
    ply=Polynomial.createFromInterpolation(range(len(y)),y)
    l=len(pts)
    mst=100

    # Creation of the points
    # pts=[(random.uniform(xmin,xmax),random.uniform(ymin,ymax)) for i in range(n)]

    # # """ Tests:
    # # Calculations for n points in dimension 2:
    #
    # x=[pt[0] for pt in pts]
    # y=[pt[1] for pt in pts]
    # plx=Polynomial.createFromInterpolation(range(len(x)),x)
    # ply=Polynomial.createFromInterpolation(range(len(y)),y)
    # print(plx)
    # print(ply)
    # l=len(pts)
    # mst=100
    # npts=[(plx(l*st/mst),ply(l*st/mst)) for st in range(mst)]
    # grapher=Grapher(context,functions=[plx,ply])
    # """


class Interpolation:
    """Base class of all interpolations."""

    def __init__(self,points,create=True):
        """Create the interpolation using a list of n-dimensional points."""
        self.points=points
        if create: self.create()

    def create(self):
        """Create the necessary attributes for the interpolation.
        This method is to be overloaded."""
        pass

    def sample(self,n):
        """Make a sample of the interpolation for n points."""
        m=n-1
        return [self(t/m) for t in range(n)]

    def __str__(self):
        """Return the string representation of the interpolation."""
        return "Itp("+",".join(map(str,self.points))+")"


class ExtraInterpolation(Interpolation):
    """Extra features for interpolations."""

    def getSegments(self):
        """Return the segments formed by the points."""
        return [Segment(self.points[i],self.points[i+1]) for i in range(len(self.points)-1)]

    def getTrajectory(self):
        """Return the trajectory associated with the points of the interpolation."""
        return Trajectory.createFromTuples(self.points)

    def getPointsType(self):
        """Return the points under a point type instead of just a tuple type."""
        return [Point(*p) for p in self.points]

    def getPoint(self,t,**kwargs):
        """Return the point of position t in the parametric function."""
        return Point(*self(t),**kwargs)

    segments=property(getSegments)
    trajectory=property(getTrajectory)
    points_type=property(getPointsType)


class VisualInterpolation(Interpolation):
    """Visual features for interpolation, this class allows to show an
    interpolation on a graphical context."""

    def __init__(self,points,
                    color=mycolors.RED,
                    point_color=mycolors.LIGHTRED,
                    trajectory_color=mycolors.GREEN,
                    **kwargs):
        """Create a visual interpolation."""
        self.color=color
        self.point_color=point_color
        self.trajectory_color=trajectory_color
        Interpolation.__init__(self,points,**kwargs)

    def show(self,context,n,color=None):
        """Show the polynomial interpolation by sampling the function using:
        -n: the number of points
        -context:the context in which the interpolation is shown."""
        if not color: color=self.color
        points=self.sample(n)
        context.draw.lines(context.screen,color,points,width=1,connected=False)

    def showTrajectory(self,context,color=None):
        """Show the trajectory defined by the points of the interpolation."""
        if not color: color=self.trajectory_color
        Trajectory.createFromTuples(self.points).show(context,color=color)


class PolynomialInterpolation(VisualInterpolation,ExtraInterpolation):
    """Make an interpolation using the lagrangian polynomial interpolator
    over list of n-dimensional points."""

    def create(self):
        """Create the components useful for the interpolation which are the
        split components and the lagrangian polynomials."""
        self.createComponents()
        self.createPolynomials()

    def createComponents(self):
        """Split its components of each point in separate lists."""
        self.components=[[pt[i] for pt in self.points] for i in range(len(self.points[0]))]

    def createPolynomials(self):
        """Create its polynomials using its components."""
        lpts=len(self.points)
        self.polynomials=[Polynomial.createFromInterpolation(range(lpts),c) for c in self.components]

    def __call__(self,t):
        """Evaluate the parametric interpolation for the input 't' between 0 and 1."""
        lcps=len(self.components)
        lpts=len(self.points)-1
        return tuple([self.polynomials[i](lpts*t) for i in range(lcps)])

class PseudoBezierInterpolation(VisualInterpolation):
    """Make an interpolation using the bezier interpolation over a list of
    n-dimensional points."""

    def create(self):
        """Create the lines, the intruding points and the bezier curves."""
        self.createLines()
        self.createIntrudingPoints()
        self.createBezierCurves()

    def createLines(self):
        """Create the lines of the duos of consecutive points."""
        l=len(self.points)
        lines=[Line.createFromTwoPoints(self.points[i],self.points[i+1]) for i in range(l-1)]

    def createIntrudingPoints(self):
        """Create the points of intersection formed by some of the lines."""
        l=len(lines)
        intruding_points=[lines[i].crossLine(lines[i+1]) for i in range(l-1)]

    def __call__(self,t):
        """Evaluate the parametric interpolation for the input 't' between 0 and 1."""
        l=len(lines)
        intruding_points=[lines[i].crossLine(lines[i+1]) for i in range(l-1)]
        bezier_curves=[]
        for i in range(l):
            bezier_points=[self.points[i],self.intruding_points[i],self.points[i+1]]
            b=BezierCurve(bezier_points)
            bezier_curves.append(b)



if __name__=="__main__":
    #To show the points
    from mycontext import Context
    import mycolors
    #To create the points
    import random

    context=Context(name="Interpolation Demonstration")

    #Parameters
    h=1; w=1; xmin,xmax,ymin,ymax=[-w,w,-h,h] #corners
    l=5 #number of points
    n=0 #number of steps
    m=100 #max number of steps

    #Final version
    #pts=[Point.random() for i in range(10)]
    pts=[Point(2*x,random.randint(-5,5)) for x in range(l)]
    interpolation=PolynomialInterpolation([p.components for p in pts])
    interpolation.color
    npts=interpolation.sample(200)

    #Setting the console
    context.console.append(["interpolation: "+str(interpolation),"trajectory: "+str(interpolation.trajectory)])


    #Main loop of the context
    while context.open:
        #Update the context
        context.check()
        context.control()
        context.clear()
        context.show()

        #Update data components
        Point.turnPoints([1/100/l for i in range(l)],pts)
        #trajectory=Trajectory(pts,mycolors.GREEN)
        interpolation=PolynomialInterpolation([p.components for p in pts])
        npts=interpolation.sample(200) #Sample 200 points by interpolation


        #Additional features
        n=(n+1)%(m+1)
        c1=interpolation(n/m)
        pt1=Point(*c1,radius=0.1,color=mycolors.lighten(mycolors.RED,2),fill=True)
        c2=interpolation.trajectory(n/m)
        pt2=Point(*c2,radius=0.1,color=mycolors.lighten(mycolors.GREEN,2),fill=True)

        #Show visual components
        pt1.show(context)
        pt2.show(context)
        interpolation.show(context,200)
        interpolation.showTrajectory(context)

        #Console
        context.showConsole()

        #Flip the context
        context.flip()
