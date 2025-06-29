from collections.abc import Iterable
from typing import Union

import abjad


def selections_are_identical(selections: Union[Iterable[abjad.Component],
                                               Iterable[abjad.Selection],
                                               ],
                             *,
                             include_indicators: bool = True,
                             ) -> bool:
    r"""Returns a :obj:`bool` representing whether two or more selections are
    identical or not. Input argument must be an iterable made of two or more
    |abjad.Selection|'s.

    Basic usage:
        When the pitches and effective durations of all leaves in all
        selections are identical, this function returns ``True``:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.selections_are_identical(selections)
        True

        This function can handle multiple selections, and will compare them
        among each other returning ``True`` if all are identical:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container3 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container4 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [
        ...     container1[:],
        ...     container2[:],
        ...     container3[:],
        ...     container4[:],
        ... ]
        >>> auxjad.get.selections_are_identical(selections)
        True

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.get|. It can thus be used from either |auxjad.get|_ or
        |abjad.get| namespaces. Therefore, the two lines below are equivalent:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.selections_are_identical(selections)
        True
        >>> abjad.get.selections_are_identical(selections)
        True

    Effective durations:
        Even if all leaves of both selections are identical in relation to both
        pitches and written durations, the function considers the effective
        durations. This means that situations like the one below do not yield a
        false positive:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(
        ...     r"\times 3/2 {c'4 d'4 e'4} f'4 <g' a'>2 r2"
        ... )
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.selections_are_identical(selections)
        False

    ``include_indicators``:
        By default, this function includes indicators in the comparison, so the
        containers in the example below are understood to be different:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.selections_are_identical(selections)
        False

        Set the argument ``include_indicators`` to ``False`` to ignore
        indicators when comparison selections. In that case, the containers in
        the example above are then considered identical:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.selections_are_identical(
        ...     selections,
        ...     include_indicators=False,
        ... )
        True

    Grace notes:
        This function also handles grace notes.

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 \grace{d'4} d'4 e'4 f'4")
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.get.selections_are_identical(selections)
        False

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(
        ...     r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.get.selections_are_identical(selections)
        False

        >>> container1 = abjad.Staff(
        ...     r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> container2 = abjad.Staff(
        ...     r"c'4 \grace{c''8} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.get.selections_are_identical(selections)
        False

        >>> container1 = abjad.Staff(
        ...     r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> container2 = abjad.Staff(
        ...     r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.get.selections_are_identical(selections)
        True

    ..  warning::

        It is important to create selections using |abjad.select()| as shown in
        the example above, instead of using the syntax ``container[:]``, since
        the latter ignores grace notes.

    ..  note::

        It is important to note it is the contents of the containers which are
        compared, so containers of different classes can still return a
        ``True`` value.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.selections_are_identical(selections)
        True
    """
    if not isinstance(selections, Iterable):
        raise TypeError("argument must be an iterable of 'abjad.Selection's "
                        "or 'abjad.Component's")
    for selection in selections:
        if not isinstance(selection, (abjad.Component, abjad.Selection)):
            raise TypeError("argument must be an iterable of "
                            "'abjad.Selection's or 'abjad.Component's")
    if not isinstance(include_indicators, bool):
        raise TypeError("'include_indicators' must be 'bool'")

    for index, selection1 in enumerate(selections[:-1]):
        for selection2 in selections[index + 1:]:
            leaves1 = [leaf for leaf in selection1.leaves()]
            leaves2 = [leaf for leaf in selection2.leaves()]
            if len(leaves1) != len(leaves2):
                return False
            for leaf1, leaf2 in zip(leaves1, leaves2):
                if not isinstance(leaf1, type(leaf2)):
                    return False
                if abjad.get.duration(leaf1) != abjad.get.duration(leaf2):
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
                if include_indicators:
                    indicators1 = [format(indicator) for indicator
                                   in abjad.get.indicators(leaf1)]
                    indicators2 = [format(indicator) for indicator
                                   in abjad.get.indicators(leaf2)]
                    if not all(indicator1 in indicators2
                               for indicator1 in indicators1):
                        return False
                    if not all(indicator2 in indicators1
                               for indicator2 in indicators2):
                        return False
    return True
