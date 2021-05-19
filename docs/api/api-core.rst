core
====

The |core|_ subpackage contains the core classes of the |auxjad|_ package.
The include random selectors, loopers, phasers, and other classes for
algorithmic manipulation of material.

.. note::

    These classes are imported directly into the |auxjad|_ namespace.
    Therefore, to use a class such as :class:`auxjad.CartographySelector` you
    only need to import |auxjad|_ and instantiate the class from its namespace:

    >>> import auxjad
    >>> selector = auxjad.CartographySelector(pitch_list)

Below is the full list of classes included in |core|_. Click on their names
for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    CartographySelector
    CrossFader
    Fader
    FittestMeasureMaker
    GeneticAlgorithm
    Hocketer
    LeafLooper
    ListLooper
    Phaser
    PitchRandomiser
    Repeater
    Shuffler
    TenneySelector
    WindowLooper

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
