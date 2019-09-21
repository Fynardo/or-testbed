import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

    
setuptools.setup(
    name="or-testbed",
    version="1.0.2",
    author="Diego Noceda",
    author_email="dfynar@gmail.com",
    description="Operations Research Framework for building metaheuristic algorithms.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Fynardo/or-testbed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
