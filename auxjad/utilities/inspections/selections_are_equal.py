import collections
from typing import Iterable, Union

import abjad


def selections_are_equal(selections: Union[Iterable[abjad.Component],
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
        >>> auxjad.inspect(selections).selections_are_equal()
        True

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.inspect()|. Therefore it can be used from either
        :func:`auxjad.inspect()` or |abjad.inspect()|, as shown below:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.inspect(selections).selections_are_equal()
        True
        >>> abjad.inspect(selections).selections_are_equal()
        True

    Effective durations:
        Even if all leaves of both selections are identical in relation to both
        pitches and written durations, the function considers the effective
        durations. This means that situations like the one below do not yield a
        false positive:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} "
        ...                          "f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.inspect(selections).selections_are_equal()
        False

    ``include_indicators``:
        By default, this function includes indicators in the comparison, so the
        containers in the example below are understood to be different:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.inspect(selections).selections_are_equal()
        False

        Set the argument ``include_indicators`` to ``False`` to ignore
        indicators when comparison selections. In that case, the containers
        in the example above are then considered identical:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.inspect(selections).selections_are_equal(
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
        >>> auxjad.inspect(selections).selections_are_equal()
        False

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          r"f'4 <g' a'>2 r2")
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.inspect(selections).selections_are_equal()
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          r"f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 "
        ...                          r"f'4 <g' a'>2 r2")
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.inspect(selections).selections_are_equal()
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          r"f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          r"f'4 <g' a'>2 r2")
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.inspect(selections).selections_are_equal()
        True

    .. warning::

        It is important though to create selections using |abjad.select()| as
        shown in the example above instead of using the syntax
        ``container[:]``, since the latter selects only leaves which are not
        grace notes.

    .. note::

        It is important to note it is the contents of the containers which are
        compared, so containers of different classes can still return a
        ``True`` value.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.inspect(selections).selections_are_equal()
        True
    """
    if not isinstance(selections, collections.abc.Iterable):
        raise TypeError("argument must be an iterable of 'abjad.Selection's")
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
                if (abjad.inspect(leaf1).duration()
                        != abjad.inspect(leaf2).duration()):
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
                if (include_indicators and abjad.inspect(leaf1).indicators()
                        != abjad.inspect(leaf2).indicators()):
                    return False
    return True
