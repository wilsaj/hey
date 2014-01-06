"""
hey
===

a cross-platform client/server for communicating with processes less-than-synchronously
"""
from setuptools import setup

setup(
    name='hey',
    version='0.1-dev',
    url='http://github.com/wilsaj/hey/',
    license='BSD',
    author='Andy Wilson',
    author_email='wilson.andrew.j@gmail.com',
    description='a cross-platform client/server for communicating with processes less-than-synchronously',
    long_description=__doc__,
    packages=['hey'],
    platforms='any',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: System :: Operating System',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
