score
=====

The |score|_ subpackage include score component classes such as harmonic
leaf classes as well as extension methods to |abjad.Score|.

..  note::

    These classes are imported directly into the |auxjad|_ namespace.
    Therefore, to use a class such as :class:`auxjad.ArtificialHarmonic` you
    only need to import |auxjad|_ and instantiate the class from its namespace:

    >>> import auxjad
    >>> note = auxjad.ArtificialHarmonic(r"<c' f'>4")

Below is the full list of classes included in |score|_. Click on their names
for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    ArtificialHarmonic
    HarmonicNote
    Score.add_double_bar_lines_before_time_signatures
    Score.add_final_bar_line

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
