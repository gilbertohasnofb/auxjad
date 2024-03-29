import abjad

from .. import select
from .auto_rewrite_meter import auto_rewrite_meter


def sustain_notes(container: abjad.Container,
                  *,
                  sustain_multimeasure_rests: bool = True,
                  rewrite_meter: bool = True,
                  ) -> None:
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function will sustain all pitched
    leaves until the next pitched leaf, thus replacing all rests in between
    them.

    Basic usage:
        Simply call the function on a container.

        >>> staff = abjad.Staff(r"c'16 r8. d'16 r8. e'16 r8. f'16 r8.")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r8.
                d'16
                r8.
                e'16
                r8.
                f'16
                r8.
            }

        ..  figure:: ../_images/sustain_notes-w1e1pmruyce.png

        >>> auxjad.mutate.sustain_notes(staff)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

        ..  figure:: ../_images/sustain_notes-ythfpvkrvue.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.close_containers(staff)
        >>> abjad.mutate.close_containers(staff)

    Leaves with same pitch:
        Leaves are sustained until the next pitched leaf, even if the pitch is
        the same.

        >>> staff = abjad.Staff(r"c'16 r8. c'16 r8. c'16 r8. c'16 r8.")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r8.
                c'16
                r8.
                c'16
                r8.
                c'16
                r8.
            }

        ..  figure:: ../_images/sustain_notes-oliqicqqw7q.png

        >>> auxjad.mutate.sustain_notes(staff)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                c'4
                c'4
                c'4
            }

        ..  figure:: ../_images/sustain_notes-3alcbmhc2jt.png

    Consecutive leaves with the same pitch:
        Consecutive pitched leaves with a same pitch will not be tied.

        >>> staff = abjad.Staff(
        ...     r"<c' e'>16 r8. <c' e'>4 <c' e'>4 <c' e'>16 r8."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                <c' e'>16
                r8.
                <c' e'>4
                <c' e'>4
                <c' e'>16
                r8.
            }

        ..  figure:: ../_images/sustain_notes-ek4ujjintt8.png

        >>> auxjad.mutate.sustain_notes(staff)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                <c' e'>4
                <c' e'>4
                <c' e'>4
                <c' e'>4
            }

        ..  figure:: ../_images/sustain_notes-f7au6hojq99.png

    Tuplets:
        This function handles tuplets.

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 d'4 r4} r8 e'8 \times 2/3 {f'8 r4}"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \times 2/3
                {
                    c'4
                    d'4
                    r4
                }
                r8
                e'8
                \times 2/3
                {
                    f'8
                    r4
                }
            }

        ..  figure:: ../_images/sustain_notes-nsjvhnyrkea.png

        >>> auxjad.mutate.sustain_notes(staff)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \times 2/3
                {
                    c'4
                    d'2
                    ~
                }
                d'8
                e'8
                f'4
            }

        ..  figure:: ../_images/sustain_notes-26l9hob8wko.png

    Complex example:
        This function can handle containers with a mixture of notes, chords,
        and rests, as well as tuplets.

        >>> staff = abjad.Staff(
        ...     r"c'16 r8. d'16 r8. r8 r32 <e' g'>32 r16 r4 "
        ...     r"\times 2/3 {r4 f'4 r4} r4 g'8 r8 a'4 ~ "
        ...     r"a'16 r8. b'4 c''8 r8 "
        ...     r"r4. d''8 \times 4/5 {r8 d''2}"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r8.
                d'16
                r8.
                r8
                r32
                <e' g'>32
                r16
                r4
                \times 2/3
                {
                    r4
                    f'4
                    r4
                }
                r4
                g'8
                r8
                a'4
                ~
                a'16
                r8.
                b'4
                c''8
                r8
                r4.
                d''8
                \times 4/5
                {
                    r8
                    d''2
                }
            }

        ..  figure:: ../_images/sustain_notes-cpw7dvpegge.png

        >>> auxjad.mutate.sustain_notes(staff)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                d'4
                ~
                d'8
                ~
                d'32
                <e' g'>16.
                ~
                <e' g'>4
                ~
                \times 2/3
                {
                    <e' g'>4
                    f'2
                    ~
                }
                f'4
                g'4
                a'2
                b'4
                c''4
                ~
                c''4.
                d''8
                ~
                \times 4/5
                {
                    d''8
                    d''2
                }
            }

        ..  figure:: ../_images/sustain_notes-z8t2jwxsvar.png

    ``sustain_multimeasure_rests``:
        By default, notes are tied across multi-measure rests.

        >>> staff = abjad.Staff(
        ...     r"r4 c'16 r8. d'16 r4.. "
        ...     r"R1 "
        ...     r"r4 e'4 r2 "
        ...     r"\time 5/8 r8 f'4 r4 "
        ...     r"R1 * 5/8 "
        ...     r"r8 g'8 a'8 r4"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                r4
                c'16
                r8.
                d'16
                r4..
                R1
                r4
                e'4
                r2
                \time 5/8
                r8
                f'4
                r4
                R1 * 5/8
                r8
                g'8
                a'8
                r4
            }

        ..  figure:: ../_images/sustain_notes-mJOOARIUAp.png

        >>> auxjad.mutate.sustain_notes(staff)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                r4
                c'4
                d'2
                ~
                d'1
                ~
                d'4
                e'2.
                ~
                \time 5/8
                e'8
                f'2
                ~
                f'4.
                ~
                f'4
                ~
                f'8
                g'8
                a'4.
            }

        ..  figure:: ../_images/sustain_notes-iLTiWERSvO.png

        To disable sustaining across those, set ``sustain_multimeasure_rests``
        to  ``False``:

        >>> auxjad.mutate.sustain_notes(staff, sustain_multimeasure_rests=True)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                r4
                c'4
                d'2
                R1
                r4
                e'2.
                ~
                \time 5/8
                e'8
                f'2
                R1 * 5/8
                r8
                g'8
                a'4.
            }

        ..  figure:: ../_images/sustain_notes-9WeilArLex.png

    ``rewrite_meter``:
        By default, |auxjad.mutate.auto_rewrite_meter()| is summoned after
        notes are sustained.

        >>> staff = abjad.Staff(
        ...     r"r4 c'16 r8. d'16 r4.. "
        ...     r"R1"
        ...     r"r4 e'4 r2"
        ...     r"\time 5/8 r8 f'4 r4"
        ...     r"R1 * 5/8 "
        ...     r"r8 g'8 a'8 r4"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                r4
                c'16
                r8.
                d'16
                r4..
                R1
                r4
                e'4
                r2
                \time 5/8
                r8
                f'4
                r4
                R1 * 5/8
                r8
                g'8
                a'8
                r4
            }

        ..  figure:: ../_images/sustain_notes-Egibb7mRfJ.png

        To disable this behaviour, set ``rewrite_meter`` to ``False``:

        >>> auxjad.mutate.sustain_notes(staff, rewrite_meter=False)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                r4
                c'16
                ~
                c'8.
                d'16
                ~
                d'4..
                ~
                d'1
                ~
                d'4
                e'4
                ~
                e'2
                ~
                \time 5/8
                e'8
                f'4
                ~
                f'4
                ~
                f'2
                ~
                f'8
                ~
                f'8
                g'8
                a'8
                ~
                a'4
            }

        ..  figure:: ../_images/sustain_notes-iTuoVMoWgm.png

    ..  warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    if not isinstance(sustain_multimeasure_rests, bool):
        raise TypeError("'sustain_multimeasure_rests' must be 'bool'")
    if not isinstance(rewrite_meter, bool):
        raise TypeError("'rewrite_meter' must be 'bool'")

    logical_selections = select.logical_selections(
        container,
        include_multimeasure_rests=sustain_multimeasure_rests,
    )
    pitch = None
    last_leaf = None
    for logical_selection in logical_selections:
        first_leaf = abjad.select(logical_selection).leaf(0)
        # if pitched
        if isinstance(first_leaf, abjad.Note):
            pitch = first_leaf.written_pitch
            last_leaf = abjad.select(logical_selection).leaf(-1)
            continue
        elif isinstance(first_leaf, abjad.Chord):
            # needs 2D list as abjad.LeafMaker considers a single pitch list as
            # a series of consecutive pitches, but any sublist as a chord
            pitch = [[pitch for pitch in first_leaf.written_pitches]]
            last_leaf = abjad.select(logical_selection).leaf(-1)
            continue
        # if not pitched
        for leaf in abjad.select(logical_selection).leaves():
            if last_leaf is None:
                break
            elif isinstance(leaf, abjad.Rest):
                duration = leaf.written_duration
            elif isinstance(leaf, abjad.MultimeasureRest):
                if not sustain_multimeasure_rests:
                    pitch = None
                    last_leaf = None
                    break
                duration = abjad.get.duration(leaf)
            else:
                raise TypeError("Leaves in 'container' must be notes, chords,"
                                "rests, or multi-measure rests")
            if abjad.get.indicator(last_leaf, abjad.Tie) is None:
                abjad.attach(abjad.Tie(), last_leaf)
            new_leaves = abjad.LeafMaker()(pitch, duration)
            for indicator in abjad.get.indicators(leaf):
                abjad.attach(indicator,
                             abjad.select(new_leaves).leaf(0),
                             )
            abjad.mutate.replace(leaf, new_leaves)
            last_leaf = abjad.select(new_leaves).leaf(-1)

    # rewriting meter
    if rewrite_meter:
        auto_rewrite_meter(container)
