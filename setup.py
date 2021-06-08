from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Shortcuts for matplotlib'
LONG_DESCRIPTION = 'i just want graphs not programming!'

# Setting up
setup(
    name="plotx",
    version=VERSION,
    author="DaveAsator (Eugene Bolshakov)",
    author_email="<omnispark@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords=['plot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers, Mathematicians, BI",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)