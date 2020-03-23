import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taskchain",
    version="0.0.1",
    author="Jiří Thran Řihák",
    author_email="jiri.rihak@plant.id",
    description="Utils for plant.id",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.org/flowerchecker/taskchain",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'tqdm',
        'pandas',
        'pytest',
        'pyyaml',
    ]
)
