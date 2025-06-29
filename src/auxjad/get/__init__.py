"""
get
===

Auxjad's inspection functions. These can be accesses via either:

>>> abjad.get.auxjad_function(container)
>>> auxjad.get.auxjad_function(container)
"""

import abjad

from .leaves_are_tieable import leaves_are_tieable
from .rhythms_are_identical import rhythms_are_identical
from .selection_is_full import selection_is_full
from .selections_are_identical import selections_are_identical
from .time_signature_list import time_signature_list
from .underfull_duration import underfull_duration
from .virtual_fundamental import virtual_fundamental

### EXTENSION FUNCTIONS ###

abjad.get.leaves_are_tieable = leaves_are_tieable
abjad.get.rhythms_are_identical = rhythms_are_identical
abjad.get.selection_is_full = selection_is_full
abjad.get.selections_are_identical = selections_are_identical
abjad.get.time_signature_list = time_signature_list
abjad.get.underfull_duration = underfull_duration
abjad.get.virtual_fundamental = virtual_fundamental
