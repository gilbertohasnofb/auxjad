import abjad

from .. import get, mutate


def _groupped_logical_ties(container) -> list:
    r'Selects logical ties with all consecutive rests.'
    groupped_logical_ties = []
    selection = abjad.Selection()
    for logical_tie in abjad.select(container).logical_ties():
        if not isinstance(logical_tie.head, (abjad.Rest,
                                             abjad.MultimeasureRest,
                                             )):
            if len(selection) > 0:
                groupped_logical_ties.append(selection)
            selection = abjad.Selection(logical_tie)
        else:
            selection += abjad.Selection(logical_tie)
    if len(selection) > 0:
        groupped_logical_ties.append(selection)
    return groupped_logical_ties


def extend_notes(container: abjad.Container,
                 max_note_duration: abjad.Duration,
                 *,
                 gap: abjad.Duration = abjad.Duration((0, 1)),
                 gap_before_end: bool = False,
                 use_multimeasure_rests: bool = True,
                 rewrite_meter: bool = True,
                 ) -> None:
    r"""Mutates an input |abjad.Container| (or child class) in place and has no
    return value; this function extends all logical ties (notes and chords) up
    to a given maximum note duration.

    Basic usage:
        This function will extend the duration of each logical tie up until the
        allowed maximum duration.

        >>> staff = abjad.Staff(r"c'16 r2... d'8 r2.. e'8. r16 r2. f'4 r2.")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r2...
                d'8
                r2..
                e'8.
                r16
                r2.
                f'4
                r2.
            }

        ..  figure:: ../_images/extend_notes-gJGtjtm3fu.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                r2.
                d'4
                r2.
                e'4
                r2.
                f'4
                r2.
            }

        ..  figure:: ../_images/extend_notes-6pjHLREOap.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.extend_notes(staff)
        >>> abjad.mutate.extend_notes(staff)

    Longer notes:
        This function will not alter the length of logical ties that are
        already equal to or larger than the maximum extension duration.

        >>> staff = abjad.Staff(r"c'16 r2... d'2 r2 e'2. r4 f'1")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r2...
                d'2
                r2
                e'2.
                r4
                f'1
            }

        ..  figure:: ../_images/extend_notes-56rOAsxHPP.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                r2.
                d'2
                r2
                e'2.
                r4
                f'1
            }

        ..  figure:: ../_images/extend_notes-egF496w5Bs.png

    Chords:
        This function works with chords:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'8 r8 r2 r4 <d' e' f'>4 r4 r8 g'16 r16 r2"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'8
                r8
                r2
                r4
                <d' e' f'>4
                r4
                r8
                g'16
                r16
                r2
            }

        ..  figure:: ../_images/extend_notes-2151PE127t.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((2, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2
                r4
                r4
                <d' e' f'>2
                r8
                g'8
                ~
                g'4.
                r8
            }

        ..  figure:: ../_images/extend_notes-GVM7SBRQ5z.png

    Second positional argument:
        The second positional argument must be an |abjad.Duration| or objects
        that can instantiate an |abjad.Duration|, such as :obj:`str`,
        :obj:`tuple`, :obj:`int`, and :obj:`float`. The notes will be extended
        up to that duration, or until the next note if the full duration is not
        possible:

        >>> staff = abjad.Staff(
        ...     r"c'16 r4.. d'16 r4.. e'16 r2... f'16 r4.. g'16 r4.."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r4..
                d'16
                r4..
                e'16
                r2...
                f'16
                r4..
                g'16
                r4..
            }

        ..  figure:: ../_images/extend_notes-GfrvgpqH2J.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2
                d'2
                e'2.
                r4
                f'2
                g'2
            }

        ..  figure:: ../_images/extend_notes-1vKtKyK7up.png

    Dynamics:
        Dynamics are preserved:

        >>> staff = abjad.Staff(
        ...     r"c'16\ppp r2... d'16\ff r2... e'16\f r2... f'16\mp r2..."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                \ppp
                r2...
                d'16
                \ff
                r2...
                e'16
                \f
                r2...
                f'16
                \mp
                r2...
            }

        ..  figure:: ../_images/extend_notes-rAHtip59b2.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2.
                \ppp
                r4
                d'2.
                \ff
                r4
                e'2.
                \f
                r4
                f'2.
                \mp
                r4
            }

        ..  figure:: ../_images/extend_notes-TNbei46PhS.png

    Time signatures changes:
        This function handles time signature changes:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'16 r8. r2 "
        ...     r"\time 2/4 d'8 r8 e'8 r8 "
        ...     r"\time 3/4 r2 f'16 r8."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'16
                r8.
                r2
                \time 2/4
                d'8
                r8
                e'8
                r8
                \time 3/4
                r2
                f'16
                r8.
            }

        ..  figure:: ../_images/extend_notes-k8d4mKMaS7.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2.
                \time 2/4
                d'4
                e'4
                ~
                \time 3/4
                e'2
                f'4
            }

        ..  figure:: ../_images/extend_notes-5eDO8ehSld.png

    ``gap``:
        Use the argument ``gap`` to ensure that there a minimum gap is left
        between leaves when extending them:

        >>> staff = abjad.Staff(r"c'4 r4 d'4 r4 e'4 r2.")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                r4
                d'4
                r4
                e'4
                r2.
            }

        ..  figure:: ../_images/extend_notes-zpAx8NYXof.png

        >>> auxjad.mutate.extend_notes(staff,
        ...                            abjad.Duration((2, 4)),
        ...                            gap=abjad.Duration((1, 16)),
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4..
                r16
                d'4..
                r16
                e'2
                r2
            }

        ..  figure:: ../_images/extend_notes-t1HIPtyJkn.png

        Note that this function will not shorten leaves, so previous leaves
        that had no gaps will still have no gaps between them. ``gap`` will
        only affect leaves that are extended by the function.

        >>> staff = abjad.Staff(r"c'2 d'4 r4 e'4 r4 f'2 ~ f'2 r2")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2
                d'4
                r4
                e'4
                r4
                f'2
                ~
                f'2
                r2
            }

        ..  figure:: ../_images/extend_notes-ZfrusN3f8T.png

        >>> auxjad.mutate.extend_notes(staff,
        ...                            abjad.Duration((2, 4)),
        ...                            gap=abjad.Duration((1, 16)),
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2
                d'4..
                r16
                e'4..
                r16
                f'2
                ~
                f'2
                r2
            }

        ..  figure:: ../_images/extend_notes-5iteVkhz3l.png

    ``gap_before_end``:
        By default, a when ``gap`` is present it is not applied to the last
        pitched at the end of the container.

        >>> staff = abjad.Staff(r"c'16 r8. d'16 r8. e'16 r8. f'16 r8.")
        >>> auxjad.mutate.extend_notes(staff,
        ...                            abjad.Duration((1, 4)),
        ...                            gap=abjad.Duration((1, 16)),
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'8.
                r16
                d'8.
                r16
                e'8.
                r16
                f'4
            }

        ..  figure:: ../_images/extend_notes-LuCN8pgjLH.png

        Set ``gap_before_end`` to ``True`` to ensure that there is also a
        minimum gap at the end of the container.

        >>> staff = abjad.Staff(r"c'16 r8. d'16 r8. e'16 r8. f'16 r8.")
        >>> auxjad.mutate.extend_notes(staff,
        ...                            abjad.Duration((1, 4)),
        ...                            gap=abjad.Duration((1, 16)),
        ...                            gap_before_end=True,
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'8.
                r16
                d'8.
                r16
                e'8.
                r16
                f'8.
                r16
            }

        ..  figure:: ../_images/extend_notes-LppuegmkEP.png

    ``use_multimeasure_rests``:
        By default, this function uses multi-measure rests

        >>> staff = abjad.Staff(r"\time 3/4 r8 c'8 r4 c'4 r2. r8 c'8 r2 r2.")
        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((2, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                r8
                c'4.
                c'4
                ~
                c'4
                r2
                r8
                c'8
                ~
                c'4.
                r8
                R1 * 3/4
            }

        ..  figure:: ../_images/extend_notes-WaLYhL24UG.png


        Set the keyword argument ``use_multimeasure_rests`` to ``False`` to
        disable this behaviour.

        >>> staff = abjad.Staff(r"\time 3/4 r8 c'8 r4 c'4 r2. r8 c'8 r2 r2.")
        >>> auxjad.mutate.extend_notes(staff,
        ...                            abjad.Duration((2, 4)),
        ...                            use_multimeasure_rests=False,
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                r8
                c'4.
                c'4
                ~
                c'4
                r2
                r8
                c'8
                ~
                c'4.
                r8
                r2.
            }

        ..  figure:: ../_images/extend_notes-H1uDCqQ8iz.png

    ``rewrite_meter``
        By default, this function applies |auxjad.mutate.auto_rewrite_meter()|
        at the end of its process.

        >>> staff = abjad.Staff(r"c'16 r4.. d'16 r4..")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r4..
                d'16
                r4..
            }

        ..  figure:: ../_images/extend_notes-BcAYS4SvUL.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                r4
                d'4
                r4
            }

        ..  figure:: ../_images/extend_notes-QNEks8lUXB.png

        Set ``rewrite_meter`` to ``False`` to disable this. The main reason for
        doing this is performance: when multiple mutations are being applied,
        it is faster to rewrite the meter just once at the end.

        >>> staff = abjad.Staff(r"c'16 r4.. d'16 r4..")
        >>> auxjad.mutate.extend_notes(staff,
        ...                            abjad.Duration((1, 4)),
        ...                            rewrite_meter=False,
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                ~
                c'8.
                r4
                d'16
                ~
                d'8.
                r4
            }

        ..  figure:: ../_images/extend_notes-49jhNoSa9T.png

    ..  warning::

        This function does not support tuplets. Using a container with one or
        more tuplets will result in a :exc:`ValueError` exception being raised:

        >>> staff = abjad.Staff(r"c'4 r4 \times 2/3 {r4 d'4 r4} e'4 r2.")
        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        ValueError: first positional argument contains one ore more tuplets,
        which are not currently supported
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first positional argument must be 'abjad.Container' "
                        "or child class")
    if len(abjad.select(container).tuplets()) > 0:
        raise ValueError("first positional argument contains one ore more "
                         "tuplets, which are not currently supported")
    if not isinstance(max_note_duration,
                      (abjad.Duration, str, tuple, int, float),
                      ):
        raise TypeError("second positional argument must be 'abjad.Duration', "
                        "'str', 'tuple', or a number")
    if not isinstance(max_note_duration, abjad.Duration):
        max_note_duration = abjad.Duration(max_note_duration)
    if gap is not None:
        if not isinstance(gap, (abjad.Duration, str, tuple, int, float)):
            raise TypeError("'gap' must be 'abjad.Duration', 'str', 'tuple', "
                            "or a number")
        if not isinstance(gap, abjad.Duration):
            gap = abjad.Duration(gap)
    if not isinstance(gap_before_end, bool):
        raise TypeError("'gap_before_end' must be 'bool'")
    if not isinstance(use_multimeasure_rests, bool):
        raise TypeError("'use_multimeasure_rests' must be 'bool'")
    if not isinstance(rewrite_meter, bool):
        raise TypeError("'rewrite_meter' must be 'bool'")

    time_signatures = get.time_signature_list(container,
                                              implicit_common_time=False,
                                              )
    groups = _groupped_logical_ties(container)
    for group_index, group in enumerate(groups):
        if not gap_before_end and group_index == len(groups) - 1:
            gap = abjad.Duration((0, 1))
        if isinstance(group[0], (abjad.Rest, abjad.MultimeasureRest)):
            continue
        pitched_duration = 0
        rest_duration = 0
        for item in group:
            if isinstance(item, (abjad.Note, abjad.Chord)):
                pitched_duration += abjad.get.duration(item)
            else:
                rest_duration += abjad.get.duration(item)
        missing_duration = max_note_duration - pitched_duration
        available_duration = rest_duration - gap
        if missing_duration <= 0 or available_duration <= 0:
            continue
        else:
            extended_duration = min(missing_duration, available_duration)
            new_rest_duration = rest_duration - extended_duration

        for index, item in enumerate(group):
            if isinstance(item, (abjad.Rest, abjad.MultimeasureRest)):
                first_rest_index = index
                break
        if isinstance(group[first_rest_index - 1], abjad.Note):
            pitches = group[first_rest_index - 1].written_pitch
        elif isinstance(group[first_rest_index - 1], abjad.Chord):
            pitches = [pitch for pitch
                       in group[first_rest_index - 1].written_pitches]
        if new_rest_duration > abjad.Duration((0, 1)):
            replacement_items = abjad.LeafMaker()(
                [pitches, None],
                [extended_duration, new_rest_duration],
            )
        else:
            replacement_items = abjad.LeafMaker()([pitches],
                                                  [extended_duration],
                                                  )
        abjad.mutate.replace(group[first_rest_index:], replacement_items)
        abjad.attach(abjad.Tie(), group[first_rest_index - 1])
    mutate.enforce_time_signature(container,
                                  time_signatures,
                                  disable_rewrite_meter=True,
                                  )
    if rewrite_meter:
        mutate.auto_rewrite_meter(container)
    if use_multimeasure_rests:
        mutate.rests_to_multimeasure_rest(container[:])
