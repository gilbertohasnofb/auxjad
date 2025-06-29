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

from auxjad.core.CartographySelector import CartographySelector
from auxjad.core.CrossFader import CrossFader
from auxjad.core.Echoer import Echoer
from auxjad.core.Fader import Fader
from auxjad.core.GeneticAlgorithm import GeneticAlgorithm
from auxjad.core.Hocketer import Hocketer
from auxjad.core.LeafLooper import LeafLooper
from auxjad.core.ListLooper import ListLooper
from auxjad.core.Phaser import Phaser
from auxjad.core.PitchRandomiser import PitchRandomiser
from auxjad.core.Repeater import Repeater
from auxjad.core.Shuffler import Shuffler
from auxjad.core.TenneySelector import TenneySelector
from auxjad.core.WindowLooper import WindowLooper

from auxjad.indicators.TimeSignature import TimeSignature

from auxjad.makers.GeneticAlgorithmMusicMaker import GeneticAlgorithmMusicMaker
from auxjad.makers.LeafDynMaker import LeafDynMaker

from auxjad.score.ArtificialHarmonic import ArtificialHarmonic
from auxjad.score.HarmonicNote import HarmonicNote
from auxjad.score.Score import Score

from auxjad.spanners.piano_pedal import piano_pedal

from auxjad.utilities.staff_splitter import staff_splitter

from auxjad import get

from auxjad import mutate

from auxjad import select


__author__ = 'Gilberto Agostinho <gilbertohasnofb@gmail.com>'
__version__ = '1.0.3'
__all__ = [
    '__author__',
    '__version__',
    'CartographySelector',
    'CrossFader',
    'Echoer',
    'Fader',
    'GeneticAlgorithm',
    'Hocketer',
    'GeneticAlgorithmMusicMaker',
    'LeafLooper',
    'ListLooper',
    'Phaser',
    'PitchRandomiser',
    'Repeater',
    'Shuffler',
    'TenneySelector',
    'WindowLooper',
    'TimeSignature',
    'LeafDynMaker',
    'ArtificialHarmonic',
    'HarmonicNote',
    'Score',
    'piano_pedal',
    'staff_splitter',
    'get',
    'mutate',
    'select',
]
