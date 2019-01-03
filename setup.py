import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="figma_export",
    version="0.1",
    author="Roman Aliyev",
    description="Exports components from any Figma document and saves them to files that can be easily imported to other applications.",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RomanAliyev/figma-export",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "figma_export = figma_export.__main__:main"
        ]
    }
)
