from mydraw import Draw
from myrect import Rect
from mywindow import Window

import mycolors
import time as tm
import copy

# For the camera only
from pygame.locals import *
import numpy as np
import pygame
import cv2


# For the camera only


class Camera:
    """The camera relies on opencv, pygame and numpy."""

    def __init__(self, draw, position=[0, 0],
                 build_capture=False,
                 build_screen_writer=False,
                 build_capture_writer=False,
                 filename="unnamed.mp4",
                 framerate=15):
        """Create an opencv camera. By default the capture is not active, it must
        be built using the build method, or by setting build to True in the
        init method."""
        self._draw = draw
        self.position = position
        self.filename = filename
        self.fourccs = {'mp4': 'MP4V', 'avi': 'DIVX'}
        self.framerate = framerate
        # Building videos components
        if build_capture:
            self.buildCapture()
        if build_screen_writer:
            self.buildScreenWriter()
        if build_capture_writer:
            self.buildCaptureWriter()

    def buildCapture(self):
        """Build the capture with opencv. Having a separate function for the
        capture allows to have more efficiency for programs that do not need the
        camera."""
        self.capture = cv2.VideoCapture(0)

    def buildCaptureWriter(self, filename=None, framerate=None):
        """Write the videos of the camera, this is just an odd concept, nothing
        really functional."""
        if not filename: filename = self.filename
        _, extension = filename.split('.')
        fourcc = self.fourccs[extension]
        print(fourcc)
        fourcc = cv2.VideoWriter_fourcc(*fourcc)
        if not framerate: framerate = self.framerate
        self.capture_writer = cv2.VideoWriter(filename, fourcc, framerate, frameSize=self._draw.window.size)

    def buildScreenWriter(self, filename=None, framerate=None):
        """Write the videos of the screen."""
        if not filename: filename = self.filename
        _, extension = filename.split('.')
        fourcc = self.fourccs[extension]
        fourcc = cv2.VideoWriter_fourcc(*fourcc)
        if not framerate: framerate = self.framerate
        self.screen_writer = cv2.VideoWriter(filename, fourcc, framerate, frameSize=self._draw.window.size)

    def writeCapture(self):
        """Write the capture."""
        # Note this cannot work if the video capture is not built
        _, frame = self.capture.read()
        self.capture_writer.write(frame)

    def writeScreen(self):
        """Write the screen."""
        output = pygame.surfarray.array3d(self._draw.window.screen)
        output = cv2.transpose(output)
        output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
        self.screen_writer.write(output)

    def show(self):
        """Show the video."""
        ret, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        self._draw.image(self._draw.window.screen, frame, self.position)

    __call__ = show

    def endCaptureWriter(self):
        """End the video writer and save its content."""
        del self.capture_writer

    def endScreenWriter(self):
        """End the screen writer and record its content."""
        del self.screen_writer

    def endCapture(self):
        """End the camera by ending the video capture."""
        del self.capture

    def destroy(self):
        """Destroy all cv2 windows."""
        cv2.destroyAllWindows()

    def isCapturing(self):
        """Determine if the capture is set."""
        return "capture" in self.__dict__

    def isWriting(self):
        """Determine if some content is being recorded."""
        return ("screen_writer" in self.__dict__) or ("capture_writer" in self.__dict__)

    def isScreenWriting(self):
        """Determine if the screen is being recorded."""
        return "screen_writer" in self.__dict__

    def isCaptureWriting(self):
        """Determine if the capture is being recorded."""
        return "capture_writer" in self.__dict__

    def setCapturing(self, capturing):
        """Set the capturing to the boolean 'capturing'."""
        if not self.capturing and capturing:
            self.buildCapture()
        if self.capturing and not capturing:
            self.endCapture()

    def setScreenWriting(self, screen_writing):
        """Set the screen writing to the boolean 'screen_writing'."""
        if not self.screen_writing and screen_writing:
            self.buildScreenWriter()
        if self.screen_writing and not screen_writing:
            self.endScreenWriter()

    def setCaptureWriting(self, capture_writing):
        """Set the capture writing to the boolean 'capture_writing'."""
        if not self.capture_writing and capture_writing:
            self.buildCaptureWriter()
        if self.capture_writing and not capture_writing:
            self.endCaptureWriter()

    capturing = property(isCapturing, setCapturing)
    screen_writing = property(isScreenWriting)
    capture_writing = property(isCaptureWriting)
    writing = property(isWriting)

    def switchCapture(self):
        """Switch the capture mode."""
        if self.capturing:
            self.endCapture()
        else:
            self.buildCapture()

    def switchScreenWriting(self):
        """Switch the screen writing mode."""
        if self.screen_writing:
            self.endScreenWriter()
        else:
            self.buildScreenWriter()

    def switchCaptureWriting(self):
        """Switch the capture writing mode."""
        if self.capture_writing:
            self.endCaptureWriter()
        else:
            self.buildCaptureWriter()

    def __del__(self):
        """Delete the camera components if they exist."""
        if self.capturing:
            del self.capture
        if self.screen_writing:
            del self.screen_writer
        if self.capture_writing:
            del self.capture_writer
        self.destroy()

    def write(self):
        """Write the screen or the capture video if they are on."""
        if self.screen_writing:
            self.writeScreen()
        if self.capture_writing:
            self.writeCapture()

    def release(self):
        """Release the screen or the capture video if they are on."""
        if self.screen_writing:
            self.screen_writer.release()
        if self.capture_writing:
            self.capture_writer.release()


