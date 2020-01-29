import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ToyData",
    version="1.0",
    author="Xiangzhuang Shen",
    author_email="datahonor@gmail.com",
    description="An easy-to-use algorithms timer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shenxiangzhuang/ToyData",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)