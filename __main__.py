#!/usr/bin/env python
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from fourier_drawing.context import Context
from fourier_drawing.fourier import VisualFourier


import logging
import sys

folder = "FourierImages"
directory = "FourierObjects"

if len(sys.argv) > 1:
    image_name = sys.argv[1]
else:
    logging.warning(
        "You must place your image in the FourierImages folder before using it.\n" ""
    )
    print("Choose an image:")
    print(*os.listdir(folder))
    image_name = input("> ")

image_path = os.path.abspath(image_name)
if not os.path.exists(image_path):
    image_path = os.path.abspath(os.path.join(folder, image_name))
print("path:", image_path)

directory_path = os.path.abspath(directory)

context = Context(name="Application of the Fourier Transform.", fullscreen=False)
fourier = VisualFourier(context, image=image_path, directory=directory_path)
# Load fourier coefficients if some already exist
if fourier.filename in os.listdir(fourier.directory):
    fourier.load()
fourier()
fourier.save()
