"""
Auxjad
======

Auxjad is a library of auxiliary classes and functions for Abjad 3.4 aimed at
composers of algorithmic music. All classes and functions have a ``__doc__``
attribute with usage instructions.

Documentation is available at https://gilbertohasnofb.github.io/auxjad-docs/.

Bugs can be reported through the project's Issue Tracker.

This library is published under the MIT License.
"""

from .core.CartographySelector import CartographySelector
from .core.CrossFader import CrossFader
from .core.Fader import Fader
from .core.FittestMeasureMaker import FittestMeasureMaker
from .core.GeneticAlgorithm import GeneticAlgorithm
from .core.Hocketer import Hocketer
from .core.LeafLooper import LeafLooper
from .core.ListLooper import ListLooper
from .core.Phaser import Phaser
from .core.PitchRandomiser import PitchRandomiser
from .core.Repeater import Repeater
from .core.Shuffler import Shuffler
from .core.TenneySelector import TenneySelector
from .core.WindowLooper import WindowLooper

from .indicators.TimeSignature import TimeSignature

from .score.ArtificialHarmonic import ArtificialHarmonic
from .score.HarmonicNote import HarmonicNote
from .score.LeafDynMaker import LeafDynMaker

from .spanners.half_piano_pedal import half_piano_pedal
from .spanners.piano_pedal import piano_pedal

from . import get

from . import mutate


__author__ = "Gilberto Agostinho <gilbertohasnofb@gmail.com>"
__version__ = "0.9.0"
__all__ = [
    '__author__',
    '__version__',
    'CartographySelector',
    'CrossFader',
    'Fader',
    'FittestMeasureMaker',
    'GeneticAlgorithm',
    'Hocketer',
    'LeafLooper',
    'ListLooper',
    'Phaser',
    'PitchRandomiser',
    'Repeater',
    'Shuffler',
    'TenneySelector',
    'WindowLooper',
    'TimeSignature',
    'ArtificialHarmonic',
    'HarmonicNote',
    'LeafDynMaker',
    'half_piano_pedal',
    'piano_pedal',
    'get',
    'mutate',
]
