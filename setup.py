from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="termchart",
    version="1.0.0",
    description="Render Unicode bar charts, line charts, histograms and scatter plots in the terminal from any CSV file. Zero dependencies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NzJulien",
    url="https://github.com/NzJulien/termchart",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    extras_require={"dev": ["pytest>=7.0"]},
    entry_points={"console_scripts": ["termchart=termchart.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
)
