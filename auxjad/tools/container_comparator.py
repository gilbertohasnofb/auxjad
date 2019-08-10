import abjad
import itertools


def container_comparator(container1,
                         container2,
                         include_indicators: bool = False,
                         include_grace_notes: bool = False,
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
        >>> container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} f'4 <g' a'>2 r2")
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

        By default, this function ignores grace notes, so the containers in the
        example below are understood to be identical:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1, container2)
        True

    ..  container:: example

        Setting the argument ``include_grace_notes`` to ``True`` forces the
        function to include grace notes in its comparison. In that case, the
        containers in the example above are not considered identical any
        longer:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1,
        ...                             container2,
        ...                             include_grace_notes=True,
        ...                             )
        False

    ..  container:: example

        When the argument ``include_grace_notes`` is set to ``True``, the
        function will consider not only a grace note is attached to a given
        leaf, but also wether the contents of the grace containers are the
        identical:

        >>> container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.container_comparator(container1,
        ...                             container2,
        ...                             include_grace_notes=True,
        ...                             )
        False

    """
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
        if include_indicators:
            if abjad.inspect(leaf1).indicators() != \
                    abjad.inspect(leaf2).indicators():
                return False
        if include_grace_notes:
            grace_container1 = abjad.inspect(leaf1).grace_container()
            grace_container2 = abjad.inspect(leaf2).grace_container()
            if grace_container1 and grace_container2:
                ungraced_container1 = abjad.Container()
                ungraced_container2 = abjad.Container()
                for component in grace_container1.components:
                    ungraced_container1.append(component)
                for component in grace_container2.components:
                    ungraced_container2.append(component)
                if not container_comparator(ungraced_container1,
                                            ungraced_container2,
                                            ):
                    return False
            elif grace_container1 != grace_container2:
                return False
    return True
