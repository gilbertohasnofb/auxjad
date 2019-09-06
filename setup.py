try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import auxjad

auxjad_classifiers = [
    "Development Status :: 5 - Production/Stable",
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3 :: Only',
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    'Topic :: Software Development :: Libraries :: Python Modules',
    "Topic :: Utilities",
]

with open("README.rst", "r") as fp:
    auxjad_long_description = fp.read()

setup(
    name='auxjad',
    description='Auxiliary functions and classes for Abjad 3.0.',
    author='Gilberto Agostinho',
    author_email='gilbertohasnofb@gmail.com',
    version=auxjad.__version__,
    packages=find_packages(),
    url='https://github.com/gilbertohasnofb/auxjad',
    license='MIT',
    long_description=auxjad_long_description,
    tests_require=['pytest'],
    classifiers=auxjad_classifiers,
    python_requires='>=3.6',
)
