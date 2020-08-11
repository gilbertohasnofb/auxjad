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
from .core.Shuffler import Shuffler
from .core.TenneySelector import TenneySelector
from .core.WindowLooper import WindowLooper

from .score.ArtificialHarmonic import ArtificialHarmonic
from .score.HarmonicNote import HarmonicNote
from .score.LeafDynMaker import LeafDynMaker

from .inspections.inspect import Inspection
from .inspections.inspect import inspect

from .mutations.mutate import Mutation
from .mutations.mutate import mutate

from .utilities.close_container import close_container
from .utilities.enforce_time_signature import enforce_time_signature
from .utilities.fill_with_rests import fill_with_rests
from .utilities.repeat_container import repeat_container
from .utilities.simplified_time_signature_ratio import (
    simplified_time_signature_ratio,
)
from .utilities.sync_containers import sync_containers
from .utilities.time_signature_extractor import time_signature_extractor


__author__ = "Gilberto Agostinho <gilbertohasnofb@gmail.com>"
__version__ = "0.8.9"
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
    'close_container',
    'enforce_time_signature',
    'fill_with_rests',
    'repeat_container',
    'simplified_time_signature_ratio',
    'sync_containers',
    'time_signature_extractor',
]
