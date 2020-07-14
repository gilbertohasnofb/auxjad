"""auxjad
======

``auxjad`` is a library of auxiliary functions and classes for Abjad 3.1 aimed
at composers of algorithmic music. All classes and functions have a __doc__
attribute with usage instructions.

Documentation is available at https://gilbertohasnofb.github.io/auxjad-docs/.

Bugs can be reported through the project's Issue Tracker.

This library is published under the MIT License.
"""

from .core.Adrifter import Adrifter
from .core.CartographySelector import CartographySelector
from .core.Fader import Fader
from .core.Hocketer import Hocketer
from .core.LeafDynMaker import LeafDynMaker
from .core.LoopByList import LoopByList
from .core.LoopByNotes import LoopByNotes
from .core.LoopByWindow import LoopByWindow
from .core.Phaser import Phaser
from .core.Shuffler import Shuffler
from .core.TenneySelector import TenneySelector

from .entities.ArtificialHarmonic import ArtificialHarmonic
from .entities.HarmonicNote import HarmonicNote

from .utilities.close_container import close_container
from .utilities.container_is_full import container_is_full
from .utilities.containers_are_equal import containers_are_equal
from .utilities.enforce_time_signature import enforce_time_signature
from .utilities.fill_with_rests import fill_with_rests
from .utilities.leaves_are_tieable import leaves_are_tieable
from .utilities.prettify_rewrite_meter import prettify_rewrite_meter
from .utilities.remove_empty_tuplets import remove_empty_tuplets
from .utilities.remove_repeated_dynamics import remove_repeated_dynamics
from .utilities.remove_repeated_time_signatures import (
    remove_repeated_time_signatures,
)
from .utilities.repeat_container import repeat_container
from .utilities.reposition_clefs import reposition_clefs
from .utilities.reposition_dynamics import reposition_dynamics
from .utilities.respell_container import respell_container
from .utilities.respell_chord import respell_chord
from .utilities.rests_to_multimeasure_rest import rests_to_multimeasure_rest
from .utilities.simplified_time_signature_ratio import (
    simplified_time_signature_ratio,
)
from .utilities.sync_containers import sync_containers
from .utilities.time_signature_extractor import time_signature_extractor
from .utilities.underfull_duration import underfull_duration


__author__ = "Gilberto Agostinho <gilbertohasnofb@gmail.com>"
__version__ = "0.8.0"
__all__ = [
    '__author__',
    '__version__',
    'Adrifter',
    'CartographySelector',
    'Fader',
    'Hocketer',
    'LeafDynMaker',
    'LoopByList',
    'LoopByNotes',
    'LoopByWindow',
    'Phaser',
    'Shuffler',
    'TenneySelector',
    'ArtificialHarmonic',
    'HarmonicNote',
    'close_container',
    'container_is_full',
    'containers_are_equal',
    'enforce_time_signature',
    'fill_with_rests',
    'leaves_are_tieable',
    'prettify_rewrite_meter',
    'remove_empty_tuplets',
    'remove_repeated_dynamics',
    'remove_repeated_time_signatures',
    'repeat_container',
    'reposition_clefs',
    'reposition_dynamics',
    'respell_container',
    'respell_chord',
    'rests_to_multimeasure_rest',
    'simplified_time_signature_ratio',
    'sync_containers',
    'time_signature_extractor',
    'underfull_duration',
]
