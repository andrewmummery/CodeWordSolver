import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codewordsolver", # Name of module to import
    version="0.0.1",
    author="Andrew Mummery",
    author_email="andrew.mummery.software@gmail.com",
    description="A small package which solves codeword puzzles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewmummery/CodeWordSolver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)