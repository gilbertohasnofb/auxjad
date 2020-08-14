score
=====

The |score|_ subpackage include score component and component maker classes
such as an expanded leaf maker as well as harmonic leaves.

.. note::

    These classes are imported directly into the |auxjad|_ namespace.
    Therefore, to use a class such as :class:`auxjad.ArtificialHarmonic` you
    only need to import |auxjad|_ and instantiate the class from its namespace:

    >>> import auxjad
    >>> note = auxjad.ArtificialHarmonic(r"<c' f'>4")

Below is the full list of classes included in |score|_. Click on their names
for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.ArtificialHarmonic
    auxjad.HarmonicNote
    auxjad.LeafDynMaker

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |score| replace:: :mod:`score <auxjad.score>`
.. _score: api-score.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
