#! /usr/bin/env python
import ast
import importlib.util

import setuptools

PKG_DIR = 'auxjad'


def find_version():
    r"""Return value of __version__.

    Reference: https://stackoverflow.com/a/42269185/
    """
    version_file_path = importlib.util.find_spec(PKG_DIR).origin
    with open(version_file_path, 'r') as file_contents:
        root_node = ast.parse(file_contents.read())
        for node in ast.walk(root_node):
            if isinstance(node, ast.Assign):
                if (len(node.targets) == 1
                        and node.targets[0].id == '__version__'):
                    return node.value.s
    raise RuntimeError('Unable to find version string.')


with open('README.rst', 'r') as file:
    auxjad_long_description = file.read()


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
        long_description=auxjad_long_description,
        name='auxjad',
        packages=['auxjad'],
        platforms='Any',
        python_requires='>=3.9',
        url='https://gilbertohasnofb.github.io/auxjad-docs/',
        version=find_version(),
    )
