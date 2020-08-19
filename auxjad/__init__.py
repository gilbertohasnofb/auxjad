"""
Auxjad
======

Auxjad is a library of auxiliary classes and functions for Abjad 3.1 aimed at
composers of algorithmic music. All classes and functions have a ``__doc__``
attribute with usage instructions.

Documentation is available at https://gilbertohasnofb.github.io/auxjad-docs/.

Bugs can be reported through the project's Issue Tracker.

This library is published under the MIT License.
"""

from .core.CartographySelector import CartographySelector
from .core.Drifter import Drifter
from .core.Fader import Fader
from .core.Hocketer import Hocketer
from .core.LeafLooper import LeafLooper
from .core.ListLooper import ListLooper
from .core.Phaser import Phaser
from .core.PitchRandomiser import PitchRandomiser
from .core.Repeater import Repeater
from .core.Shuffler import Shuffler
from .core.TenneySelector import TenneySelector
from .core.WindowLooper import WindowLooper

from .score.ArtificialHarmonic import ArtificialHarmonic
from .score.HarmonicNote import HarmonicNote
from .score.LeafDynMaker import LeafDynMaker

from .utilities.inspect import Inspection
from .utilities.inspect import inspect
from .utilities.mutate import Mutation
from .utilities.mutate import mutate
from .utilities.simplify_time_signature_ratio import (
    simplify_time_signature_ratio,
)


__author__ = "Gilberto Agostinho <gilbertohasnofb@gmail.com>"
__version__ = "0.8.10"
__all__ = [
    '__author__',
    '__version__',
    'CartographySelector',
    'Drifter',
    'Fader',
    'Hocketer',
    'LeafLooper',
    'ListLooper',
    'Phaser',
    'PitchRandomiser',
    'Repeater',
    'Shuffler',
    'TenneySelector',
    'WindowLooper',
    'ArtificialHarmonic',
    'HarmonicNote',
    'LeafDynMaker',
    'Inspection',
    'inspect',
    'Mutation',
    'mutate',
    'simplify_time_signature_ratio',
]
