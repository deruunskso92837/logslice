from setuptools import setup

setup(
    name="logslice",
    version="0.1.0",
    py_modules=["logslice"],
    entry_points={"console_scripts": ["logslice=logslice:main"]},
    python_requires=">=3.9",
    description="Fast log file parser with pattern matching",
    author="Derek Unsworth",
)
