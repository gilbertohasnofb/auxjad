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

from . import get, mutate, select

from .core.CartographySelector import CartographySelector
from .core.CrossFader import CrossFader
from .core.Echoer import Echoer
from .core.Fader import Fader
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

from .makers.GeneticAlgorithmMusicMaker import GeneticAlgorithmMusicMaker
from .makers.LeafDynMaker import LeafDynMaker

from .score.ArtificialHarmonic import ArtificialHarmonic
from .score.HarmonicNote import HarmonicNote
from .score.Score import Score

from .spanners.piano_pedal import piano_pedal

from .utilities.staff_splitter import staff_splitter

from ._version import __version__


__author__ = 'Gilberto Agostinho <gilbertohasnofb@gmail.com>'
__all__ = [
    '__author__',
    '__version__',
    # modules
    'get',
    'mutate',
    'select',
    # core
    'CartographySelector',
    'CrossFader',
    'Echoer',
    'Fader',
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
    # indicators
    'TimeSignature',
    # makers
    'GeneticAlgorithmMusicMaker',
    'LeafDynMaker',
    # score
    'ArtificialHarmonic',
    'HarmonicNote',
    'Score',
    # spanners
    'piano_pedal',
    # utilities
    'staff_splitter',
]
