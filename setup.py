import os

from setuptools import find_packages
from setuptools import setup


setup(
    name='iterm2-dwim',
    version=(open(os.path.join(os.path.dirname(__file__),
                               'version.txt'))
             .read().strip()),
    author='Dan Davison',
    author_email='dandavison7@gmail.com',
    description="iTerm2 click handler",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'iterm2-dwim = iterm2_dwim:main',
        ],
    },
)
