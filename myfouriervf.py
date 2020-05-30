from myinterpolation import PolynomialInterpolation
from myabstract import Point, Vector, Circle
from mycurves import Trajectory
from pygame.locals import *
#from PIL import Image


import numpy as np
import mycolors
import pygame
import pickle
import cmath
import math
import cv2
#import os


class Fourier:

    def transform(pts, ncfs, wo=2 * math.pi):
        """Apply the true fourier transform by
        returning a dictionary of the coefficients."""
        npts = len(pts)
        h = ncfs // 2
        cfs = {}
        # Compute all coefficients
        for n in range(-h, h + 1):
            # Compute each coefficient
            cn = 0
            for iw in range(npts):
                w = iw / npts  # w is not a frequency but the variable of a parametric equation
                fw = complex(*pts[iw])
                cn += fw * cmath.exp(-1j * n * w * wo)
            cn /= npts
            cfs[n] = cn
        return cfs

    def inverseTransform(cfs, npts, wo=2 * math.pi):
        """Apply the true fourier inverse transform
        by returning the list of the points."""
        ncfs = len(cfs)
        h = npts // 2
        pts = []
        # Compute all the points
        for it in range(npts):
            t = it / npts  # t is not a time but the variable of a parametric equation of the final graph
            # Compute each point
            zpt = 0
            for (n, cn) in cfs.items():  # Addition is commutative, even though the dictionary is unordered, the sum of the terms will be the same
                zpt += cn * cmath.exp(1j * wo * n * t)
            pts.append((zpt.real, zpt.imag))
        return pts

    def build(cfs, t, wo=2 * math.pi):
        """Return the 'construction graph' with a given time 't'."""
        ncfs = len(cfs)
        h = ncfs // 2
        cst = [(0, 0)]
        zpt = cfs[0]
        cst.append((zpt.real, zpt.imag))
        for n in range(1, h + 1):
            pcf = cfs[n] * cmath.exp(1j * wo * n * t)
            ncf = cfs[-n] * cmath.exp(1j * wo * (-n) * t)
            zpt += pcf
            cst.append((zpt.real, zpt.imag))
            zpt += ncf
            cst.append((zpt.real, zpt.imag))
        return cst


