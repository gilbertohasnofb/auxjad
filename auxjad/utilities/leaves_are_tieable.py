import abjad


def leaves_are_tieable(leaf1: abjad.Leaf,
                       leaf2: abjad.Leaf,
                       ) -> bool:
    r"""Returns a ``bool`` representing whether or not two input leaves (of
    type ``abjad.Leaf`` or child class) have identical pitch(es) and thus can
    be tied.

    ..  container:: example

        When the pitches in both leaves are identical, this function returns
        ``True``:

        >>> Leaf1 = abjad.Note(r"c'4")
        >>> Leaf2 = abjad.Note(r"c'4")
        >>> auxjad.leaves_are_tieable(Leaf1, Leaf2)
        True

    ..  container:: example

        Durations do not affect the comparison.

        >>> Leaf1 = abjad.Note(r"c'2.")
        >>> Leaf2 = abjad.Note(r"c'16")
        >>> Leaf3 = abjad.Note(r"f'''16")
        >>> auxjad.leaves_are_tieable(Leaf1, Leaf2)
        True
        >>> auxjad.leaves_are_tieable(Leaf1, Leaf3)
        False
        >>> auxjad.leaves_are_tieable(Leaf2, Leaf3)
        False

    ..  container:: example

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

    ..  container:: example

        Leaves can also be part of containers.

        >>> container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
        >>> auxjad.leaves_are_tieable(container[1], container[2])
        True

    ..  container:: example

        If rests are input, the return value is ``False``.

        >>> container = abjad.Container(r"r4 g'4 r2")
        >>> auxjad.leaves_are_tieable(container[0], container[2])
        False
    """
    if not isinstance(leaf1, abjad.Leaf):
        raise TypeError("first positional argument must be 'abjad.Leaf' or "
                        "child class")
    if not isinstance(leaf2, abjad.Leaf):
        raise TypeError("second positional argument must be 'abjad.Leaf' or "
                        "child class")
    if type(leaf1) is not type(leaf2):
        return False
    if isinstance(leaf1, abjad.Rest):
        return False
    if isinstance(leaf1, abjad.MultimeasureRest):
        return False
    if (isinstance(leaf1, abjad.Note) and 
            leaf1.written_pitch != leaf2.written_pitch):
        return False
    if (isinstance(leaf1, abjad.Chord) and 
            leaf1.written_pitches != leaf2.written_pitches):
        return False
    if (type(abjad.inspect(leaf1).before_grace_container()) is not 
            type(abjad.inspect(leaf2).before_grace_container())):
        return False
    return True
