#! /usr/bin/env python
import setuptools


auxjad_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Topic :: Artistic Software',
    'Topic :: Utilities',
]

install_requires = [
    'abjad==3.4',
    'flake8',
    'isort',
    'pydocstyle',
    'pytest',
    'setuptools',
]

keywords = [
    'algorithmic composition',
    'generative music',
    'music composition',
    'music notation',
    'lilypond',
    'abjad',
]

if __name__ == '__main__':
    setuptools.setup(
        author_email='gilbertohasnofb@gmail.com',
        author='Gilberto Agostinho',
        classifiers=auxjad_classifiers,
        description='Auxiliary classes and functions for Abjad.',
        install_requires=install_requires,
        license='MIT',
        long_description='Auxjad is a library of auxiliary classes and functions for Abjad 3.4 aimed at composers of algorithmic music.',
        name='auxjad',
        packages=['auxjad'],
        platforms='Any',
        python_requires='>=3.9',
        url='https://gilbertohasnofb.github.io/auxjad-docs/',
        version='1.0.3',
    )