class Line:
    """Representation of a line in the console.
    This might be used for visual debugging but also for typing commands."""

    def __init__(self, *content, time=None, color=mycolors.WHITE, separator=" "):
        """Object of line created using the text and optional time."""
        if time is None: time=tm.time()
        self.content = list(content)
        self.time = time
        self.color = color
        self.separator = separator

    def __str__(self):
        """Return the string representation of a line."""
        return self.separator.join(map(str, self.content))

    def __iter__(self):
        """Iterate a line by giving its content of the instant the line was written."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return first the content, then the instant the line was written."""
        if self.iterator < 2:
            self.iterator += 1
            if self.iterator + 1 == 0:
                return self.content
            elif self.iterator + 1 == 1:
                return self.time

    def getText(self):
        """Return the content of a line."""
        return self.content

    text = property(getText)

    def refresh(self):
        """Refresh the time."""
        self.time = tm.time()

    @property
    def empty(self):
        return self.content[0] == ""  # difficult to do uglier


class Console:
    def __init__(self, draw,
                 lines=[],
                 interline=15,
                 left_padding=10,
                 down_padding=20,
                 conversion=False,
                 size=20,
                 position=[0, 0],
                 font=None,
                 max_lines_shown=10,
                 duration_lines_shown=10,
                 disappearance_lines_shown=10,
                 colors=[mycolors.WHITE, mycolors.BLACK]):
        """Create a console."""
        self._draw = draw  # Draw is protected and can only be read
        self.lines = lines  # List of Lines
        self.interline = interline
        self.left_padding = left_padding
        self.down_padding = down_padding
        self.conversion = conversion
        self.size = size
        self.position = position
        self.font = font
        self.max_lines_shown = max_lines_shown
        self.duration_lines_shown = duration_lines_shown
        self.disappearance_lines_shown = disappearance_lines_shown
        self.colors = colors
        self.line_index = 0
        self.line_memory = None

    def eval(self):
        """Execute the last line."""
        content = self.lines[-1].content
        if len(content) >= 1:
            if content[0] == "marc":
                content[0] += " is awesome."
            elif content[0] == "time":
                content[0] = "The time is " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "."
            elif content[0] == "minecraft":
                content[0] += "is the best game ever."
            elif content[0][:6] == "print(":
                self(eval(content[0][6:-1]))
            elif content[0] == "refresh":
                self.refresh()

    def back(self):
        """Set the line to an older one."""
        if self.line_index == 0:
            self.line_memory = copy.deepcopy(self.line)
        if self.line_index < len(self.lines) - 1:
            self.line_index += 1
            self.line = copy.deepcopy(self.lines[-1 - self.line_index])
            self.line.refresh()

    def forward(self):
        """Set the line to a new one."""
        if self.line_index > 1:
            self.line_index -= 1
            self.line = copy.deepcopy(self.lines[-1 - self.line_index])
        elif self.line_index == 1:
            self.line_index -= 1
            self.line = self.line_memory
        self.line.refresh()

    def clear(self):
        """Clear the console by removing all the lines."""
        self.lines = []

    def refresh(self):
        """Refresh the console by showing its previous messages."""
        for line in self.lines:
            line.time = tm.time()

    def __getitem__(self, i):
        """Return the i-th line."""
        return self.lines[i]

    def __setitem__(self, v, i):
        """Set the i-th line."""
        self.lines[i] = v

    def __iadd__(self, *args):
        """Add a line to the console."""
        l = Line(*args, time=tm.time())
        self.lines.append(l)

    append = __iadd__

    def appendLines(self, lines):
        """Append multiple lines."""
        for line in lines:
            self.append(line)

    def __call__(self, *args, **kwargs):
        """Display a message on the context as a console would do."""
        if len(args) > 0:
            l = Line(*args, **kwargs)
            self.lines.append(l)

    def nextArg(self):
        """Create a new argument."""
        self.lines[-1].content.append("")

    def nextLine(self):
        """Create a new line."""
        self("")

    def setLine(self, line):
        self.lines[-1] = line

    def getLine(self):
        return self.lines[-1]

    def delLine(self):
        del self.lines[-1]

    line = property(getLine, setLine, delLine)

    def show(self):
        """Show the console without adding a text."""
        sx, sy = self._draw.window.size
        n = len(self.lines)
        nmax = self.max_lines_shown
        dls = self.disappearance_lines_shown
        for i in range(min(n, nmax)):
            position = (self.left_padding, sy - self.interline * i - self.down_padding)
            to = self.lines[-i - 1].time
            t = (tm.time() - to) / self.duration_lines_shown
            if t < 1:
                c1 = self.lines[-i-1].color + (t ** dls,)
                # c2 = self.colors[1] + (t ** dls,)
                self._draw.print(self.lines[-i - 1], position, self.size, c1, self.font, self.conversion)


