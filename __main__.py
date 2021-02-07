#!/usr/bin/env python
from fourier_drawing.context import Context
from fourier_drawing.fourier import VisualFourier

import os
import logging
import sys

folder = "FourierImages"
directory = "FourierObjects"

if len(sys.argv) > 1:
    image_name = sys.argv[1]
else:
    logging.warning(
        "You must place your image in the FourierImages folder before using it." ""
    )
    image_name = input("image name:")

image_path = os.path.abspath(image_name)
if not os.path.exists(image_path):
    image_path = os.path.abspath(os.path.join(folder, image_name))
print("path:", image_path)

directory_path = os.path.abspath(directory)

context = Context(name="Application of the Fourier Transform.", fullscreen=False)
fourier = VisualFourier(context, image=image_path, directory=directory_path)
fourier.load()
fourier()
fourier.save()
