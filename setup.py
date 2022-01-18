import re

import setuptools

# from .src.pyaltium import __version__

with open("src/pyaltium/__init__.py") as f:
    txt = f.read()
    r = re.search(r'__version__\s+=\s+"(.*)"', txt)
    __version__ = r.group(1)

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="PyAltium",
    version=__version__,
    author="Trevor Gross",
    author_email="t.gross35@gmail.com",
    description="A package for reading Altium files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pluots/PyAltium",
    project_urls={
        "Bug Tracker": "https://github.com/pluots/PyAltium/issues",
    },
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.7",
)
