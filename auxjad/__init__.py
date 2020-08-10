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

from .inspections.leaves_are_tieable import leaves_are_tieable
from .inspections.selection_is_full import selection_is_full
from .inspections.selections_are_equal import selections_are_equal
from .inspections.underfull_duration import underfull_duration

from .mutations.prettify_rewrite_meter import prettify_rewrite_meter
from .mutations.remove_empty_tuplets import remove_empty_tuplets
from .mutations.remove_repeated_dynamics import remove_repeated_dynamics
from .mutations.remove_repeated_time_signatures import (
    remove_repeated_time_signatures,
)
from .mutations.reposition_clefs import reposition_clefs
from .mutations.reposition_dynamics import reposition_dynamics
from .mutations.reposition_slurs import reposition_slurs
from .mutations.respell_accidentals import respell_accidentals
from .mutations.rests_to_multimeasure_rest import rests_to_multimeasure_rest

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
    'leaves_are_tieable',
    'selection_is_full',
    'selections_are_equal',
    'underfull_duration',
    'prettify_rewrite_meter',
    'remove_empty_tuplets',
    'remove_repeated_dynamics',
    'remove_repeated_time_signatures',
    'reposition_clefs',
    'reposition_dynamics',
    'reposition_slurs',
    'respell_accidentals',
    'rests_to_multimeasure_rest',
    'close_container',
    'enforce_time_signature',
    'fill_with_rests',
    'repeat_container',
    'simplified_time_signature_ratio',
    'sync_containers',
    'time_signature_extractor',
]
