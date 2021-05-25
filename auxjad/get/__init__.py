"""
getters
=======

Auxjad's getter functions. These can be accesses via either:

>>> abjad.get.auxjad_function(container)
>>> auxjad.get.auxjad_function(container)
"""

import abjad

from .extract_time_signatures import extract_time_signatures
from .leaves_are_tieable import leaves_are_tieable
from .selection_is_full import selection_is_full
from .selections_are_identical import selections_are_identical
from .underfull_duration import underfull_duration
from .virtual_fundamental import virtual_fundamental

### EXTENSION FUNCTIONS ###

abjad.get.extract_time_signatures = extract_time_signatures
abjad.get.leaves_are_tieable = leaves_are_tieable
abjad.get.selection_is_full = selection_is_full
abjad.get.selections_are_identical = selections_are_identical
abjad.get.underfull_duration = underfull_duration
abjad.get.virtual_fundamental = virtual_fundamental
