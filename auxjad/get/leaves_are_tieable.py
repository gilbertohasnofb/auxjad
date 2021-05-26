from collections.abc import Iterable
from typing import Union

import abjad


def leaves_are_tieable(leaves: Union[abjad.Selection,
                                     Iterable[abjad.Component],
                                     Iterable[abjad.LogicalTie],
                                     ],
                       ) -> bool:
    r"""Returns a :obj:`bool` representing whether or not two or more input
    leaves have identical pitch(es) and thus can be tied. Input argument can be
    a single |abjad.Selection| with multiple leaves, or an iterable with
    elements of type |abjad.Leaf| or child classes.

    Basic usage:
        When the pitches in both leaves are identical, this function returns
        ``True``:

        >>> leaf1 = abjad.Note(r"c'4")
        >>> leaf2 = abjad.Note(r"c'4")
        >>> auxjad.get.leaves_are_tieable([leaf1, leaf2])
        True

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.get|. It can thus be used from either |auxjad.get|_ or
        |abjad.get| namespaces. Therefore, the two lines below are equivalent:

        >>> leaf1 = abjad.Note(r"c'4")
        >>> leaf2 = abjad.Note(r"c'4")
        >>> auxjad.get.leaves_are_tieable([leaf1, leaf2])
        True
        >>> abjad.get.leaves_are_tieable([leaf1, leaf2])
        True

    Durations:
        Durations do not affect the comparison.

        >>> leaf1 = abjad.Note(r"c'2.")
        >>> leaf2 = abjad.Note(r"c'16")
        >>> leaf3 = abjad.Note(r"f'''16")
        >>> auxjad.get.leaves_are_tieable([leaf1, leaf2])
        True
        >>> auxjad.get.leaves_are_tieable([leaf1, leaf3])
        False
        >>> auxjad.get.leaves_are_tieable([leaf2, leaf3])
        False

    Chords:
        Handles chords as well as pitches.

        >>> chord1 = abjad.Chord(r"<c' e' g'>4")
        >>> chord2 = abjad.Chord(r"<c' e' g'>16")
        >>> chord3 = abjad.Chord(r"<f''' fs'''>16")
        >>> auxjad.get.leaves_are_tieable([chord1, chord2])
        True
        >>> auxjad.get.leaves_are_tieable([chord1, chord3])
        False
        >>> auxjad.get.leaves_are_tieable([chord2, chord3])
        False

    Parentage:
        Leaves can also be part of |abjad.Container|'s or child classes.

        >>> container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
        >>> auxjad.get.leaves_are_tieable([container[1], container[2]])
        True

    Rests:
        If rests are input, the return value is ``False``.

        >>> container = abjad.Container(r"r4 g'4 r2")
        >>> auxjad.get.leaves_are_tieable(leaves)
        False

    Multiple leaves:
        Accepts more than two notes:

        >>> leaf1 = abjad.Note(r"c'4")
        >>> leaf2 = abjad.Note(r"c'4")
        >>> leaf3 = abjad.Note(r"c'2.")
        >>> auxjad.get.leaves_are_tieable([leaf1, leaf2, leaf3])
        True

    Logical ties:
        Accepts leaves as well as |abjad.LogicalTie|'s:

        >>> leaf = abjad.Note(r"c'2.")
        >>> staff = abjad.Staff(r"c'4 ~ c'16")
        >>> logical_tie = abjad.select(staff).logical_tie(0)
        >>> auxjad.get.leaves_are_tieable([leaf, logical_tie])
        True

    Selections:
        Accepts a single |abjad.Selection| as input. It will consider all of
        its leaves.

        >>> staff = abjad.Staff(r"c'2 c'4. c'8")
        >>> auxjad.get.leaves_are_tieable(staff[:])
        True
        >>> staff = abjad.Staff(r"c'2 c'4. d'8")
        >>> auxjad.get.leaves_are_tieable(staff[:])
        False
    """
    if not isinstance(leaves, (abjad.Selection, Iterable)):
        raise TypeError("argument must be 'abjad.Selection' or an iterable of "
                        "'abjad.Component's or 'abjad.LogicalTie's")
    for leaf in leaves:
        if not isinstance(leaf, (abjad.Component, abjad.LogicalTie)):
            raise TypeError("argument must be 'abjad.Selection' or an "
                            "iterable of 'abjad.Component's or "
                            "'abjad.LogicalTie's")
    if len(leaves) == 1:
        raise ValueError("argument must contain two or more leaves")
    for index, leaf1 in enumerate(leaves[:-1]):
        for leaf2 in leaves[index + 1:]:
            if isinstance(leaf1, abjad.LogicalTie):
                leaf1 = leaf1[0]
            if isinstance(leaf2, abjad.LogicalTie):
                leaf2 = leaf2[0]
            if not isinstance(leaf1, type(leaf2)):
                return False
            if isinstance(leaf1, abjad.Rest):
                return False
            if isinstance(leaf1, abjad.MultimeasureRest):
                return False
            if (isinstance(leaf1, abjad.Note)
                    and leaf1.written_pitch != leaf2.written_pitch):
                return False
            if (isinstance(leaf1, abjad.Chord)
                    and leaf1.written_pitches != leaf2.written_pitches):
                return False
            leaf1_graces = abjad.get.before_grace_container(leaf1)
            leaf2_graces = abjad.get.before_grace_container(leaf2)
            if not isinstance(leaf1_graces, type(leaf2_graces)):
                return False
    return True