class VisualFourier:
    """Show an application of the fourier transform."""

    # Instance methods
    def __init__(self,
                 context,
                 image=None,
                 coefficients=[],
                 directory="FourierObjects",
                 filename="Fourier",
                 coefficients_filename="fourier_coefficients.txt"
                 ):
        """Initialization."""
        self.context = context
        self.coefficients = coefficients
        self.coefficients_filename = coefficients_filename

        # Directory
        self.directory = directory
        self.filename = filename

        # Graphs
        self.graphs = [[], [], []]

        # Memory cache for less calculations
        # This information is redundant and can be computed again
        self.sample = []

        # Mode
        self.mode = 0
        self.step = 0
        self.max_step = 1000
        self.messages = ['drawing', 'construction', 'display']
        self.pause = False
        self.include = True  # Include the last point of the interpolation

        # Precision settings
        # self.coefficients_number=100
        self.sample_number = 5
        self.display_number = 100  # Number of points of the display graph
        self.integral_precision = 100
        self.points_radius = 5

        # Optional settings
        # Graph shown
        self.show_image = True
        self.show_polynomial = False
        self.show_drawing = True
        self.show_display = True
        self.show_vectors = True
        self.show_circles = True
        self.show_sample = True
        self.show_camera = False
        # Graph color
        self.color_polynomial = mycolors.BLUE
        self.color_drawing = mycolors.GREEN
        self.color_display = mycolors.RED
        self.color_vectors = mycolors.WHITE
        self.color_circles = mycolors.GREY
        self.color_sample = mycolors.YELLOW

        # Set the image for sampling
        if image is None:
            self.image = None
            self.show_image = False
        else:
            self.image = self.context.loadImage(image)
            # Trying to convert a pygame image into a pil image that can be used for the canny algorithm.
            # s=self.image.get_size()
            # self.image=pygame.image.tostring(self.image,"RGBA",False)
            # self.image=Image.frombytes("RGBA",s,self.image)
            # self.image=cv2.Canny(self.image,50,150)

    def __call__(self):
        """Main loop."""
        self.setMode(self.mode)
        while self.context.open:
            self.events()
            self.main()
            self.show()

    def events(self):
        """Deal with all the events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.context.open = False
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    self.context.open = False
                if event.key == K_SPACE or event.key == K_MENU or event.key == K_q:
                    self.setMode((self.mode + 1) % 3)
                if event.key == K_0:
                    self.show_polynomial = not(self.show_polynomial)
                if event.key == K_1:
                    self.show_image = not(self.show_image)
                if event.key == K_2:
                    self.show_drawing = not(self.show_drawing)
                if event.key == K_3:
                    self.show_display = not(self.show_display)
                if event.key == K_4:
                    self.show_vectors = not(self.show_vectors)
                if event.key == K_5:
                    self.show_circles = not(self.show_circles)
                if event.key == K_6:
                    self.show_sample = not(self.show_sample)
                if event.key == K_r:
                    self.reset()
                if event.key == K_z:
                    self.drawing = self.drawing[:-1]
                    self.updateSample()
                if event.key == K_s:
                    self.save()  # Save the coefficients and the graphs
                if event.key == K_d:
                    self.saveCoefficients()
                if event.key == K_a:
                    # Save a picture the screen
                    self.screenshot(self.directory)
                if event.key == K_p:
                    self.pause = not(self.pause)
                if event.key == K_f:
                    self.context.switch()
                if event.key == K_c:
                    self.show_camera = not(self.show_camera)
                    if self.show_camera:
                        self.context.camera.buildCapture()
                    else:
                        self.context.camera.destroy()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1) and (self.mode == 0):
                    self.place()
                    self.updateSample()
                if event.button == 4:
                    self.context.draw.plane.zoom([1.1, 1.1])
                if event.button == 5:
                    self.context.draw.plane.zoom([0.9, 0.9])

            if event.type == VIDEORESIZE:
                self.context.screen = pygame.display.set_mode(
                    (event.w, event.h), RESIZABLE)

    def main(self):
        """Code inside the loop."""
        if self.mode == 0:  # drawing
            pass
        elif self.mode == 1:  # construction
            if self.step > self.max_step:
                self.mode = 2
            else:
                self.construction = Fourier.build(self.coefficients, self.time)
                self.display.append(self.construction[-1])
                if not self.pause:
                    self.step += 1
        elif self.mode == 2:  # display
            pass

    def show(self):
        """Show the graph."""
        self.context.control()
        self.context.clear()
        self.context.show()

        sx, sy = self.context.size
        drawing, construction, display = range(3)

        if self.show_image and self.image:
            self.context.draw.image(self.context.screen, self.image, (0, 0))
        if self.show_camera:
            self.context.camera.show()

        if self.mode == 0:
            if self.show_polynomial:
                self.drawPolynomial(drawing, self.color_polynomial)
            if self.show_drawing:
                self.drawGraph(drawing, self.color_drawing)
            if self.show_sample:
                self.drawPoints(self.sample, self.color_sample)
        elif self.mode == 1:
            if self.show_polynomial:
                self.drawPolynomial(drawing, self.color_polynomial)
            if self.show_drawing:
                self.drawGraph(drawing, self.color_drawing)
            if self.show_vectors:
                self.drawVectors(construction, self.color_vectors)
            if self.show_circles:
                self.drawCircles(construction, self.color_circles)
            if self.show_display:
                self.drawGraph(display, self.color_display)
            if self.show_sample:
                self.drawPoints(self.sample, self.color_sample)
        elif self.mode == 2:
            if self.show_polynomial:
                self.drawPolynomial(drawing, self.color_polynomial)
            if self.show_drawing:
                self.drawGraph(drawing, self.color_drawing)
            if self.show_display:
                self.drawGraph(display, self.color_display)
            if self.show_sample:
                self.drawPoints(self.sample, self.color_sample)

        self.context.print("Time: " + str(self.time),
                           position=(10, 10), size=35, conversion=False)
        if self.pause:
            self.context.print("Pause", position=(
                sx - 100, 10), size=35, conversion=False)
        self.context.showConsole()
        self.context.flip()

    def reset(self):
        """Reset the graphs, the sample and the mode."""
        self.mode = 0
        self.graphs = [[], [], []]
        self.coefficients = []
        self.sample = []

    def getVectors(self, graph):
        """Return the list of vectors."""
        return [Vector.createFromTwoTuples(graph[i], graph[i + 1]) for i in range(len(graph) - 1)]

    def showVectors(self, graph, vectors, color=mycolors.WHITE):
        """Show the vectors on the screen."""
        for i in range(len(vectors) - 1):
            vectors[i].show(self.context, Point(*graph[i]), color)

    def setMode(self, mode):
        """Change the mode into another."""
        self.mode = mode
        if self.mode == 0:
            self.setDrawingMode()
        elif self.mode == 1:
            self.setConstructionMode()
        elif self.mode == 2:
            self.setDisplayMode()
        self.context.text.append("mode: " + self.messages[self.mode])

    def setDrawingMode(self):
        """Set the attributes before starting the drawing mode."""
        pass

    def setConstructionMode(self):
        """Set the attributes before starting the construction mode."""
        self.step = 0
        self.display = []
        # t=Trajectory.createFromTuples(self.drawing)
        # l=t.sampleSegments(self.sample_number)
        self.coefficients = Fourier.transform(
            self.sample, self.coefficients_number)

    def setDisplayMode(self):
        """Set the attributes before starting the display mode."""
        self.step = (self.max_step + int(self.include))
        self.display = Fourier.inverseTransform(
            self.coefficients, self.display_number)

    def place(self):
        """Place a point."""
        p = self.context.point()
        self.drawing.append(p)

    def updateSample(self):
        """Update the sample."""
        t = Trajectory.createFromTuples(self.drawing)
        self.sample = t.sampleSegments(
            self.sample_number, include=self.include)

    def screenshot(self):
        """Make a screenshot of the window."""
        self.context.draw.window.screenshot(self.filename)

    @property
    def dictionary(self):
        """Return the dictionary."""
        dictionary = {
            "coefficients":     self.coefficients,
            "drawing":          self.drawing,
            "construction":     self.construction,
            "display":          self.display
        }
        return dictionary

    def save(self):
        """Save the sampled graph and fourier's coefficients."""
        path = self.directory + "/" + self.filename
        pickle.dump(self.dictionary, open(path, 'wb'))
        self.context.console.append("The Fourier components are saved.")

    def saveCoefficients(self):
        """Save the coefficients in a txt file."""
        path = self.directory + "/" + self.coefficients_filename
        with open(path, mode="w", encoding="utf-8") as file:
            file.write(
                "\n".join([f"{k}:{v}" for k, v in self.dictionary["coefficients"].items()]))
            self.context.console.append(
                "The Fourier coefficients are written.")

    def load(self):
        """Load the fourier's coefficients."""
        path = self.directory + "/" + self.filename
        dictionary = pickle.load(open(path, 'rb'))
        self.coefficients = dictionary["coefficients"]
        self.display = dictionary["display"]
        self.construction = dictionary["construction"]
        self.drawing = dictionary["drawing"]
        self.updateSample()
        self.context.console.append("The Fourier components are loaded.")

    def getTime(self):
        """Return the time of the construction."""
        return self.step / (self.max_step + int(self.include))

    time = property(getTime)

    # Graphical functions
    def distance(self, p1, p2):
        """Return the distance between 2 points."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def drawVectors(self, index, color):
        """Draw the vectors from the points."""
        graph = self.graphs[index]
        for i in range(len(graph) - 1):
            v = Vector.createFromTwoTuples(graph[i], graph[i + 1], color=color)
            v.showFromTuple(self.context, graph[i])

    def drawCircles(self, index, color):
        """Draw the circles from the points."""
        graph = self.graphs[index]
        for i in range(len(graph) - 1):
            radius = self.distance(graph[i], graph[i + 1])
            c = Circle.createFromPointAndRadius(graph[i], radius, color=color)
            c.show(self.context)

    def drawGraph(self, index, color, connected=False, width=1, conversion=True):
        """Draw the graph."""
        graph = self.graphs[index]
        if len(graph) > 1:
            self.context.draw.lines(
                self.context.screen, color, graph, connected, width, conversion)

    def drawPolynomial(self, index, color, precision=200):
        """Draw the polynomial interpolation of the points."""
        graph = self.graphs[index]
        if len(graph) > 1:
            p = PolynomialInterpolation(graph, color)
            p.show(self.context, precision)

    def drawPoints(self, points, color):
        """Draw the points that were sampled for the fourier transform."""
        for p in points:
            Point
            p.color = color
            p.radius = self.points_radius
            p.conversion = False
            p.show(self.context)

    def drawSample(self, index, color):
        """Draw the points that were sampled for the fourier transform."""
        t = Trajectory.createFromTuples(self.graphs[index])
        l = t.sampleSegments(self.sample_number, include=self.include)
        for e in l:
            p = Point(*e, radius=5, conversion=False)
            p.show(self.context)

    # Properties

    def getDrawing(self):
        return self.graphs[0]

    def setDrawing(self, graph):
        self.graphs[0] = graph

    def getConstruction(self):
        return self.graphs[1]

    def setConstruction(self, graph):
        self.graphs[1] = graph

    def getDisplay(self):
        return self.graphs[2]

    def setDisplay(self, graph):
        self.graphs[2] = graph

    def getCoefficientsNumber(self):
        return len(self.sample)

    drawing = property(getDrawing, setDrawing)
    construction = property(getConstruction, setConstruction)
    display = property(getDisplay, setDisplay)
    coefficients_number = property(getCoefficientsNumber)


if __name__ == "__main__":
    from mycontext import Context

    folder = "FourierImages"

    sj = "saint jalm.jpg"
    vl = "valentin.png"
    tm = "tetedemarc.png"
    pm = "profiledemarc.jpg"
    rh = "rohart.jpg"

    image = folder + "/" + rh

    context = Context(
        name="Application of the Fourier Transform.", fullscreen=False)
    fourier = VisualFourier(context, image=image)
    fourier.load()
    fourier()
    fourier.save()