class Context(Rect):
    """The context is an object that allows the user to display graphical objects
    on the screen in a virtual mathematical plane."""

    def createFromSizeAndCorners(size, corners, **kwargs):
        c = Context(size=size, **kwargs)
        c.corners = corners
        return c

    def __init__(self, draw=None, console=None, camera=None, **kwargs):
        """Create a context using the optional draw, console and camera, with
        some of the draw's arguments for the window.
        If those are not given, they will be created automatically."""
        if draw is None:
            draw = Draw(**kwargs)
        if console is None:
            console = Console(draw)
        if camera is None:
            camera = Camera(draw)
        self.start_time = tm.time()
        self.draw = draw
        self.console = console
        self.camera = camera
        self.clear = self.draw.clear
        self.flip = self.draw.window.flip
        self.press = self.draw.window.press
        self.build = self.draw.window.build
        self.click = self.draw.window.click
        self.__call__ = self.draw.window.__call__
        self.wait = self.draw.window.wait
        self.control = self.draw.control
        self.checking = self.draw.window.checking
        self.loadImage = self.draw.window.loadImage
        self.print = self.draw.print
        self.update = self.draw.window.update
        self.switch = self.draw.window.switch
        self.count = self.draw.window.count
        self.alert = self.draw.window.alert
        self.scale = self.draw.window.scale

    def getScreen(self):
        return self.draw.window.screen

    def setScreen(self, screen):
        self.draw.window.screen = screen

    screen = property(getScreen, setScreen)

    def getKeys(self):
        """Return the keys of the window."""
        return self.press()

    def getCorners(self):
        """Return the corners of the surface shown."""
        return self.draw.plane.getCorners(self.draw.window)

    def setCorners(self, corners):
        """Set the corners of the plane using the new corners."""
        self.draw.plane.setCorners(corners, self.draw.window)

    def getRect(self):
        """Return the rect of the surface shown."""
        return Plane.getRectFromCorners(self.getCorners())

    def setRect(self, rect):
        """Set the rect of the surface shown."""
        self.draw.plane.setCorners(Plane.getCornersFromRect(rect))

    def getCoordonnates(self):
        """Return the coordonnates of the surface shown."""
        return Plane.getCoordonnatesFromCorners(self.getCorners())

    def setCoordonnates(self, coordonnates):
        """Set the coordonnates of the surface shown."""
        self.draw.plane.setCorners(
            Plane.getCornersFromCoordonnates(coordonnates))

    def getPosition(self):
        """Return the position of the surface shown."""
        return self.draw.plane.position

    def setPosition(self, position):
        """Set the position of the surface shown."""
        self.draw.plane.position = position

    def getSize(self):
        """Return the size of the surface shown."""
        return self.draw.window.size

    def setSize(self, size):
        """Set the size of the surface shown."""
        self.draw.window.size = size

    def getUnits(self):
        """Return the units of the surface shown."""
        return self.draw.plane.units

    def setUnits(self, units):
        """Set the units of the surface shown."""
        self.draw.plane.units = units

    def point(self):
        """Adapt the position of the cursor in plane's coordonnates."""
        x, y = self.draw.window.point()
        x, y = self.draw.plane.getFromScreen([x, y], self.draw.window)
        return (x, y)

    def check(self):
        """Check if the surface is open."""
        self.draw.window.check()
        self.open = self.draw.window.open

    def __call__(self):
        """Calling the surface allow the user to move on screen."""
        while self.open:
            self.check()
            self.draw.plane.control(self.draw.window)
            self.draw.window.clear()
            self.draw.plane.show(self.draw.window)
            self.flip()

    def __contains__(self, position):
        """Determine if a position is in the context."""
        return self.draw.plane.contains(position, self.draw.window)

    def show(self):
        """Show the plane on screen."""
        self.draw.plane.show(self.draw.window)

    def refresh(self):
        """Refresh the context by clearing the screen and showing the plane."""
        self.draw.window.clear()
        self.draw.plane.show(self.draw.window)

    def controlZoom(self):
        """Control the zoom of the surface's plane."""
        self.draw.plane.controlZoom(self.draw.window)

    def controlPosition(self):
        """Control the position of the surface's plane."""
        self.draw.plane.controlPosition(self.draw.window)

    def getFromScreen(self, position):
        """Behave like the get from screen of the plan without having to put
        the window in parameter."""
        return self.draw.plane.getFromScreen(position, self.draw.window)

    def getToScreen(self, position):
        """Behave like the get to screen of the plan without having to put
        the window in parameter."""
        return self.draw.plane.getToScreen(position, self.draw.window)

    def blit(self, surface, position):
        """Blit a given surface to a given position."""
        size = surface.get_size()
        position = self.draw.plane.getToScreen(position, self.window)
        self.draw.window.screen.blit(surface, position)

    def getOpen(self):
        return self.draw.window.open

    def setOpen(self, open):
        self.draw.window.open = open

    def __enter__(self):
        """Opening the context."""
        self.check()
        self.control()
        self.clear()
        self.show()
        print("went in")
        return self

    def __exit__(self):
        """Ending the context."""
        print("going out")
        self.flip()
        if self.open:
            self.__enter__()

    def getWidth(self):
        """Return the width of the window."""
        return self.size[0]

    def setWidth(self, width):
        """Set the width of the window."""
        self.size[0] = width

    def getHeight(self):
        """Return the height of the window."""
        return self.size[1]

    def setHeight(self, height):
        """Set the height of the window."""
        self.size[1] = height

    def __bool__(self):
        """Determine if the context is opened or not."""
        return self.open

    def getText(self):
        """Text is an alias for console and can be read."""
        return self.console

    def setText(self, value):
        """Text is an alias for console and can be written."""
        self.console = value

    def showConsole(self, *args):
        """Show the console, this function is a fix for deprecated programs."""
        self.console.show(*args)

    def getCounter(self):
        """Return the window counter."""
        return self.draw.window.counter

    def setCounter(self, coutner):
        """Set the window counter."""
        self.draw.window.counter = counter

    def getPlane(self):
        """Return the draw's plane."""
        return self.draw.plane

    def setPlane(self, plane):
        """Set the draw's plane."""
        self.plane = plane

    def getWindow(self):
        """Return the draw's window."""
        return self.draw.window

    def setWindow(self, window):
        """Set the draw's window."""
        self.draw.window = window

    def getFullscreen(self):
        """Determine if the context is in fullscreen mode."""
        return self.draw.window.fullscreen

    def setFullscreen(self, fullscreen):
        """Set the fullscreen mode."""
        self.draw.window.fullscreen = fullscreen

    def getResolution(self):
        """Return the resolution of the screen."""
        return self.width / self.height

    @property
    def rate(self):
        return self.counter / (tm.time() - self.start_time)

    window = property(getWindow, setWindow)
    plane = property(getPlane, setPlane)

    corners = property(getCorners, setCorners)
    rect = property(getRect, setRect)
    coordonnates = property(getCoordonnates, setCoordonnates)  # Coordinates
    position = property(getPosition, setPosition)
    size = property(getSize, setSize)
    units = property(getUnits, setUnits)
    keys = property(getKeys)
    open = property(getOpen, setOpen)
    width = property(getWidth, setWidth)
    height = property(getHeight, setHeight)
    text = property(getText, setText)
    counter = property(getCounter, setCounter)
    fullscreen = property(getFullscreen, setFullscreen)
    resolution = property(getResolution)


Surface = Context  # Ugly fix for deprectated programs

if __name__ == "__main__":
    context = Context(name="Context test")
    context.camera.buildCapture()
    context.camera.buildScreenWriter("mycontext test.mp4")
    # context.camera.buildCaptureWriter('zzzz.mp4')
    context.console.duration_lines_shown = 2
    context.console.max_lines_shown = 40
    # context.corners=[0,0,1,1]
    print(context.corners)
    print(bool(context))
    while context:
        context.count()
        print(context.counter)
        context.check()
        context.update()
        context.control()
        context.clear()
        context.show()

        context.camera.show()
        context.camera.write()
        context.console(context.rate)

        # if context.counter > 100:
        #    context.camera.destroy()

        context.flip()
    context.camera.capture.release()
    context.camera.screen_writer.release()
    print('released')
