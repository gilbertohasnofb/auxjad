import collections
from typing import Iterable, Union

import abjad


def leaves_are_tieable(leaves: Union[abjad.Selection,
                                     Iterable[Union[abjad.Component,
                                                    abjad.LogicalTie,
                                                    ]],
                                     ],
                       ) -> bool:
    r"""Returns a :obj:`bool` representing whether or not two or more input
    leaves have identical pitch(es) and thus can be tied. Input argument can
    be a single |abjad.Selection| with multiple leaves, or an iterable with
    elements of type |abjad.Leaf| or child classes.

    Basic usage:
        When the pitches in both leaves are identical, this function returns
        ``True``:

        >>> leaf1 = abjad.Note(r"c'4")
        >>> leaf2 = abjad.Note(r"c'4")
        >>> auxjad.inspect([leaf1, leaf2]).leaves_are_tieable()
        True

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.inspect()|. Therefore it can be used from either
        :func:`auxjad.inspect()` or |abjad.inspect()|, as shown below:

        >>> leaf1 = abjad.Note(r"c'4")
        >>> leaf2 = abjad.Note(r"c'4")
        >>> auxjad.inspect([leaf1, leaf2]).leaves_are_tieable()
        True
        >>> abjad.inspect([leaf1, leaf2]).leaves_are_tieable()
        True

    Durations:
        Durations do not affect the comparison.

        >>> leaf1 = abjad.Note(r"c'2.")
        >>> leaf2 = abjad.Note(r"c'16")
        >>> leaf3 = abjad.Note(r"f'''16")
        >>> auxjad.inspect([leaf1, leaf2]).leaves_are_tieable()
        True
        >>> auxjad.inspect([leaf1, leaf3]).leaves_are_tieable()
        False
        >>> auxjad.inspect([leaf2, leaf3]).leaves_are_tieable()
        False

    Chords:
        Handles chords as well as pitches.

        >>> chord1 = abjad.Chord(r"<c' e' g'>4")
        >>> chord2 = abjad.Chord(r"<c' e' g'>16")
        >>> chord3 = abjad.Chord(r"<f''' fs'''>16")
        >>> auxjad.inspect([chord1, chord2]).leaves_are_tieable()
        True
        >>> auxjad.inspect([chord1, chord3]).leaves_are_tieable()
        False
        >>> auxjad.inspect([chord2, chord3]).leaves_are_tieable()
        False

    Parentage:
        Leaves can also be part of |abjad.Container|'s or child classes.

        >>> container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
        >>> auxjad.inspect([container[1], container[2]]).leaves_are_tieable()
        True

    Rests:
        If rests are input, the return value is ``False``.

        >>> container = abjad.Container(r"r4 g'4 r2")
        >>> auxjad.inspect(leaves).leaves_are_tieable()
        False

    Multiple leaves:
        Accepts more than two notes:

        >>> leaf1 = abjad.Note(r"c'4")
        >>> leaf2 = abjad.Note(r"c'4")
        >>> leaf3 = abjad.Note(r"c'2.")
        >>> auxjad.inspect([leaf1, leaf2, leaf3]).leaves_are_tieable()
        True

    Logical ties:
        Accepts leaves as well as |abjad.LogicalTie|'s:

        >>> leaf = abjad.Note(r"c'2.")
        >>> staff = abjad.Staff(r"c'4 ~ c'16")
        >>> logical_tie = abjad.select(staff).logical_tie(0)
        >>> auxjad.inspect([leaf, logical_tie]).leaves_are_tieable()
        True

    Selections:
        Accepts a single |abjad.Selection| as input. It will consider all of
        its leaves.

        >>> staff = abjad.Staff(r"c'2 c'4. c'8")
        >>> auxjad.inspect(staff[:]).leaves_are_tieable()
        True
        >>> staff = abjad.Staff(r"c'2 c'4. d'8")
        >>> auxjad.inspect(staff[:]).leaves_are_tieable()
        False
    """
    if not isinstance(leaves, (abjad.Selection,
                               collections.abc.Iterable,
                               )):
        raise TypeError("argument must be 'abjad.Selection' or non-string "
                        "iterable of components")
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
            leaf1_graces = abjad.inspect(leaf1).before_grace_container()
            leaf2_graces = abjad.inspect(leaf2).before_grace_container()
            if not isinstance(leaf1_graces, type(leaf2_graces)):
                return False
    return True
