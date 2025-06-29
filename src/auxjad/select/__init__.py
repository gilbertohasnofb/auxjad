"""
select
======

Auxjad's selection functions. These can be accesses via either:

>>> abjad.select.auxjad_function(container)
>>> auxjad.select.auxjad_function(container)
"""

import abjad

from .logical_selections import logical_selections

### EXTENSION FUNCTIONS ###

abjad.select.logical_selections = logical_selections
