try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import setup, find_packages

import auxjad

auxjad_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3 :: Only',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
]

with open('README.rst', 'r') as file:
    auxjad_long_description = file.read()

setup(
    name='auxjad',
    description='Auxiliary functions and classes for Abjad 3.1.',
    author='Gilberto Agostinho',
    author_email='gilbertohasnofb@gmail.com',
    version=auxjad.__version__,
    packages=find_packages(),
    url='https://github.com/gilbertohasnofb/auxjad',
    license='MIT',
    long_description=auxjad_long_description,
    tests_require=['abjad==3.1', 'pytest'],
    classifiers=auxjad_classifiers,
    python_requires='>=3.6',
    install_requires=['abjad==3.1', 'setuptools'],
    extras_require={'test' : ['flake8', 'isort', 'pytest']},
)
