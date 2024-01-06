from typing import Union

import abjad


def _group_consecutive_rests(logical_tie: abjad.LogicalTie,
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
    if isinstance(logical_tie.head, (abjad.Rest, abjad.MultimeasureRest)):
        return True
    else:
        return logical_tie.head


def logical_selections(container: Union[abjad.Container, abjad.Selection],
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

    Multi-measure rests:
        It also handles multi-measure rests.

        >>> container = abjad.Container(r"c'2. ~ c'16 r8. R1 r4.. d'16 ~ d'2.")
        >>> logical_selections = auxjad.select.logical_selections(container)
        >>> for logical_selection in logical_selections:
        ...     print(logical_selection.leaves())
        Selection([Note("c'2."), Note("c'16")])
        Selection([Rest('r8.'), MultimeasureRest('R1'), Rest('r4..')])
        Selection([Note("d'16"), Note("d'2.")])
    """
    if not isinstance(container, (abjad.Container, abjad.Selection)):
        raise TypeError("Argument must be 'abjad.Container', 'abjad.Selection'"
                        ", or child classes")
    if isinstance(container, abjad.Container):
        if not abjad.select(container).leaves().are_contiguous_logical_voice():
            raise ValueError("Argument must be contiguous logical voice")

    logical_ties = abjad.select(container).logical_ties()
    return logical_ties.group_by(_group_consecutive_rests)
