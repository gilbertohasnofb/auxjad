import abjad


def container_comparator(container1: abjad.Container,
                         container2: abjad.Container,
                         *,
                         include_indicators: bool = False,
                         ) -> bool:
    r"""A comparator function returning True when two containers are identical
    and False when they are not.

    ..  container:: example

        When the pitches and effective durations of all leaves in both
        containers are identical, this function returns ``True``:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1, container2)
        True

    ..  container:: example

        Even if all leaves of both containers are identical in pitches and in
        written_duration, the function considers the effective duration so that
        situations like the one below do not yield a false positive:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1, container2)
        False

    ..  container:: example

        By default, this function ignores indicators, so the containers in the
        example below are understood to be identical:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1, container2)
        True

    ..  container:: example

        Setting the argument ``include_indicators`` to ``True`` forces the
        function to include indicators in its comparison. In that case, the
        containers in the example above are not considered identical any
        longer:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1,
        ...                             container2,
        ...                             include_indicators=True,
        ...                             )
        True

    ..  container:: example

        This function also handles grace notes:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 \grace{d'4} d'4 e'4 f'4")
        >>> auxjad.container_comparator(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1, container2)
        True

    """
    if not isinstance(container1, abjad.Container):
        raise TypeError("'container1' must be 'abjad.Container' or "
                        "child class")
    if not isinstance(container2, abjad.Container):
        raise TypeError("'container2' must be 'abjad.Container' or "
                        "child class")
    if not isinstance(include_indicators, bool):
        raise TypeError("'include_indicators' must be 'bool'")

    leaves1 = [leaf for leaf in abjad.select(container1).leaves()]
    leaves2 = [leaf for leaf in abjad.select(container2).leaves()]

    if len(leaves1) != len(leaves2):
        return False

    for leaf1, leaf2 in zip(leaves1, leaves2):
        if type(leaf1) != type(leaf2):
            return False
        if abjad.inspect(leaf1).duration() != abjad.inspect(leaf2).duration():
            return False
        if type(leaf1) == abjad.Note:
            if leaf1.written_pitch != leaf2.written_pitch:
                return False
        if type(leaf1) == abjad.Chord:
            if leaf1.written_pitches != leaf2.written_pitches:
                return False
        if type(abjad.inspect(leaf1).before_grace_container()) != \
                type(abjad.inspect(leaf2).before_grace_container()):
            return False
        if include_indicators:
            if abjad.inspect(leaf1).indicators() != \
                    abjad.inspect(leaf2).indicators():
                return False
    return True
