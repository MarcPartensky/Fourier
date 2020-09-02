#!/usr/bin/env python
from fourier_drawing.context import Context
from fourier_drawing.fourier import VisualFourier

import os
import logging
import sys

folder = "FourierImages"

if len(sys.argv) > 1:
  image_name = sys.argv[1]
else:
  logging.warning("You must place your image in the FourierImages folder before using it.""")
  image_name = input('image name:')

image = os.path.join(folder, image_name)
print(image)


context = Context(name="Application of the Fourier Transform.", fullscreen=False)
fourier = VisualFourier(context, image=image, directory="FourierObjects")
fourier.load()
fourier()
fourier.save()
