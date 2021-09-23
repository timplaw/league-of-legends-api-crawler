import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leaguestats",
    version="0.0.1",
    author="Tim Law",
    author_email="nasaartemis@protonmail.com",
    description="aggregates data to find best team comps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timplaw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8'
)