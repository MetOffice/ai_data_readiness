# (C) British Crown Copyright 2017-2025, Met Office.
# Please see LICENSE.md for license details.

from setuptools import setup, find_packages

setup(
    name="aidatareadiness",
    version="0.0.1",
    description="Placeholder",
    url= "https://github.com/informatics-lab/ai_data_readiness",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7, <4",
    install_requires=[],
)
