import os

from setuptools import find_packages
from setuptools import setup

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.rst')) as fp:
    long_description = fp.read()

setup(
    name='iterm2-dwim',
    url='https://github.com/dandavison/iterm2-dwim',
    version=(open(os.path.join(os.path.dirname(__file__),
                               'version.txt'))
             .read().strip()),
    author='Dan Davison',
    author_email='dandavison7@gmail.com',
    description="iTerm2 click handler",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'iterm2-dwim = iterm2_dwim:main',
        ],
    },
)
