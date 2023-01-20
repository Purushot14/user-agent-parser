"""
    Created by prakash at 02/03/22
"""
__author__ = 'Purushot14'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="user-agent-parser",  # This is the name of the package
    version="0.1.2",
    author="Purushot14",  # Full name of the author
    author_email="prakash.purushoth@gmail.com",
    description="Parser User agent string and get device details",
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=["user_agent_parser"],  # List of all python modules to be installed
    url="https://github.com/Purushot14/user-agent-parser",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Intended Audience :: Developers'
    ],  # Information to filter the project on PyPi website
    python_requires='>=3.6',  # Minimum version requirement of the package
    install_requires=[]  # Install other dependencies if any
)
