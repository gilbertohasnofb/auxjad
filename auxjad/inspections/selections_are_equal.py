import collections
from typing import Iterable, Union

import abjad


def selections_are_equal(selections: Union[Iterable[abjad.Component],
                                           Iterable[abjad.Selection],
                                           ],
                         *,
                         include_indicators: bool = False,
                         ) -> bool:
    r"""Returns a :obj:`bool` representing whether two input containers (of
    type |abjad.Container| or child class) are identical or not.

    Basic usage:
        When the pitches and effective durations of all leaves in both
        containers are identical, this function returns ``True``:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.selections_are_equal(container1, container2)
        True

    Effective durations:
        Even if all leaves of both containers are identical in relation to both
        pitches and written durations, the function considers the effective
        durations. This means that situations like the one below do not yield a
        false positive:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.selections_are_equal(container1, container2)
        False

    ``include_indicators``:
        By default, this function ignores indicators, so the containers in the
        example below are understood to be identical:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.selections_are_equal(container1, container2)
        True

        Setting the argument ``include_indicators`` to ``True`` forces the
        function to include indicators in its comparison. In that case, the
        containers in the example above are not considered identical any
        longer:

        >>> container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> auxjad.selections_are_equal(container1,
        ...                             container2,
        ...                             include_indicators=True,
        ...                             )
        False

    Grace notes:
        This function also handles grace notes:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 \grace{d'4} d'4 e'4 f'4")
        >>> auxjad.selections_are_equal(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.selections_are_equal(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.selections_are_equal(container1, container2)
        False

        >>> container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 "
        ...                          "f'4 <g' a'>2 r2")
        >>> auxjad.selections_are_equal(container1, container2)
        True

    ..  note::

        It is important to note it is the contents of the containers which are
        compared, so containers of different classes can still return a
        ``True`` value.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.selections_are_equal(container1, container2)
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


def _selections_are_equal(self,
                          *,
                          include_indicators: bool = False,
                          ):
    return selections_are_equal(self._client,
                                include_indicators=include_indicators,
                                )


abjad.Inspection.selections_are_equal = _selections_are_equal
