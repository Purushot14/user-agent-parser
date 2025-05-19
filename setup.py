"""
    Created by prakash at 02/03/22
"""
__author__ = "Purushot14"
from pathlib import Path

from setuptools import find_packages, setup

this_dir = Path(__file__).parent
setup(
    name="user-agent-parser",
    version="0.1.5",
    description="Python 3 library to parse User-Agent strings and detect browser, OS and device details",
    long_description=(this_dir / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Purushot14",
    author_email="prakash.purushoth@gmail.com",
    url="https://github.com/Purushot14/user-agent-parser",
    project_urls={
        "Documentation": "https://github.com/Purushot14/user-agent-parser#readme",
        "Bug Tracker": "https://github.com/Purushot14/user-agent-parser/issues",
    },
    license="MIT",
    packages=find_packages(include=["user_agent_parser", "user_agent_parser.*"]),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
    ],
    keywords=[
        "user agent",
        "user-agent parser",
        "ua parser",
        "browser detection",
        "device detection",
        "python",
        "http",
        "analytics",
    ],
)
