import abjad


def containers_are_equal(container1: abjad.Container,
                         container2: abjad.Container,
                         *,
                         include_indicators: bool = False,
                         ) -> bool:
    r"""Returns a ``bool`` representing whether two input containers (of type
    ``abjad.Container`` or child class) are identical or not.

    ..  container:: example

        When the pitches and effective durations of all leaves in both
        containers are identical, this function returns ``True``:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.containers_are_equal(container1, container2)
        True

    ..  container:: example

        Even if all leaves of both containers are identical in relation to both
        pitches and written durations, the function considers the effective
        durations. This means that situations like the one below do not yield a
        false positive:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.containers_are_equal(container1, container2)
        False

    ..  container:: example

        By default, this function ignores indicators, so the containers in the
        example below are understood to be identical:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.containers_are_equal(container1, container2)
        True

    ..  container:: example

        Setting the argument ``include_indicators`` to ``True`` forces the
        function to include indicators in its comparison. In that case, the
        containers in the example above are not considered identical any
        longer:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.containers_are_equal(container1,
        ...                             container2,
        ...                             include_indicators=True,
        ...                             )
        True

    ..  container:: example

        This function also handles grace notes:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 \grace{d'4} d'4 e'4 f'4")
        >>> auxjad.containers_are_equal(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.containers_are_equal(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.containers_are_equal(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.containers_are_equal(container1, container2)
        True
    """
    if not isinstance(container1, abjad.Container):
        raise TypeError("first positional argument must be 'abjad.Container' "
                        "or child class")
    if not isinstance(container2, abjad.Container):
        raise TypeError("second positional argument must be 'abjad.Container' "
                        "or child class")
    if not isinstance(include_indicators, bool):
        raise TypeError("'include_indicators' must be 'bool'")

    leaves1 = [leaf for leaf in abjad.select(container1).leaves()]
    leaves2 = [leaf for leaf in abjad.select(container2).leaves()]

    if len(leaves1) != len(leaves2):
        return False

    for leaf1, leaf2 in zip(leaves1, leaves2):
        if type(leaf1) is not type(leaf2):
            return False
        if abjad.inspect(leaf1).duration() != abjad.inspect(leaf2).duration():
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
        if (include_indicators and abjad.inspect(leaf1).indicators() != 
                abjad.inspect(leaf2).indicators()):
            return False
    return True
