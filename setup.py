import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fourier_drawing",
    version="0.0.8",
    author="Mazex",
    author_email="marc.partensky@gmail.com",
    description="Use fourier transform to draw epicycles with your drawings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcPartensky/Fourier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
