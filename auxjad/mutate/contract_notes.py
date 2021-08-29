import abjad

from .. import get, mutate


def contract_notes(container: abjad.Container,
                   max_contraction_duration: abjad.Duration,
                   *,
                   minimum_duration: abjad.Duration = abjad.Duration((0, 1)),
                   use_multimeasure_rests: bool = True,
                   rewrite_meter: bool = True,
                   ) -> None:
    r"""Mutates an input |abjad.Container| (or child class) in place and has no
    return value; this function contracts all logical ties (notes and chords)
    by a maximum contraction duration.

    Basic usage:
        This function will contract the duration of each logical tie up by the
        allowed maximum contraction duration.

        >>> staff = abjad.Staff(r"c'4 r2. d'2 r2 e'2. r4 f'1")
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


        ..  figure:: ../_images/contract_notes-DtvjEcpLMF.png

        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'8
                r2..
                d'4.
                r8
                r2
                e'2
                ~
                e'8
                r4.
                f'2..
                r8
            }

        ..  figure:: ../_images/contract_notes-PEgTVggwUR.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.contract_notes(staff)
        >>> abjad.mutate.contract_notes(staff)

    Chords:
        This function works with chords:

        >>> staff = abjad.Staff(r"\time 3/4 c'2. <d' e' f'>2 r4 g'4 r2")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2.
                <d' e' f'>2
                r4
                g'4
                r2
            }

        ..  figure:: ../_images/contract_notes-MtQM9vn5rV.png

        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((1, 16)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2
                ~
                c'8.
                r16
                <d' e' f'>4..
                r16
                r4
                g'8.
                r16
                r2
            }

        ..  figure:: ../_images/contract_notes-3KViO6UZ74.png

    Second positional argument:
        The second positional argument must be an |abjad.Duration| or objects
        that can instantiate an |abjad.Duration|, such as :obj:`str`,
        :obj:`tuple`, :obj:`int`, and :obj:`float`. The notes will be contract
        by up to that duration, or until the note is removed:

        >>> staff = abjad.Staff(
        ...     r"c'4 r2. d'2 r2 e'2. r4 f'1"
        ... )
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

        ..  figure:: ../_images/contract_notes-OgFmg6p3VP.png

        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((1, 2)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                R1
                R1
                e'4
                r2.
                f'2
                r2
            }

        ..  figure:: ../_images/contract_notes-YfZ3maHywo.png

    Dynamics:
        Dynamics are preserved:

        >>> staff = abjad.Staff(r"c'4\ppp r2. d'2\ff r2 e'2.\f r4 f'1\mp")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \ppp
                r2.
                d'2
                \ff
                r2
                e'2.
                \f
                r4
                f'1
                \mp
            }

        ..  figure:: ../_images/contract_notes-zKIFJdZuSX.png

        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'8
                \ppp
                r2..
                d'4.
                \ff
                r8
                r2
                e'2
                \f
                ~
                e'8
                r4.
                f'2..
                \mp
                r8
            }

        ..  figure:: ../_images/contract_notes-iKVB9DmxJf.png

    Time signatures changes:
        This function handles time signature changes:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'4 r2 "
        ...     r"\time 2/4 d'2 "
        ...     r"\time 3/4 e'2. "
        ...     r"\time 4/4 f'1"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'4
                r2
                \time 2/4
                d'2
                \time 3/4
                e'2.
                \time 4/4
                f'1
            }

        ..  figure:: ../_images/contract_notes-cpRcyhRgB7.png

        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((3, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'8
                r8
                r2
                \time 2/4
                d'4.
                r8
                \time 3/4
                e'2
                ~
                e'8
                r8
                \time 4/4
                f'2..
                r8
            }

        ..  figure:: ../_images/contract_notes-R6hnRYZU68.png

    ``minimum_duration``:
        Use the argument ``minimum_duration`` to ensure that notes will not be
        contracted further than this value:

        >>> staff = abjad.Staff(r"c'4 r2. d'2 r2 e'2. r4 f'1")
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

        ..  figure:: ../_images/contract_notes-lzHgoaJ2Es.png

        >>> auxjad.mutate.contract_notes(staff,
        ...                            abjad.Duration((1, 2)),
        ...                            minimum_duration=abjad.Duration((1, 8)),
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'8
                r2..
                d'8
                r2..
                e'4
                r2.
                f'2
                r2
            }

        ..  figure:: ../_images/contract_notes-o5lELCkJm8.png

    ``use_multimeasure_rests``:
        By default, this function uses multi-measure rests

        >>> staff = abjad.Staff(
        ...     r"\time 4/4 c'4 r2. \time 3/4 d'4 r2 \time 4/4 e'4 r2."
        ... )
        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((1, 2)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                R1
                \time 3/4
                R1 * 3/4
                \time 4/4
                R1
            }

        ..  figure:: ../_images/contract_notes-olfdBpIydF.png


        Set the keyword argument ``use_multimeasure_rests`` to ``False`` to
        disable this behaviour.

        >>> staff = abjad.Staff(
        ...     r"\time 4/4 c'4 r2. \time 3/4 d'4 r2 \time 4/4 e'4 r2."
        ... )
        >>> auxjad.mutate.contract_notes(staff,
        ...                              abjad.Duration((1, 2)),
        ...                              use_multimeasure_rests=False,
        ...                              )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                r1
                \time 3/4
                r2.
                \time 4/4
                r1
            }

        ..  figure:: ../_images/contract_notes-VNPRYNnFl5.png

    ``rewrite_meter``
        By default, this function applies |auxjad.mutate.auto_rewrite_meter()|
        at the end of its process.

        >>> staff = abjad.Staff(r"\time 3/4 r8 c'8 ~ c'2 r8 d'8 ~ d'2")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                r8
                c'8
                ~
                c'2
                r8
                d'8
                ~
                d'2
            }

        ..  figure:: ../_images/contract_notes-rGCxpXl3rI.png

        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                r8
                c'8
                ~
                c'4.
                ~
                r8
                r8
                d'8
                ~
                d'4.
                ~
                r8
            }

        ..  figure:: ../_images/contract_notes-NoBsRNQJos.png

        Set ``rewrite_meter`` to ``False`` to disable this. The main reason for
        doing this is performance: when multiple mutations are being applied,
        it is faster to rewrite the meter just once at the end.

        >>> staff = abjad.Staff(r"\time 3/4 r8 c'8 ~ c'2 r8 d'8 ~ d'2")
        >>> auxjad.mutate.contract_notes(staff,
        ...                            abjad.Duration((1, 8)),
        ...                            rewrite_meter=False,
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                r8
                c'2
                ~
                r8
                r8
                d'2
                ~
                r8
            }

        ..  figure:: ../_images/contract_notes-VNHowP6bFi.png

    ..  warning::

        This function does not support tuplets. Using a container with one or
        more tuplets will result in a :exc:`ValueError` exception being raised:

        >>> staff = abjad.Staff(r"c'4 r4 \times 2/3 {r4 d'4 r4} e'4 r2.")
        >>> auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
        ValueError: first positional argument contains one ore more tuplets,
        which are not currently supported
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first positional argument must be 'abjad.Container' "
                        "or child class")
    if len(abjad.select(container).tuplets()) > 0:
        raise ValueError("first positional argument contains one ore more "
                         "tuplets, which are not currently supported")
    if not isinstance(max_contraction_duration,
                      (abjad.Duration, str, tuple, int, float),
                      ):
        raise TypeError("second positional argument must be 'abjad.Duration', "
                        "'str', 'tuple', or a number")
    if not isinstance(max_contraction_duration, abjad.Duration):
        max_contraction_duration = abjad.Duration(max_contraction_duration)
    if minimum_duration is not None:
        if not isinstance(minimum_duration, (abjad.Duration,
                                             str,
                                             tuple,
                                             int,
                                             float,
                                             )):
            raise TypeError("'minimum_duration' must be 'abjad.Duration', "
                            "'str', 'tuple', or a number")
        if not isinstance(minimum_duration, abjad.Duration):
            minimum_duration = abjad.Duration(minimum_duration)
    if not isinstance(use_multimeasure_rests, bool):
        raise TypeError("'use_multimeasure_rests' must be 'bool'")
    if not isinstance(rewrite_meter, bool):
        raise TypeError("'rewrite_meter' must be 'bool'")

    time_signatures = get.time_signature_list(container,
                                              implicit_common_time=False,
                                              )
    for logical_tie in abjad.select(container).logical_ties():
        if isinstance(logical_tie.head, (abjad.Rest, abjad.MultimeasureRest)):
            continue
        total_duration = abjad.get.duration(logical_tie)
        if total_duration <= minimum_duration:
            continue
        rest_duration = min(max_contraction_duration,
                            total_duration - minimum_duration
                            )
        if rest_duration == abjad.Duration((0, 1)):
            continue
        pitched_duration = total_duration - rest_duration

        indicators = abjad.get.indicators(logical_tie.head)

        if pitched_duration > abjad.Duration((0, 1)):
            if isinstance(logical_tie.head, abjad.Note):
                pitches = logical_tie.head.written_pitch
            elif isinstance(logical_tie.head, abjad.Chord):
                pitches = [pitch for pitch in logical_tie.head.written_pitches]
            replacement_items = abjad.LeafMaker()(
                [pitches, None],
                [pitched_duration, rest_duration],
            )
            if len(indicators) > 0:
                for indicator in indicators:
                    abjad.attach(indicator, replacement_items[0])
        else:
            replacement_items = abjad.LeafMaker()([None], [rest_duration])
        abjad.mutate.replace(logical_tie, replacement_items)
    mutate.enforce_time_signature(container,
                                  time_signatures,
                                  disable_rewrite_meter=True,
                                  )
    if rewrite_meter:
        mutate.auto_rewrite_meter(container)
    if use_multimeasure_rests:
        mutate.rests_to_multimeasure_rest(container[:])
