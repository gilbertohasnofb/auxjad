score
=====

The ``score`` subpackage include score component classes such as artificial and
natural harmonics.

..  note::

    These classes are imported directly into the ``auxjad`` namespace.
    Therefore, to use a class such as :class:`ArtificialHarmonic` you only need
    to import ``auxjad`` and instantiate the class from its namespace:

    >>> import auxjad
    >>> note = auxjad.ArtificialHarmonic(r"<c' f'>4")

Below is the full list of classes included in ``score``. Click on their names
for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.ArtificialHarmonic
    auxjad.HarmonicNote
