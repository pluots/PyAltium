import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyAltium",
    version="0.1.0",
    author="Trevor Gross",
    author_email="t.gross35@gmail.com",
    description="A package for reading Altium files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tgross35/PyAltium",
        project_urls={
            "Bug Tracker": "https://github.com/tgross35/PyAltium/issues",
        },
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
)
