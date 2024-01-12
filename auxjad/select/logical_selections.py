from functools import partial
from typing import Union

import abjad


def _group_consecutive_rests(logical_tie: abjad.LogicalTie,
                             *,
                             include_multimeasure_rests: bool = True,
                             ) -> Union[abjad.Leaf, bool]:
    r"""Private function used by |auxjad.select.logical_selections()| in order
    to group consecutive ties together. If a logical tie is made out of a rest,
    this function returns the value ``True``, otherwise it returns the logical
    tie's head object itself. When this output is used with
    |abjad.select.group_by()|, consecutive ``True`` values will be grouped
    together, thus selecting consecutive rests as a single 'logical selection'.
    Meanwhile, non-rest logical ties will return their individual unique head
    object, maintaining their individual selections as is.
    """
    if isinstance(logical_tie.head, abjad.Rest):
        return True
    elif (isinstance(logical_tie.head, abjad.MultimeasureRest)
            and include_multimeasure_rests):
        return True
    else:
        return logical_tie.head


def logical_selections(container: Union[abjad.Container, abjad.Selection],
                       *,
                       include_multimeasure_rests: bool = True,
                       ) -> abjad.Selection:
    r"""Takes an |abjad.Container| (or child class).
    Returns the logical selections of a container, that is the logical
    ties but with consecutive rests grouped together. Return value is in the
    form of a |abjad.Selection| of |abjad.Selection|'s.

    Basic usage:
        Usage is similar to |abjad.select.logical_ties()|:

        >>> container = abjad.Container(r"c'4 ~ c'16 r8. r4.. d'16 ~ d'4")
        >>> logical_selections = auxjad.select.logical_selections(container)
        >>> for logical_selection in logical_selections:
        ...     print(logical_selection.leaves())
        Selection([Note("c'4"), Note("c'16")])
        Selection([Rest('r8.'), Rest('r4..')])
        Selection([Note("d'16"), Note("d'4")])

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.select|. It can thus be used from either |auxjad.select|_ or
        |abjad.select| namespaces. Therefore, the two lines below are
        equivalent:

        >>> container = abjad.Container(r"c'4 ~ c'16 r8. r4.. d'16 ~ d'4")
        >>> for logical_sel in auxjad.select.logical_selections(container):
        ...     print(logical_sel.leaves())
        Selection([Note("c'4"), Note("c'16")])
        Selection([Rest('r8.'), Rest('r4..')])
        Selection([Note("d'16"), Note("d'4")])
        >>> for logical_sel in abjad.select.logical_selections(container):
        ...     print(logical_sel.leaves())
        Selection([Note("c'4"), Note("c'16")])
        Selection([Rest('r8.'), Rest('r4..')])
        Selection([Note("d'16"), Note("d'4")])

    ``include_multimeasure_rests``:
        By default, this function groups multi-measure rests with the previous
        pitched leaf as a single logical selection.

        >>> container = abjad.Container(r"c'2. ~ c'16 r8. R1 r4.. d'16 ~ d'2.")
        >>> logical_selections = auxjad.select.logical_selections(container)
        >>> for logical_selection in logical_selections:
        ...     print(logical_selection.leaves())
        Selection([Note("c'2."), Note("c'16")])
        Selection([Rest('r8.'), MultimeasureRest('R1'), Rest('r4..')])
        Selection([Note("d'16"), Note("d'2.")])

        To treat multi-measure rests as their own logical selections, set
        ``include_multimeasure_rests`` to ``False`` (default value is
        ``True``).

        >>> container = abjad.Container(r"c'2. ~ c'16 r8. R1 r4.. d'16 ~ d'2.")
        >>> logical_selections = auxjad.select.logical_selections(
        ...     container,
        ...     include_multimeasure_rests=False,
        ... )
        >>> for logical_selection in logical_selections:
        ...     print(logical_selection.leaves())
        Selection([Note("c'2."), Note("c'16")])
        Selection([Rest('r8.')])
        Selection([MultimeasureRest('R1')])
        Selection([Rest('r4..')])
        Selection([Note("d'16"), Note("d'2.")])
    """
    if not isinstance(container, (abjad.Container, abjad.Selection)):
        raise TypeError("Argument must be 'abjad.Container', 'abjad.Selection'"
                        ", or child classes")
    if isinstance(container, abjad.Container):
        if not abjad.select(container).leaves().are_contiguous_logical_voice():
            raise ValueError("Argument must be contiguous logical voice")

    logical_ties = abjad.select(container).logical_ties()
    return logical_ties.group_by(
        partial(_group_consecutive_rests,
                include_multimeasure_rests=include_multimeasure_rests,
                )
    )
