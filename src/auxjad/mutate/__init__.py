"""
mutate
======

Auxjad's mutation functions. These can be accesses via either:

>>> abjad.mutate.auxjad_function(container)
>>> auxjad.mutate.auxjad_function(container)
"""

import abjad

from .auto_rewrite_meter import auto_rewrite_meter
from .close_container import close_container
from .contract_notes import contract_notes
from .enforce_time_signature import enforce_time_signature
from .extend_notes import extend_notes
from .extract_trivial_tuplets import extract_trivial_tuplets
from .fill_with_rests import fill_with_rests
from .merge_hairpins import merge_hairpins
from .merge_partial_tuplets import merge_partial_tuplets
from .prettify_rewrite_meter import prettify_rewrite_meter
from .remove_repeated_dynamics import remove_repeated_dynamics
from .remove_repeated_time_signatures import remove_repeated_time_signatures
from .reposition_clefs import reposition_clefs
from .reposition_dynamics import reposition_dynamics
from .reposition_slurs import reposition_slurs
from .respell_augmented_unisons import respell_augmented_unisons
from .rests_to_multimeasure_rest import rests_to_multimeasure_rest
from .sustain_notes import sustain_notes
from .sync_containers import sync_containers

### EXTENSION FUNCTIONS ###

abjad.mutate.auto_rewrite_meter = auto_rewrite_meter
abjad.mutate.close_container = close_container
abjad.mutate.contract_notes = contract_notes
abjad.mutate.enforce_time_signature = enforce_time_signature
abjad.mutate.extend_notes = extend_notes
abjad.mutate.extract_trivial_tuplets = extract_trivial_tuplets
abjad.mutate.fill_with_rests = fill_with_rests
abjad.mutate.merge_hairpins = merge_hairpins
abjad.mutate.merge_partial_tuplets = merge_partial_tuplets
abjad.mutate.prettify_rewrite_meter = prettify_rewrite_meter
abjad.mutate.remove_repeated_dynamics = remove_repeated_dynamics
abjad.mutate.remove_repeated_time_signatures = remove_repeated_time_signatures
abjad.mutate.reposition_clefs = reposition_clefs
abjad.mutate.reposition_dynamics = reposition_dynamics
abjad.mutate.reposition_slurs = reposition_slurs
abjad.mutate.respell_augmented_unisons = respell_augmented_unisons
abjad.mutate.rests_to_multimeasure_rest = rests_to_multimeasure_rest
abjad.mutate.sustain_notes = sustain_notes
abjad.mutate.sync_containers = sync_containers
