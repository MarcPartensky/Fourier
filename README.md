# Use fourier transform to draw epicycles with your drawings.

Draw a picture or sample one, press space, then watch an epic simulation of epicycles being drawned identically as your picture. Thanks the the fourier transform your drawing will be reproduced in a real-time simulation only using epicycles.

# Demo

![https://www.youtube.com/watch?v=86bYtJCwQ_o](https://cdn.discordapp.com/attachments/507519157387132940/808039024022257694/fourier.gif)
# Install

```sh
#Clone the repository
git clone git@github.com:MarcPartensky/Fourier.git
cd Fourier

#Install requirements
pip install -r requirements.txt
```

# Usage

Put your model image `image.png` in the `FourierImages` folder.

* Option 1: Give image at launch.

```sh
python __main__.py image.png
```

* Option 2: Launch then give the image.

```sh
python __main__.py
> image name:
```

Then give your image:

```sh
> image name:image.png
```

# Run with docker
```sh
# Replace the first occurence of 'FourierImages' by your custom image folder
# Replace 'rodolphe.jpg' by your own image too
docker-compose run \
    -v ./FourierImages:/opt/FourierImages \
    --entrypoint './__main__.py rodolphe.jpg' \
    fourier
```

# Description

There are 3 modes in this program:

* Mode 1: **Sampling**
Sample or draw a picture.

* Mode 2: **Drawing**
Watch the epicycles simulation which uses fourier transform.

* Mode 3: **Display**
Get the output image directly without waiting for the simulation.

# Controls

* `Space`: Switch to next mode.
* `Enter`: Go back to the center.
* `Up/Down/Right/Left Arrow`: Move arround.
* `Right/Left Shift`: Zoom in or out.
* `Quit/Escape`: Quit.
* `Z`: Cancel last sample.
* `R`: Remove all samples.
* `S`: Save the fourier-coefficients.

## Hide or Show the graphical components
Press the following numbers to toggle:
* `1`: Image
* `2`: Green lines
* `3`: Red graph
* `4`: White vectors
* `5`: Grey circles
* `6`: Yellow sample

# Enjoy!
