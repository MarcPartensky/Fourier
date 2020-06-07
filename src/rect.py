import random


class Rect:
    """Define a pure and simple rectangle."""

    # Class methods
    @classmethod
    def cross(cls, r1, r2):
        """Determine the rectangle resulting of the intersection of two rectangles."""
        if r1.xmax < r2.xmin or r1.xmin > r2.xmax: return
        if r1.ymax < r2.ymin or r1.ymin > r2.ymax: return
        xmin = max(r1.xmin, r2.xmin)
        ymin = max(r1.ymin, r2.ymin)
        xmax = min(r1.xmax, r2.xmax)
        ymax = min(r1.ymax, r2.ymax)
        return Rect.createFromCorners(xmin, ymin, xmax, ymax)

    @classmethod
    def random(cls, borns=[-1, 1], borns_size=[0, 1]):
        """Create a random rect."""
        x = random.uniform(*borns)
        y = random.uniform(*borns)
        sx = random.uniform(*borns_size)
        sy = random.uniform(*borns_size)
        return cls(x, y, sx, sy)

    @classmethod
    def createFromCorners(cls, *corners):
        """Create a rectangle."""
        x, y, xm, ym = corners
        w = xm - x
        h = ym - y
        return cls(x + w / 2, y + h / 2, w, h)

    @classmethod
    def createFromCoordinates(cls, *coordinates):
        """Create a rect using the coordinates."""
        return cls(*coordinates)

    @classmethod
    def createFromRect(cls, *rect):
        """Create a rect from an unpacked pygame.rect"""
        l, r, w, h = rect
        return cls(l + w / 2, r + h / 2, w, h)

    def __init__(self, x, y, w, h):
        """Create a rectangle using its x, y, width, and height, the
        x and y components correspond to the center of the rectangle."""
        self.components = [x, y, w, h]

    def __getitem__(self, index):
        return self.components[index]

    def __setitem__(self, key, value):
        self.components[key] = value

    x = property(lambda cls: cls.__getitem__(0), lambda cls, value: cls.__setitem__(0, value),
                 doc="x component of the center")
    y = property(lambda cls: cls.__getitem__(1), lambda cls, value: cls.__setitem__(1, value),
                 doc="y component of the center")

    def getSize(self):
        return [self.w, self.h]

    def setSize(self, size):
        self.w, self.height = size

    size = property(getSize, setSize)

    def getPosition(self):
        return [self.x, self.y]

    def setPosition(self, position):
        self.x, self.y = position

    center = position = property(getPosition, setPosition)

    def __str__(self, n=2):
        """Return the string representation of a rect."""
        r = self.__round__(n)
        return "Rect(x=" + str(r.x) + ",y=" + str(r.y) + ",w=" + str(r.w) + ",h=" + str(r.h) + ")"

    def __round__(self, n=2):
        """Round the components of the rect."""
        x = round(self.x, n)
        y = round(self.y, n)
        w = round(self.w, n)
        h = round(self.h, n)
        return Rect(x, y, w, h)

    def __contains__(self, position):
        """Determine if a position is in the rectangle."""
        x, y = position
        return (self.xmin <= x <= self.xmax) and (self.ymin <= y <= self.ymax)

    def resize(self, n):
        """Allow the user to resize the rectangle."""
        self.w *= n
        self.h *= n

    def __iter__(self):
        self.iterator = 0
        return self

    def __next__(self):
        if self.iterator < 4:
            self.iterator += 1
            return self.components[self.iterator - 1]
        else:
            raise StopIteration

    # properties
    # corners
    def getCorners(self):
        """Return the corners of the rect."""
        return [self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2]

    def setCorners(self, corners):
        """Set the corners of the rect."""
        x1, y1, x2, y2 = corners
        self.w = x2 - x1
        self.h = y2 - y1
        self.x = x1 - self.w / 2
        self.y = y1 - self.w / 2

    # coordinates
    def getCoordinates(self):
        """Return the coordinates of the rect."""
        return [self.x, self.y, self.w, self.h]

    def setCoordinates(self, coordinates):
        """Set the coordinates of the rect."""
        self.position = coordinates[:2]
        self.size = coordinates[2:]

    # rect
    def getRect(self):
        """Return the rect of the rectangle."""
        return Rect.getRectFromCoordinates(self.getCoordinates())

    def setRect(self, rect):
        """Set the rect of the rectangle."""
        self.setCoordinates(Rect.getCoordinatesFromRect(rect))

    # sx component
    def getWidth(self):
        """Return the width."""
        return self.components[2]

    def setWidth(self, w):
        """Set the width."""
        self.components[2] = w

    # sy component
    def getHeight(self):
        """Return the height."""
        return self.components[3]

    def setHeight(self, h):
        """Set the height."""
        self.components[3] = h

    # xmin component
    def getXmin(self):
        """Return the minimum of the x component."""
        return self.x - self.w / 2

    def setXmin(self, xmin):
        """Set the minimum of the x component."""
        self.x = xmin + w / 2

    # ymin component
    def getYmin(self):
        """Return the minimum of the y component."""
        return self.y - self.h / 2

    def setYmin(self, ymin):
        """Set the minimum of the y component."""
        self.y = ymin + self.h / 2

    # xmax component
    def getXmax(self):
        """Return the maximum of the x component."""
        return self.x + self.w / 2

    def setXmax(self, xmax):
        """Set the maximum of the x component."""
        self.x = xmax - self.w / 2

    # ymax component
    def getYmax(self):
        """Return the maximum of the y component."""
        return self.y + self.h / 2

    def setYmax(self, ymax):
        """Set the maximum of the y component."""
        self.y = ymax - self.h / 2

    corners = property(getCorners, setCorners, doc="Corners")
    coordinates = property(getCoordinates, setCoordinates, doc="Center+Size")
    w = sx = width = property(getWidth, setWidth, doc="Width")
    h = sy = height = property(getHeight, setHeight, doc="Height")
    xmin = x1 = left = l = property(getXmin, setXmin, doc="Left")
    xmax = x2 = right = r = property(getXmax, setXmax, doc="Right")
    ymin = y1 = bottom = b = property(getYmin, setYmin, doc="Bottom")
    ymax = y2 = top = t = property(getYmax, setYmax, doc="Top")

    # Static methods
    @staticmethod
    def getCornersFromCoordinates(coordinates):
        """Return the corners (top_left_corner,bottom_right_corner) using the coordinates (position+size)."""
        """[x,y,sx,sy] -> [mx,my,Mx,My]"""
        x, y, sx, sy = coordinates
        mx, my = x - sx / 2, y - sy / 2
        Mx, My = x + sx / 2, y + sy / 2
        return [mx, my, Mx, My]

    @staticmethod
    def getCoordinatesFromCorners(corners):
        """Return the coordinates (position+size) using the corners (top_left_corner,bottom_right_corner)."""
        """[mx,my,Mx,My] -> [x,y,sx,sy]"""
        mx, my, Mx, My = corners
        sx, sy = Mx - mx, My - my
        x, y = mx + sx / 2, my + sy / 2
        return [x, y, sx, sy]

    @staticmethod
    def getCoordinatesFromRect(rect):
        """Return the coordinates (position,size) using the rect (top_left_corner,size)."""
        """[x,y,sx,sy] -> [mx,my,sx,sy]"""
        mx, my, sx, sy = rect
        x, y = mx + sx / 2, my + sy / 2
        return [x, y, sx, sy]

    @staticmethod
    def getRectFromCoordinates(coordinates):
        """Return the rect (top_left_corner,size) using the coordinates (position,size)."""
        """[mx,my,sx,sy] -> [x,y,sx,sy]"""
        x, y, sx, sy = coordinates
        mx, my = x - sx / 2, y - sy / 2
        return [mx, my, sx, sy]

    @staticmethod
    def getRectFromCorners(corners):
        """Return the rect (top_left_corner,size) using the corners (top_left_corner,bottom_right_corner)."""
        """[mx,my,Mx,My] -> [mx,my,sx,sy]"""
        mx, my, Mx, My = corners
        sx, sy = Mx - mx, My - my
        return [mx, my, sx, sy]

    @staticmethod
    def getCornersFromRect(rect):
        """Return the (top_left_corner,bottom_right_corner) using the corners rect (top_left_corner,size)."""
        """[mx,my,Mx,My] -> [mx,my,sx,sy]"""
        mx, my, sx, sy = rect
        Mx, My = mx + sx, my + sy
        return [mx, my, Mx, My]


if __name__ == "__main__":
    r1 = Rect.random()
    r2 = Rect.random()
    r1.x -= 1
    print(r1, r2)
    print(r1.corners)
    print(r1.coordinates)
    print(r1.x, r1.y)
    print(r1.sx, r1.sy)
    print(r1.width, r1.height)
    r = Rect.cross(r1, r2)
    print(*r1)
