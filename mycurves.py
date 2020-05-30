from myabstract import Point,Segment,Form,Line

import random
import mycolors
import itertools

class Trajectory:
    @classmethod
    def random(cls,n=5,**kwargs):
        """Create a random trajectory of n points."""
        points=[Point.random() for i in range(n)]
        return cls(points,**kwargs)

    @classmethod
    def createFromTuples(cls,tuples,**kwargs):
        """Create a trajectory using tuples and optional arguments."""
        pts=[Point(*t) for t in tuples]
        return cls(pts,**kwargs)

    def __init__(self,points,segment_color=mycolors.WHITE,point_color=mycolors.WHITE):
        """Create a trajectory using the list of points."""
        self.points=points
        self.segment_color=segment_color
        self.point_color=point_color

    def __call__(self,t):
        """Evaluate the trajectory by t between 0 and 1."""
        if len(self.points)<=1:
            raise Exception("It is impossible to interpolate without at least 2 points.")
        length=self.length
        ns=len(self.segments)
        tsl=0
        for i in range(ns):
            s=Segment(self.points[i],self.points[i+1])
            if t*length-tsl<=s.length:
                st=(t*length-tsl)/s.length
                return tuple(s(st).components)
            tsl+=s.length
        return tuple(s(1)) #Its a fix that isn't always true

    def __str__(self):
        """Return the string representation of a trajectory."""
        return "tj("+",".join(map(str,self.points))+")"

    def show(self,surface,**kwargs):
        """Show the trajectory on the surface."""
        self.showPoints(surface,**kwargs)
        self.showSegments(surface,**kwargs)

    def showPoints(self,surface,color=None):
        """Show the point on the surface."""
        if not color: color=self.point_color
        for point in self.points:
            point.show(surface,color=color)

    def showSegments(self,surface,color=None):
        """Show the segments on the surface."""
        if not color: color=self.segment_color
        for segment in self.segments:
            segment.show(surface,color=color)

    def getSegments(self):
        """Return the segments of the trajectory of the curve."""
        return [Segment(self.points[i],self.points[i+1]) for i in range(len(self.points)-1)]

    def getLength(self):
        """Return the length of the trajectory."""
        return sum([segment.length for segment in self.segments])

    def sample(self,n,include=True):
        """Sample n points of the trajectory at equal distance.
        It is also possible to include the last one if wanted."""
        return [self(i/n) for i in range(n+int(include))]

    def fastSample(self,n,include=True):
        """Sample n points of the trajectory at equal distance but fast.
        It is also possible to include the last one if wanted."""
        length=self.length
        ns=len(self.segments)
        k=0
        l=[]
        tsl=0
        for i in range(ns):
            s=Segment(self.points[i],self.points[i+1])
            if t*length-tsl<=s.length:
                st=(t*length-tsl)/s.length
                l.append(tuple(s(st).components))
                k+=1
                t=k/n
            tsl+=s.length
        if include:
            l.append(self.points[-1])
        return l

    def sampleSegments(self,n,include=True):
        """Sample n points for each segment of the trajectory."""
        points=[]
        segments=self.segments
        for i in range(len(segments)):
            points+=segments[i].sample(n,include=False)
        if include and len(self.points)>1: points.append(self.points[-1])
        return points

    def getCenter(self):
        """Return the center (or middle) of the trajectory."""
        return self(1/2)

    def setCenter(self):
        """Set the center (or middle) of the trajectory."""
        center=self.center
        for n in range(len(self.points)):
            self.points[n]-=center

    segments=property(getSegments)
    length=property(getLength)
    center=property(getCenter)

