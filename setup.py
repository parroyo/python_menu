# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
from pip.req import parse_requirements
import io

import menu

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]


config = {
    'name': 'python-menu',
    'version': menu.__version__,
    'description': 'Module to create simple console menus',
    'long_description': long_description,
    'author': 'Pablo Arroyo Loma',
    'author_email': 'pablo.arroyo.loma@gmail.com',
    'url': 'github',
    'download_url': 'Where to download it.',
    'install_requires': reqs,
    #'extra_require': {'testing': ['PyYaml']},
    #'packages': ['menu'],
    'packages': find_packages(),
    #'py_modules': ['menu'],
    'platforms': 'unix',
    'keywords': ['dialog',
                 'ncurses',
                 'Xdialog',
                 'text-mode interface',
                 'terminal'],
    'classifiers': [
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha'
        'Natural Language :: English'
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux'
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Terminals']
}

setup(**config)
