import os

from setuptools import find_packages
from setuptools import setup

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")) as fp:
    long_description = fp.read()

setup(
    name="open-in-editor",
    url="https://github.com/dandavison/open-in-editor",
    version=(open(os.path.join(os.path.dirname(__file__), "version.txt")).read().strip()),
    author="Dan Davison",
    author_email="dandavison7@gmail.com",
    description="Open a local file at a line number in an editor/IDE of your choice",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["open-in-editor = open_in_editor:main"]},
)
