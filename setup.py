#!/usr/bin/python3

from setuptools import setup

setup(
    name='torrent-creator',
    version='1.0',
    description='A command line application that allows you to create torrent files',
    install_requires=['bencoder.pyx==1.1.3'],
    packages=['torrent_creator'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'torrent-creator = torrent_creator.torrent_creator:main'
        ]
    },
    zip_safe=False,
)
