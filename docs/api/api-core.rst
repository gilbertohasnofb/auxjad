core
====

The ``core`` subpackage contains the core classes of the ``auxjad`` package.
The include random selectors, loopers, phasers, and other classes for
algorithmic manipulation of material.

..  note::

    These classes are imported directly into the ``auxjad`` namespace.
    Therefore, to use a class such as ``CartographySelector`` you only need to
    import ``auxjad`` and invoke the function from its namespace:

    >>> import auxjad
    >>> selector = auxjad.CartographySelector(pitch_list)

Below is the full list of classes included in ``core``. Click on their names
for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.CartographySelector
    auxjad.Drifter
    auxjad.Fader
    auxjad.Hocketer
    auxjad.LeafDynMaker
    auxjad.LeafLooper
    auxjad.ListLooper
    auxjad.Phaser
    auxjad.PitchRandomiser
    auxjad.Shuffler
    auxjad.TenneySelector
    auxjad.WindowLooper
