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
from ._version import __version__
from .core.CartographySelector import CartographySelector
from .core.CrossFader import CrossFader
from .core.DeBruijnGenerator import DeBruijnGenerator
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
from .score.Context import Context, Staff, StaffGroup, Voice
from .score.HarmonicNote import HarmonicNote
from .score.Score import Score
from .spanners.piano_pedal import piano_pedal
from .utils.staff_splitter import staff_splitter

__author__ = "Gilberto Agostinho <gilbertohasnofb@gmail.com>"
__all__ = [
    "__author__",
    "__version__",
    "get",
    "mutate",
    "select",
    "CartographySelector",
    "CrossFader",
    "DeBruijnGenerator",
    "Echoer",
    "Fader",
    "GeneticAlgorithm",
    "Hocketer",
    "LeafLooper",
    "ListLooper",
    "Phaser",
    "PitchRandomiser",
    "Repeater",
    "Shuffler",
    "TenneySelector",
    "WindowLooper",
    "TimeSignature",
    "GeneticAlgorithmMusicMaker",
    "LeafDynMaker",
    "ArtificialHarmonic",
    "Context",
    "HarmonicNote",
    "Score",
    "Staff",
    "StaffGroup",
    "Voice",
    "piano_pedal",
    "staff_splitter",
]
