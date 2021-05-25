"""
getters
=======

Auxjad's getter functions. These can be accesses via either:

>>> abjad.get.auxjad_function(container)
>>> auxjad.get.auxjad_function(container)
"""

from .extract_time_signatures import extract_time_signatures
from .leaves_are_tieable import leaves_are_tieable
from .selection_is_full import selection_is_full
from .selections_are_identical import selections_are_identical
from .underfull_duration import underfull_duration
