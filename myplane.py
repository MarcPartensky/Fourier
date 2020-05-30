from mywindow import Window
from pygame.locals import *

import math
import numpy as np
import mycolors

class Plane:
    def __init__(self,theme={},view=None):
        """Create a plane using optionals theme and view."""
        self.createTheme(theme)
        self.createView(view)

    def createTheme(self,theme={}):
        """Initializes the position and the colors for the view of the plane using optional theme."""
        if not "background"  in theme: theme["background"]  = (0,0,0)
        if not "grid color"  in theme: theme["grid color"]  = (20,20,20)
        if not "grid nscale" in theme: theme["grid nscale"] = 3
        if not "show scale"  in theme: theme["show scale"]  = False
        if not "show origin" in theme: theme["show origin"] = False
        if not "show units" in theme:  theme["show units"]  = False
        self.theme=theme

    def createView(self,view=None):
        """Initializes the position and the units for the view of the plane using optional view."""
        """View must be a list of length 2."""
        if view:
            self.position= view[0]
            self.units=    view[1]
            self.default_position= view[0][:]
            self.default_units=    view[1][:]
        else:
            self.default_position= [ 0, 0]   #position of the center of the view in the plane's coordonnates
            self.default_units=    [40,40]   #units of the conversion from window/plane
            self.position=         [ 0, 0]
            self.units=            [40,40]   #units can be handled [-10**-14,10**307] before bugging or crashing

    def __call__(self,window): #The main loop must be redefined by the client and not the functions called within it.
        """Main loop of the plane."""
        window.rename("Plane")
        while window.open:
            window.check()
            self.control(window)
            self.clear(window)
            self.show(window)
            self.flip(window)

    def contains(self,position,window):
        """Determine if a position is in the visible screen."""
        x,y=position
        xmin,ymin,xmax,ymax=self.getCorners(window)
        return (xmin<=x<=xmax) and (ymin<=y<=ymax)

    def flip(self,window):
        """Flip the plane's window."""
        window.flip()

    def clear(self,window,color=None):
        """Clear the plane."""
        if not color: color=self.theme["background"]
        window.clear(color)

    def control(self,window):
        """Control the view of the plane."""
        self.controlZoom(window)
        self.controlPosition(window)

    def controlZoom(self,window):
        """Control the zoom of the plane."""
        keys=window.press()
        ux,uy=self.units
        if keys[K_RSHIFT]:
            self.zoom([1.1,1.1])
        if keys[K_LSHIFT]:# and (ux>2 and uy>2): #The second condition is useless but prevent the user from watching errors due to too far zooming out.
            self.zoom([0.9,0.9])

    def controlPosition(self,window):
        """Control the position of the plane."""
        keys=window.press()
        if keys[K_RETURN]:
            self.units=    self.default_units[:]
            self.position= self.default_position[:]
        ux,uy=self.units
        wsx,wsy=window.size
        x,y=self.position
        k=50 #Allow the user to move in the grid a reasonable velocity.
        if keys[K_LEFT]:
            x-=wsx/ux/k
        if keys[K_RIGHT]:
            x+=wsx/ux/k
        if keys[K_DOWN]:
            y-=wsy/uy/k
        if keys[K_UP]:
            y+=wsy/uy/k
        self.position=[x,y]

    def getUnitsColor(self,scale,ascale,color=None):
        """Get the color given a x position."""
        if not color: color=self.theme["grid color"]
        dscale=scale-ascale
        return [c*(2**dscale) for c in color]


    def show(self,window):
        """Show the elements on screen using the window."""
        self.showGrids(window)

    def showAll(self):
        self.showGrids(window)
        if self.theme["show scale"]:
            window.print("scale:"+str(self.getScale(window)),(10,10),size=20)
        if self.theme["show origin"] and self.contains((0,0),window):
            self.showOrigin(window)
        if self.theme["show units"]:
            window.print("units:"+str(self.units),(10,10),size=20)
        #self.showUnits(window) #Does not work for now

    def showOrigin(self,window,color=mycolors.WHITE,radius=3):
        """Show the origin of the plane."""
        position=self.getToScreen([0,0],window)
        window.draw.circle(window.screen,color,position,radius,0)


    def showUnits(self,window): #Not working because of error of synchronisation between text base system and normal window base.
        """Show the unit of the grid using the window."""
        px,py=self.position
        wsx,wsy=window.size
        ux,uy=self.units
        nx=int(wsx/ux)
        ny=int(wsy/uy)
        for y in range(int(-ny+py),int(ny+py)+1,10):
            for x in range(int(-nx+px),int(nx+px)+1,10):
                X,Y=self.getToScreen([x,y],window)
                window.print(str([x,y]),[X,Y],size=20)

    def showGrids(self,window,nscale=None):
        """Show the grid using the window and optional scales."""
        ascale=self.getScale(window) #ascale like actual_scale
        for scale in self.getScales(window,nscale,ascale):
            self.showGrid(window,scale)

    def getScales(self,window,nscale=None,scale=None):
        """Return the scales ."""
        if not nscale: nscale=self.theme["grid nscale"]
        if not scale: scale=self.getScale(window)
        l=[scale-i for i in range(nscale)]
        l.reverse()
        return l

    def getScale(self,window):
        """Return the actual scale of the displayed screen."""
        ux,uy=self.units
        wsx,wsy=window.size
        uwx,uwy=wsx/ux,wsy/uy
        uw=min(uwx,uwy)
        return int(math.log(uw)/math.log(10))

    def showGrid(self,window,scale=0,ascale=None):
        """Show the grid using the window."""
        if not ascale: ascale=self.getScale(window)
        xmin,ymin,xmax,ymax=self.getCorners(window) #Get the corners of the plane
        #For each line find the begining and the end in the plane's coordonnates then convert it into screen's coordonnates.
        for x in self.arange(xmin,xmax,scale):
            color=self.getUnitsColor(scale,ascale)
            start=self.getToScreen([x,ymin],window)
            end=  self.getToScreen([x,ymax],window)
            window.draw.line(window.screen,color,start,end,1)
        #Repeat the process for the y component
        for y in self.arange(ymin,ymax,scale):
            color=self.getUnitsColor(scale,ascale)
            start=self.getToScreen([xmin,y],window)
            end=  self.getToScreen([xmax,y],window)
            window.draw.line(window.screen,color,start,end,1)

    def arange(self,min,max,scale):
        """Return the list of values that are between min and max, separated by unit."""
        min=np.around(min,-scale)
        max=np.around(max,-scale)
        return np.arange(min,max,10**scale)

    def zoom(self,zoom):
        """Allow the user to zoom into the plane."""
        for i in range(2):
            self.units[i]*=zoom[i]

    def xZoom(self,zoom):
        """Allow the user to zoom into the plane according to the x component."""
        self.units[0]*=zoom

    def yZoom(self,zoom):
        """Allow the user to zoom into the plane according to the y component."""
        self.units[1]*=zoom

    def getToScreen(self,position,window):
        """Return a screen position using a position in the plane."""
        x,y=position
        px,py=self.position
        ux,uy=self.units
        wsx,wsy=window.size
        x=int((x-px)*ux+wsx/2)
        y=int(wsy/2-(y-py)*uy)
        return [x,y]

    def getAllToScreen(self,positions,window):
        """Return the list of screen positions using the list of plane positions."""
        screen_positions=[]
        for position in positions:
            screen_positions.append(self.getToScreen(position,window))
        return screen_positions

    def getFromScreen(self,position,window):
        """Return a plane position using a position in the screen."""
        x,y=position
        px,py=self.position
        ux,uy=self.units
        wsx,wsy=window.size
        x=(x-wsx/2)/ux+px
        y=(wsy/2-y)/uy+py
        return [x,y]

    def getAllFromScreen(self,position,window):
        """Return the list of plane positions using the list of screen positions."""
        plane_positions=[]
        for position in positions:
            planes_positions.append(self.getFromScreen(position,window))
        return plane_positions

    def getCorners(self,window):
        """Return the corners of the present view."""
        wsx,wsy=window.size
        ux,uy=self.units
        x,y=self.position
        lx,ly=wsx/ux,wsy/uy
        return [x-lx/2,y-ly/2,x+lx/2,y+ly/2]

        mx,my=self.getFromScreen([0,wsy],window)
        Mx,My=self.getFromScreen([wsx,0],window)
        return (mx,my,Mx,My)

    def setCorners(self,corners,window):
        """Change the actual corners of the plane by changing its position and units."""
        xmin,ymin,xmax,ymax=corners
        wsx,wsy=window.size
        self.position=[xmin+(xmax-xmin)/2,ymin+(ymax-ymin)/2]
        self.units=[wsx/(xmax-xmin),wsy/(ymax-ymin)]

    #The following functions are static methods

    def getCornersFromCoordonnates(coordonnates):
        """Return the corners (top_left_corner,bottom_right_corner) using the coordonnates (position+size)."""
        """[x,y,sx,sy] -> [mx,my,Mx,My]"""
        x,y,sx,sy=coordonnates
        mx,my=x-sx/2,y-sy/2
        Mx,My=x+sx/2,y+sy/2
        corners=(mx,my,Mx,My)
        return corners

    def getCoordonnatesFromCorners(corners):
        """Return the coordonnates (position+size) using the corners (top_left_corner,bottom_right_corner)."""
        """[mx,my,Mx,My] -> [x,y,sx,sy]"""
        mx,my,Mx,My=corners
        sx,sy=Mx-mx,My-my
        x,y=mx+sx/2,my+sy/2
        coordonnates=(x,y,sx,sy)
        return coordonnates

    def getCoordonnatesFromRect(rect):
        """Return the coordonnates (position,size) using the rect (top_left_corner,size)."""
        """[x,y,sx,sy] -> [mx,my,sx,sy]"""
        mx,my,sx,sy=rect
        x,y=mx+sx/2,my+sy/2
        coordonnates=[x,y,sx,sy]
        return coordonnates

    def getRectFromCoordonnates(coordonnates):
        """Return the rect (top_left_corner,size) using the coordonnates (position,size)."""
        """[mx,my,sx,sy] -> [x,y,sx,sy]"""
        x,y,sx,sy=coordonnates
        mx,my=x-sx/2,y-sy/2
        rect=[mx,my,sx,sy]
        return rect

    def getRectFromCorners(corners):
        """Return the rect (top_left_corner,size) using the corners (top_left_corner,bottom_right_corner)."""
        """[mx,my,Mx,My] -> [mx,my,sx,sy]"""
        mx,my,Mx,My=corners
        sx,sy=Mx-mx,My-my
        rect=[mx,my,sx,sy]
        return rect

    def getCornersFromRect(rect):
        """Return the (top_left_corner,bottom_right_corner) using the corners rect (top_left_corner,size)."""
        """[mx,my,Mx,My] -> [mx,my,sx,sy]"""
        mx,my,sx,sy=rect
        Mx,My=mx+sx,my+sy
        corners=[mx,my,Mx,My]
        return corners



if __name__=="__main__":
    window=Window(fullscreen=False)
    theme={"background":(0,0,0),"show scale":True,"show origin":True,"grid color":(200,200,200)}
    plane=Plane(theme)
    #plane.units=[1/10**300,1/10**300]
    plane(window)
