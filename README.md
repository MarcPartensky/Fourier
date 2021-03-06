# Use fourier transform to draw epicycles with your drawings.

Draw a picture or sample one, press space, then watch an epic simulation of epicycles being drawned identically as your picture. Thanks the the fourier transform your drawing will be reproduced in a real-time simulation only using epicycles.

# Demo

![https://www.youtube.com/watch?v=86bYtJCwQ_o](https://j.gifs.com/jZmnWP.gif)
# Install

```bash
#Clone the repository
git clone git@github.com:MarcPartensky/Fourier.git
cd Fourier

#Install requirements
pip install -r requirements.txt
```

# Usage

Put your model image `image.png` in the `FourierImages` folder.

* Option 1: Give image at launch.

```bash
python __main__.py image.png
```

* Option 2: Launch then give the image.

```bash
python __main__.py
> image name:
```

Then give your image:

```bash
> image name:image.png
```

# Description

There are 3 modes in this program:

* Mode 1: Sampling
Sample or draw a picture.

* Mode 2: Drawing
Watch the epicycles simulation which uses fourier transform.

* Mode 3: Display
Get the output image directly without waiting for the simulation.

# Controls

* Space: Switch to next mode.
* Enter: Go back to the center.
* Up/Down/Right/Left Arrow: Move arround.
* Right/Left Shift: Zoom in or out.
* Quit/Escape: Quit.
* Z: Cancel last sample.
* R: Remove all samples.
* S: Save the fourier-coefficients.

# Enjoy!