class BezierCurve:
    def __init__(self,points,point_color=mycolors.WHITE,segment_color=mycolors.WHITE):
        """Create a bezier curve object using 3 points."""
        self.points=points
        self.segment_color=segment_color
        self.point_color=point_color

    def __call__(self,t):
        """Return the point."""
        points=self.points
        if len(points)==0:
            return None
        elif len(points)==1:
            return points[0]
        elif len(points)==2:
            segment=Segment(points[0],points[1])
            point=segment.center()
            return point
        elif len(points)==3:
            p1,p2,p3=points
            s1=Segment(p1,p2)
            s2=Segment(p2,p3)
            ps1=s1(t)
            ps2=s2(t)
            s=Segment(ps1,ps2)
            return s(t)
        else:
            while len(points)>3:
                segments=[Segment(points[i],points[i+1]) for i in range(len(points)-1)]
                points=[segment(t) for segment in segments]
            b=BezierCurve(points)
            return b(t)

    def show(self,surface,p=50):
        """Show the bezier curve on the surface."""
        points=[self(i/p) for i in range(p+1)]
        segments=[Segment(points[i],points[i+1]) for i in range(p)]
        self.showPoints(surface,points)
        self.showSegments(surface,segments)

    def getConstruction(self,t):
        """Return the construction segments of the form."""
        points=self.points
        construction=[]
        while len(points)>=2:
            segments=[Segment(points[i],points[i+1]) for i in range(len(points)-1)]
            points=[segment(t) for segment in segments]
            construction.append(segments)
        return construction

    def showConstruction(self,surface,t):
        """Show the construction of the form at the t position."""
        construction=self.getConstruction(t)
        l=len(construction)
        for i in range(l):
            k=255*(i+1)/l
            color=(0,0,k)
            for segment in construction[i]:
                #print(segment)
                segment.show(surface,color=color,width=2)

    def showPoints(self,surface,points,color=None):
        """Show the points on the surface."""
        if not color: color=self.point_color
        for point in points:
            point.show(surface,color=color,radius=0.01)

    def showSegments(self,surface,segments,color=None):
        """Show the segments on the surface."""
        if not color: color=self.segment_color
        for segment in segments:
            segment.show(surface,color=color,width=2)

    def getSegments(self):
        """Return the segments of the trajectory of the curve."""
        return [Segment(points[i],points[i+1]) for i in range(len(self.points)-1)]

    segments=property(getSegments)

class BezierForm(Form):
    def show(self,context):
        """Show the curved form on the screen."""
        self.bezier.show(context)

    @property
    def bezier(self):
        """Return the bezier curve of the form."""
        return BezierCurve(self.points+[self.points[0]])



class Arrow(BezierCurve):
    """Join 2 objects with an arrow."""
    def __init__(self,points,point_color=mycolors.WHITE,segment_color=mycolors.WHITE,vector_color=mycolors.WHITE):
        super().__init__(self,points,point_color,segment_color,vector_color)

    def show(self,surface,p=50):
        """Show the arrow on the screen."""
        points=[self(i/p) for i in range(p)] #p=p+1 ?
        segments=[Segment(points[i],points[i+1]) for i in range(p-1)]
        vectors=[Vector(points[i],points[i+1]) for i in range(0,p-1,5)]
        self.showPoints(surface,points)
        self.showSegments(surface,segments)
        self.showVectors(surface,vectors)

    def showVectors(self,surface,vectors,color=None):
        """Show the vectors on the surface."""
        if not color: color=self.vector_color
        for vector in vectors:
            vector.show(surface,color=color)




if __name__=="__main__":
    from mycontext import Surface
    surface=Surface(name="Curves demonstration")
    l=10
    points=[Point(2*x,random.randint(-5,5)) for x in range(l)]
    t=Trajectory(points,segment_color=mycolors.GREEN)
    b=BezierCurve(points,segment_color=mycolors.RED)
    #st=t.sampleSegments(3)
    #t1=Trajectory(st,segment_color=mycolors.BLUE)
    #print(b.points[-1])
    #print(b(1))
    #print(b.segments[-1])
    #c=CurvedForm(points)
    n=0
    ncp=50 #number construction points

    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()

        Point.turnPoints([1/1000 for i in range(l)],points)
        n=(n+1)%(ncp+1)
        b.showConstruction(surface,n/ncp)

        t.show(surface)
        b.show(surface)

        p1=b(n/ncp)
        p2=Point(*t(n/ncp))

        #l1=Line.createFromTwoPoints(p1,p2)

        p1.show(surface,color=mycolors.YELLOW,radius=0.1,fill=True)
        p2.show(surface,color=mycolors.YELLOW,radius=0.1,fill=True)
        #l1.show(surface,color=mycolors.LIGHTGREY)


        surface.flip()
