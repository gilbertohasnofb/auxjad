makers
======

The |makers|_ subpackage includes leaf making classes.

..  note::

    These classes are imported directly into the |auxjad|_ namespace.
    Therefore, to use a class such as :class:`auxjad.LeafDynMaker` you only
    need to import |auxjad|_ and instantiate the class from its namespace:

    >>> import auxjad
    >>> maker = auxjad.LeafDynMaker()

Below is the full list of classes included in |makers|_. Click on their names
for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    GeneticAlgorithmMusicMaker
    LeafDynMaker

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
