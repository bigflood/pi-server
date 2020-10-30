import setuptools
import pi_server

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = list(filter(bool, f.read().splitlines()))

setuptools.setup(
    name="pi_server",
    version=pi_server.__version__,
    author="Taesu Pyo",
    author_email="pyotaesu@gmail.com",
    description="pi-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bigflood/pi-server",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
)
