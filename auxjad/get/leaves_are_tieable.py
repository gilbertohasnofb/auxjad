from collections.abc import Iterable
from typing import Union

import abjad


def leaves_are_tieable(leaves: Union[abjad.Selection,
                                     Iterable[abjad.Component],
                                     Iterable[abjad.LogicalTie],
                                     ],
                       *,
                       only_identical_pitches: bool = False,
                       ) -> bool:
    r"""Returns a :obj:`bool` representing whether or not two or more input
    leaves have any identical pitch(es) and thus can be tied. Input argument
    can be a single |abjad.Selection| with multiple leaves, or an iterable with
    elements of type |abjad.Leaf| or child classes.

    Basic usage:
        When one or more pitches of a leave is also present in the next one,
        the function returns ``True``:

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
        Handles chords.

        >>> chord1 = abjad.Chord(r"<c' e' g'>4")
        >>> chord2 = abjad.Chord(r"<c' e' g'>16")
        >>> chord3 = abjad.Chord(r"<f''' fs'''>16")
        >>> auxjad.get.leaves_are_tieable([chord1, chord2])
        True
        >>> auxjad.get.leaves_are_tieable([chord1, chord3])
        False
        >>> auxjad.get.leaves_are_tieable([chord2, chord3])
        False

    ``only_identical_pitches``:
        By default, if any pitch in a leaf (be it either a note or chord) can
        be tied to the next leaf, the function returns ``True``:

        >>> chord1 = abjad.Chord(r"<c' e' g'>4")
        >>> chord2 = abjad.Chord(r"<c' e' g' bf'>4")
        >>> note = abjad.Note(r"c'4")
        >>> auxjad.get.leaves_are_tieable([chord1, chord2])
        True
        >>> auxjad.get.leaves_are_tieable([chord2, note])
        True

        Set the argument ``only_identical_pitches`` to ``True`` so that the
        function only returns ``True`` for identical pitch collections:

        >>> chord1 = abjad.Chord(r"<c' e' g'>4")
        >>> chord2 = abjad.Chord(r"<c' e' g' bf'>4")
        >>> note = abjad.Note(r"c'4")
        >>> auxjad.get.leaves_are_tieable([chord1, chord2],
        ...                               only_identical_pitches=True,
        ...                               )
        False
        >>> auxjad.get.leaves_are_tieable([chord2, note],
        ...                               only_identical_pitches=True,
        ...                               )
        False
        >>> chord3 = abjad.Chord(r"<c' e' g' bf'>4")
        >>> chord4 = abjad.Chord(r"<c' e' g' bf'>4")
        >>> auxjad.get.leaves_are_tieable([chord3, chord4],
        ...                               only_identical_pitches=True,
        ...                               )
        True

    Rests:
        If rests are input, the return value is ``False``. It also handles
        multi-measure rests.

        >>> leaf = abjad.Note(r"c'4")
        >>> rest = abjad.Rest(r"r4")
        >>> auxjad.get.leaves_are_tieable([leaf, rest])
        False

    Parentage:
        Leaves can also be part of |abjad.Container|'s or child classes.

        >>> container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
        >>> auxjad.get.leaves_are_tieable([container[1], container[2]])
        True

    Multiple leaves:
        It accepts more than two leaves and will return ``True`` if all leaves
        can be tied sequentially (i.e. leaf one to leaf two, leaf two to leaf
        three, etc.):

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
        Accepts a single |abjad.Selection| as input and will return ``True`` if
        all leaves can be tied sequentially (i.e. leaf one to leaf two, leaf
        two to leaf three, etc.):

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
    if not isinstance(only_identical_pitches, bool):
        raise TypeError("'only_identical_pitches' must be 'bool'")
    if len(leaves) < 2:
        raise ValueError("argument must contain two or more leaves")

    for index, leaf1 in enumerate(leaves[:-1]):
        for leaf2 in leaves[index + 1:]:
            if isinstance(leaf1, abjad.LogicalTie):
                leaf1 = leaf1[0]
            elif isinstance(leaf2, abjad.LogicalTie):
                leaf2 = leaf2[0]
            elif isinstance(leaf1, abjad.Rest):
                return False
            elif isinstance(leaf1, abjad.MultimeasureRest):
                return False
            elif (isinstance(leaf1, (abjad.Note, abjad.Chord))
                    and isinstance(leaf2, (abjad.Note, abjad.Chord))):
                try:
                    pitches_1 = [leaf1.written_pitch]
                except AttributeError:
                    pitches_1 = [p for p in leaf1.written_pitches]
                pitches_1.sort()
                try:
                    pitches_2 = [leaf2.written_pitch]
                except AttributeError:
                    pitches_2 = [p for p in leaf2.written_pitches]
                pitches_2.sort()
                if only_identical_pitches and pitches_1 != pitches_2:
                    return False
                elif not any([p in pitches_2 for p in pitches_1]):
                    return False
            else:
                return False

            # leaf1_graces = abjad.get.before_grace_container(leaf1)
            # leaf2_graces = abjad.get.before_grace_container(leaf2)
            # if not isinstance(leaf1_graces, type(leaf2_graces)):
            #     return False
    return True
