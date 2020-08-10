from typing import Union

import abjad


def leaves_are_tieable(leaf1: Union[abjad.Leaf, abjad.Selection],
                       leaf2: Union[abjad.Leaf, abjad.Selection],
                       ) -> bool:
    r"""Returns a :obj:`bool` representing whether or not two input leaves (of
    type |abjad.Leaf| or child class) have identical pitch(es) and thus can
    be tied.

    Basic usage:
        When the pitches in both leaves are identical, this function returns
        ``True``:

        >>> leaf1 = abjad.Note(r"c'4")
        >>> leaf2 = abjad.Note(r"c'4")
        >>> auxjad.leaves_are_tieable(leaf1, leaf2)
        True

    Durations:
        Durations do not affect the comparison.

        >>> leaf1 = abjad.Note(r"c'2.")
        >>> leaf2 = abjad.Note(r"c'16")
        >>> leaf3 = abjad.Note(r"f'''16")
        >>> auxjad.leaves_are_tieable(leaf1, leaf2)
        Trueselection2
        >>> auxjad.leaves_are_tieable(leaf1, leaf3)
        False
        >>> auxjad.leaves_are_tieable(leaf2, leaf3)
        False

    Chords:
        Handles chords as well as pitches.

        >>> chord1 = abjad.Chord(r"<c' e' g'>4")
        >>> chord2 = abjad.Chord(r"<c' e' g'>16")
        >>> chord3 = abjad.Chord(r"<f''' fs'''>16")
        >>> auxjad.leaves_are_tieable(chord1, chord2)
        True
        >>> auxjad.leaves_are_tieable(chord1, chord3)
        False
        >>> auxjad.leaves_are_tieable(chord2, chord3)
        False

    Parentage:
        Leaves can also be part of containers.

        >>> container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
        >>> auxjad.leaves_are_tieable(container[1], container[2])
        True

    Rests:
        If rests are input, the return value is ``False``.

        >>> container = abjad.Container(r"r4 g'4 r2")
        >>> auxjad.leaves_are_tieable(container[0], container[2])
        False
    """
    if not isinstance(leaf1, (abjad.Leaf, abjad.Selection)):
        raise TypeError("first positional argument must be 'abjad.Selection', "
                        "'abjad.Leaf' or child class")
    if not isinstance(leaf2, (abjad.Leaf, abjad.Selection)):
        raise TypeError("second positional argument must be "
                        "'abjad.Selection', 'abjad.Leaf' or child class")
    if isinstance(leaf1, abjad.Selection):
        leaf1 = leaf1.leaf(-1)
    if isinstance(leaf2, abjad.Selection):
        leaf2 = leaf2.leaf(0)
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
    if not isinstance(abjad.inspect(leaf1).before_grace_container(),
                      type(abjad.inspect(leaf2).before_grace_container())):
        return False
    return True


def _leaves_are_tieable(self,
                        leaf2: abjad.Leaf
                        ):
    return leaves_are_tieable(self._client,
                              leaf2=leaf2,
                              )


abjad.Inspection.leaves_are_tieable = _leaves_are_tieable
