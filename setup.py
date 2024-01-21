from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="deepspace_helper",
    version="0.1.0",
    url="https://github.com/ShirleySprite/deepspace_helper",
    author="Sprite",
    author_email="583882690s@gmail.com",
    description="Deepspace Helper",
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    license="Apache 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy ~= 1.26.3",
        "pandas ~= 2.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
