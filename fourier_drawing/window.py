from .colors import *

from pygame.locals import *


import pygame

pygame.init()

import random
import time


class Window:
    made = 0
    draw = pygame.draw
    rect = pygame.rect
    mouse = pygame.mouse
    # blit=pygame.blit
    display = pygame.display
    transform = pygame.transform

    # Creation of the window

    def __init__(
        self,
        name="Unnamed",
        size=None,
        text_font="monospace",
        text_size=50,
        text_color=WHITE,
        background_color=BLACK,
        fullscreen=False,
        build=True,
    ):
        """Create a window object using name, size text_font, text_size,
        text_color, background and set."""
        Window.made += 1
        self.number = Window.made
        self.name = name
        self.text_font = text_font
        self.text_size = text_size
        self.text_color = text_color
        self.background_color = background_color
        self.fullscreen = fullscreen
        self.set()
        self.log("Window has been created.")
        if build:
            self.build(size)

    def set(self):
        """Set builtins attributs of window object."""
        self.RIGHT = 0
        self.UP = 1
        self.LEFT = 2
        self.DOWN = 3
        self.open = False
        self.screenshots_taken = 0
        self.counter = 0

    def build(self, size=None):
        """Creates apparent window."""
        self.events = pygame.event.get
        self.clock = pygame.time.Clock()
        self.info = pygame.display.Info()
        self.font = pygame.font.SysFont(self.text_font, self.text_size)
        self.setScreenMode(size)
        pygame.display.set_caption(self.name)
        if self.text_color is None:
            self.text_color = self.reverseColor(self.background_color)
        self.clear()
        self.flip()
        self.open = True

    # Screen related functions

    def __call__(self, duration=float("inf")):
        """Flip the screen and pause the window."""
        self.flip()
        self.pause(duration)

    def __bool__(self):
        """Determine if the window is open or not."""
        return self.open

    def clear(self, color=None):
        """Clear to background color."""
        if color is None:
            color = self.background_color
        self.screen.fill(color)

    def flip(self):
        """Display on the screen the image considered."""
        pygame.display.flip()

    def update(self):
        """Update the screen."""
        pygame.display.update()

    def screenshot(self, image=None, name=None):
        """Save an image using the image and the name.
        - If the image is not given, a screenshot will be made.
        - If the name is not given, the named will be unnamed."""
        if name == None:
            name = "unnamed"
        if image == None:
            pygame.image.save(self.screen, name)
        self.screenshot_taken += 1

    def rename(self, name):
        """Rename the window using name."""
        self.name = name
        pygame.display.set_caption(self.name)

    def getArray(self):
        """Return the array of the screen."""
        return pygame.PixelArray(self.screen)

    def setArray(self, array):
        """Set the surface using the array."""
        surface = pygame.PixelArray.make_surface()
        self.screen.blit(surface)

    array = property(getArray, setArray)

    # Events related functions

    def check(self):
        """Update window's state depending if close buttons are pressed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.open = False
            if event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)

    def checking(self, event):
        """Determines if the window must be closed."""
        if event.type == pygame.QUIT:
            self.open = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.open = False

    def press(self):
        """Return all keys."""
        return pygame.key.get_pressed()

    def direction(self):
        """Return keys for arrows pressed. Trigonometric orientation is used."""
        keys = pygame.key.get_pressed()
        return (keys[K_RIGHT], keys[K_UP], keys[K_LEFT], keys[K_DOWN])

    def select(self):
        """Wait for user to click on screen, then return cursor position."""
        while self.open:
            for event in pygame.event.get():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.open = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.open = False
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0], event.pos[1])

    def point(self):
        """Return cursor position on screen."""
        return pygame.mouse.get_pos()

    def click(self):
        """Return bool value for clicking on screen."""
        return bool(pygame.mouse.get_pressed()[0])

    def press(self):
        """Return bool value for clicking on screen."""
        return pygame.key.get_pressed()

    # Time related functions

    def clock(self, tick):
        """Set a clock using tick."""
        self.clock.tick(tick)

    def pause(self, duration=float("inf")):
        """Wait for user to press the 'space'."""
        to = time.time()
        while self.open and time.time() - to < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.open = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.open = False
                    if event.key == K_SPACE:
                        return

    def sleep(self, duration):
        """Sleep for a given duration."""
        time.sleep(duration)

    def wait(self, duration=0.1):
        """Wait during given time."""
        t = time.time()
        while self.open and time.time() - t < duration:
            self.check()

    def count(self, n=1):
        """Increment the counter by n, which is 1 by default."""
        self.counter += n

    # Sound related functions

    def loadSound(self, filename):
        """Load a sound. Doesn't work on mac apparently..."""
        return pygame.mixer.Sound(filename)

    def playSound(self, sound):
        """Play a sound."""
        pygame.mixer.Sound.play(sound)

    def loadMusic(self, filename):
        """"Load a music. Doesn't work on mac apparently..."""
        pygame.mixer.music.load(filename)

    def playMusic(self, music, times=1):
        """Play a music."""
        pygame.mixer.music.play(music, times)

    def pauseMusic(self, music):
        """Pause a music being played."""
        pygame.mixer.music.pause()

    def unpauseMusic(self, music):
        """Unpause a music being paused."""
        pygame.mixer.music.unpause()

    def stopMusic(self, music):
        """Stop a music being played."""
        pygame.mixer.music.stop()

    def load(self, filename, music=False):
        """Load an image or a sound."""
        x = filename.split(".")[-1]
        if x == "mp3" or x == "ogg" or x == "waw":
            if music:
                return self.loadMusic()
            else:
                return self.loadSound(filename)
        if x == "png" or x == "jpg" or x == "jpeg":
            return self.loadImage(filename)

    # Image related functions

    def blit(self, image, position):
        """Blit an image on the screen."""
        self.screen.blit(image, position)

    def loadImage(self, filename):
        """Load an image using a filename."""
        return pygame.image.load(filename)

    def scale(self, picture, size):
        """Return scaled picture using picture and size."""
        return pygame.transform.scale(picture, size)

    def load(self, filename):
        """Return picture using picture directory."""
        return pygame.image.load(filename)

    def centerSurface(self, surface):
        """Centers a surface on the screen."""
        sx, sy = self.size
        sfx, sfy = surface.get_size()
        return ((sx - sfx) // 2, (sy - sfy) // 2)

    def alert(
        self,
        *text,
        size=None,
        color=None,
        font=None,
        background=None,
        bold=False,
        italic=False
    ):
        """Quickly display text on window."""
        if not size:
            size = self.text_size
        if not color:
            color = self.text_color
        if not font:
            font = self.text_font
        text = " ".join(map(str, text))
        font = pygame.font.SysFont(font, size, bold, italic)
        surface = font.render(text, 1, color, background)
        position = self.centerSurface(surface)
        self.screen.blit(surface, position)
        self.flip()

    def print(
        self,
        text,
        position,
        size=None,
        color=None,
        font=None,
        background=None,
        bold=False,
        italic=False,
    ):
        """Display text on screen using position, size, color and font."""
        if not size:
            size = self.text_size
        if not color:
            color = self.text_color
        if not font:
            font = self.text_font
        font = pygame.font.SysFont(font, size, bold, italic)
        surface = font.render(str(text), 1, color[:3], background)
        if len(color) == 4:
            a = color[3]
            surface.set_alpha(a)
            raise NotImplementedError("Transparency does not work properly in pygame")
        self.screen.blit(surface, position)

    def setScreenMode(self, size=None):
        """Set the display for the screen to the right mode using its optional size."""
        if not size:
            if self.fullscreen:
                size = [self.info.current_w, self.info.current_h]
            else:
                size = [2 * self.info.current_w // 3, 2 * self.info.current_h // 3]
        if self.fullscreen:
            self.screen = pygame.display.set_mode(size, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size, RESIZABLE)

    def switch(self):
        """Switch the mode into fullscreen or normal."""
        self.fullscreen = not (self.fullscreen)
        self.setScreenMode()

    # Usefull functions

    def randomColor(self, alpha=False):
        """Return random color."""
        return tuple([random.randint(0, 255) for i in range(3 + int(alpha))])

    def reverseColor(self, color):
        """Return reverse color."""
        return tuple([255 - c for c in color])

    def lighten(self, color, luminosity=80):  # View later
        """Return lightened color using color and luminosity percentage."""
        r, g, b = color
        if luminosity >= 50:
            r += (255 - r) * luminosity / 100
            g += (255 - g) * luminosity / 100
            b += (255 - b) * luminosity / 100
        else:
            r -= r * luminosity / 100
            g -= g * luminosity / 100
            b -= b * luminosity / 100
        color = r, g, b
        return color

    def colorize(self, image, color):
        """Return image colorized"""
        image = image.copy()
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
        return image

    def wavelengthToRGB(self, wavelength):
        """Convert wavelength to rgb color type."""
        gamma, max_intensity = 0.80, 255

        def adjust(color, factor):
            if color == 0:
                return 0
            else:
                return round(max_intensity * pow(color * factor, gamma))

        if 380 <= wavelength <= 440:
            r, g, b = -(wavelength - 440) / (440 - 380), 0, 1
        elif 440 <= wavelength <= 490:
            r, g, b = 0, (wavelength - 440) / (490 - 440), 1
        elif 490 <= wavelength <= 510:
            r, g, b = 0, 1, -(wavelength - 510) / (510 - 490)
        elif 510 <= wavelength <= 580:
            r, g, b = (wavelength - 510) / (580 - 510), 1, 0
        elif 580 <= wavelength <= 645:
            r, g, b = 1, -(wavelength - 645) / (645 - 580), 0
        elif 645 <= wavelength <= 780:
            r, g, b = 1, 0, 0
        else:
            r, g, b = 0, 0, 0
        if 380 <= wavelength <= 420:
            factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
        elif 420 <= wavelength <= 701:
            factor = 1
        elif 701 <= wavelength <= 780:
            factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
        else:
            factor = 0
        r, g, b = adjust(r, factor), adjust(g, factor), adjust(b, factor)
        return (r, g, b)

    def log(self, message):
        """Print message with window mention."""
        text = "[" + str(self.name) + "] " + str(message)
        print(text)

    # End of the game

    def quit(self):
        """Quit pygame."""
        self.log("Window has been closed.")
        pygame.quit()

    kill = quit

    # Properties

    def getSize(self):
        """Return the size of the window."""
        return self.screen.get_size()

    def getCorners(self):
        """Return the corners of the screen."""
        return (0, 0) + self.size

    def getWidth(self):
        """Return the width of the screen."""
        return self.screen.get_width()

    def getHeight(self):
        """Return the height of the screen."""
        return self.screen.get_height()

    def getCenter(self):
        """Return the center of the screen."""
        return tuple([s // 2 for s in self.size])

    size = property(getSize, doc="Size can only be read not written.")
    corners = property(getCorners, doc="Corners can only be read not written.")
    width = property(getWidth, doc="Width can only be read not written.")
    height = property(getHeight, doc="Height can only be read not written.")
    center = property(getCenter, doc="Center can only be read not written")


# class Text

# class TextWritter(Window):
# Writes text on a surface


if __name__ == "__main__":
    w = Window("Window Prototype")
    # w.save(w,"grosse fenetre")
    # w=load("grosse fenetre")
    print(w.lighten(BLUE))
    # music=w.loadMusic("The-Outlander.mp3")
    # w.playMusic(music)
    w.alert("test")
    w.pause()
    w.clear()
    w.switch()
    # w.alert(w.size)
    w.alert(w.center, w.size, background=(255, 0, 0))
    w.pause()
    w.clear()
    w.alert("je raconte de la merde juste pour avoir une longue chaine de caractere")
    w.pause()
    # w.stopMusic()
