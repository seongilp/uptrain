"""
A setuptools based setup module.
"""
#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="uptrain",
    version="0.0.4",
    description="UpTrain - ML Observability and Retraining Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/uptrain-ai/uptrain",
    # Author details
    maintainer="UpTrain AI Team",
    maintainer_email="uptrain.ai@gmail.com",
    # Choose your license
    license="Apache License 2.0",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here. In particular, ensure
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="uptrain ai retraining ML observability",
    packages=find_packages(),
    install_requires=[
        "numpy<1.24",
        "umap-learn>=0.5.3",
        "pandas>=1.0.0",
        "plotly>=5.0.0",
        "pydantic>=1.9.0",
        "scikit_learn>=1.0.0",
    ],
    tests_require=["pytest>=7.0", "torch", "imgaug", "gensim", "xgboost", "gensim"],
)
