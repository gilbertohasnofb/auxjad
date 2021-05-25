"""
mutations
=========

Auxjad's mutation functions. These can be accesses via either:

>>> abjad.mutate.auxjad_function(container)
>>> auxjad.mutate.auxjad_function(container)
"""

from .auto_rewrite_meter import auto_rewrite_meter
from .close_container import close_container
from .double_barlines_before_time_signatures import (
    double_barlines_before_time_signatures
)
from .enforce_time_signature import enforce_time_signature
from .extract_trivial_tuplets import extract_trivial_tuplets
from .fill_with_rests import fill_with_rests
from .merge_partial_tuplets import merge_partial_tuplets
from .prettify_rewrite_meter import prettify_rewrite_meter
from .remove_repeated_dynamics import remove_repeated_dynamics
from .remove_repeated_time_signatures import remove_repeated_time_signatures
from .reposition_clefs import reposition_clefs
from .reposition_dynamics import reposition_dynamics
from .reposition_slurs import reposition_slurs
from .respell_accidentals import respell_accidentals
from .rests_to_multimeasure_rest import rests_to_multimeasure_rest
from .sustain_notes import sustain_notes
from .sync_containers  import sync_containers
