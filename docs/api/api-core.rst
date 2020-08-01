core
====

The |core|_ subpackage contains the core classes of the |auxjad|_ package.
The include random selectors, loopers, phasers, and other classes for
algorithmic manipulation of material.

..  note::

    These classes are imported directly into the |auxjad|_ namespace.
    Therefore, to use a class such as :class:`auxjad.CartographySelector` you
    only  need to import |auxjad|_ and instantiate the class from itsnamespace:

    >>> import auxjad
    >>> selector = auxjad.CartographySelector(pitch_list)

Below is the full list of classes included in |core|_. Click on their names
for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.CartographySelector
    auxjad.Drifter
    auxjad.Fader
    auxjad.Hocketer
    auxjad.LeafLooper
    auxjad.ListLooper
    auxjad.Phaser
    auxjad.PitchRandomiser
    auxjad.Shuffler
    auxjad.TenneySelector
    auxjad.WindowLooper

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |core| replace:: :mod:`core <auxjad.core>`
.. _core: api-core.html

.. include:: abjad-targets.rst
