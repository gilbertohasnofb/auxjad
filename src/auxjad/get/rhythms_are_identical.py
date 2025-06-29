from collections.abc import Iterable
from typing import Union

import abjad

from .. import select


def rhythms_are_identical(selections: Union[Iterable[abjad.Component],
                                            Iterable[abjad.Selection],
                                            ],
                          ) -> bool:
    r"""Returns a :obj:`bool` representing whether two or more selections are
    rhytmically identical or not. Input argument must be an iterable made of
    two or more |abjad.Selection|'s.

    Basic usage:
        When the pitches and effective durations of all leaves in all
        selections are identical, this function returns ``True``:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c''4 b'4 a'4 g'4")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.rhythms_are_identical(selections)
        True

        Rests and chords are also handled.

        >>> container1 = abjad.Staff(r"c'4. d'8 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c''4. r8 <b' a'>4 r4 g'2 f'2")

        When comparing rests, this function considers consecutive rests as a
        single logical tie.

        >>> container1 = abjad.Staff(
        ...     r"c'4 ~ c'16 r8. r8. <d' e'>16 ~ <d' e'>4"
        ... )
        >>> container2 = abjad.Staff(r"r4 r16 c''8. ~ c''8. b'16 ~ b'4")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.rhythms_are_identical(selections)
        True
        >>> container1 = abjad.Staff(
        ...     r"c'4 ~ c'16 r8. r8. <d' e'>16 ~ <d' e'>4"
        ... )
        >>> container2 = abjad.Staff(r"r4 r16 c''8. b'8. a'16 ~ a'4")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.rhythms_are_identical(selections)
        False

        This function can handle multiple selections, and will compare them
        among each other returning ``True`` if all are identical:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(r"c''4 r4 <b' a'>4 r4 g'2 f'2")
        >>> container3 = abjad.Staff(r"c'''4 c'''4 b''4 b''4 a''2 a''2")
        >>> container4 = abjad.Staff(r"c4 d4 e4 f4 g2 a2")
        >>> selections = [
        ...     container1[:],
        ...     container2[:],
        ...     container3[:],
        ...     container4[:],
        ... ]
        >>> auxjad.get.rhythms_are_identical(selections)
        True

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.get|. It can thus be used from either |auxjad.get|_ or
        |abjad.get| namespaces. Therefore, the two lines below are equivalent:

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c''4 b'4 a'4 g'4")
        >>> selections = [container1[:], container2[:]]
        >>> auxjad.get.rhythms_are_identical(selections)
        True
        >>> abjad.get.rhythms_are_identical(selections)
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
        >>> auxjad.get.rhythms_are_identical(selections)
        False

    Grace notes:
        This function also handles grace notes.

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 \grace{d'4} d'4 e'4 f'4")
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.get.rhythms_are_identical(selections)
        False

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
        >>> container2 = abjad.Staff(
        ...     r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.get.rhythms_are_identical(selections)
        False

        >>> container1 = abjad.Staff(
        ...     r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> container2 = abjad.Staff(
        ...     r"c'4 \grace{b4} d'4 e'4 f'4 <g' a'>2 r2"
        ... )
        >>> selection1 = abjad.select(container1)
        >>> selection2 = abjad.select(container2)
        >>> selections = [selection1, selection2]
        >>> auxjad.get.rhythms_are_identical(selections)
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
        >>> auxjad.get.rhythms_are_identical(selections)
        True
    """
    if not isinstance(selections, Iterable):
        raise TypeError("argument must be an iterable of 'abjad.Selection's "
                        "or 'abjad.Component's")
    for selection in selections:
        if not isinstance(selection, (abjad.Component, abjad.Selection)):
            raise TypeError("argument must be an iterable of "
                            "'abjad.Selection's or 'abjad.Component's")

    for index, selection1 in enumerate(selections[:-1]):
        for selection2 in selections[index + 1:]:
            logical_selections1 = [logical_selection for logical_selection
                                   in select.logical_selections(selection1)]
            logical_selections2 = [logical_selection for logical_selection
                                   in select.logical_selections(selection2)]
            if len(logical_selections1) != len(logical_selections2):
                return False
            for logical_sel1, logical_sel2 in zip(logical_selections1,
                                                  logical_selections2,
                                                  ):
                if (abjad.get.duration(logical_sel1)
                        != abjad.get.duration(logical_sel2)):
                    return False
                leaf1 = logical_sel1.leaf(0)
                leaf2 = logical_sel2.leaf(0)
                leaf1_graces = abjad.get.before_grace_container(leaf1)
                leaf2_graces = abjad.get.before_grace_container(leaf2)
                if not isinstance(leaf1_graces, type(leaf2_graces)):
                    return False
    return True
