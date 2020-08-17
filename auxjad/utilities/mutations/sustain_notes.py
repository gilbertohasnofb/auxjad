import abjad

from .auto_rewrite_meter import auto_rewrite_meter


def sustain_notes(container: abjad.Container):
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function will sustain all pitched
    leaves until the next pitched leaf, thus replacing all rests in between
    them.

    Basic usage:
        Simply call the function on a container.

        >>> staff = abjad.Staff(r"c'16 r8. d'16 r8. e'16 r8. f'16 r8.")
        >>> abjad.f(staff)
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

        .. figure:: ../_images/sustain_notes-w1e1pmruyce.png

        >>> auxjad.mutate(staff).sustain_notes()
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/sustain_notes-ythfpvkrvue.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff).close_containers()
        >>> abjad.mutate(staff).close_containers()

    Leaves with same pitch:
        Leaves are sustained until the next pitched leaf, even if the pitch is
        the same.

        >>> staff = abjad.Staff(r"c'16 r8. c'16 r8. c'16 r8. c'16 r8.")
        >>> abjad.f(staff)
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

        .. figure:: ../_images/sustain_notes-oliqicqqw7q.png

        >>> auxjad.mutate(staff).sustain_notes()
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            c'4
            c'4
            c'4
        }

        .. figure:: ../_images/sustain_notes-3alcbmhc2jt.png

    Consecutive leaves with the same pitch:
        Consecutive pitched leaves with a same pitch will not be tied.

        >>> staff = abjad.Staff(
        ...     r"<c' e'>16 r8. <c' e'>4 <c' e'>4 <c' e'>16 r8."
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            <c' e'>16
            r8.
            <c' e'>4
            <c' e'>4
            <c' e'>16
            r8.
        }

        .. figure:: ../_images/sustain_notes-ek4ujjintt8.png

        >>> auxjad.mutate(staff).sustain_notes()
        >>> abjad.f(staff)
        \new Staff
        {
            <c' e'>4
            <c' e'>4
            <c' e'>4
            <c' e'>4
        }

        .. figure:: ../_images/sustain_notes-f7au6hojq99.png

    Tuplets:
        This function handles tuplets.

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 d'4 r4} r8 e'8 \times 2/3 {f'8 r4}"
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'4
                d'4
                r4
            }
            r8
            e'8
            \times 2/3 {
                f'8
                r4
            }
        }

        .. figure:: ../_images/sustain_notes-nsjvhnyrkea.png

        >>> auxjad.mutate(staff).sustain_notes()
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'4
                d'2
                ~
            }
            d'8
            e'8
            f'4
        }

        .. figure:: ../_images/sustain_notes-26l9hob8wko.png

    Complex example:
        This function can handle containers with a mixture of notes, chords,
        and rests, as well as tuplets.

        >>> staff = abjad.Staff(r"c'16 r8. d'16 r8. r8 r32 <e' g'>32 r16 r4 "
        ...                     r"\times 2/3 {r4 f'4 r4} r4 g'8 r8 a'4 ~ "
        ...                     r"a'16 r8. b'4 c''8 r8 "
        ...                     r"r4. d''8 \times 4/5 {r8 d''2}"
        ...                     )
        >>> abjad.f(staff)
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
            \times 2/3 {
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
            \times 4/5 {
                r8
                d''2
            }
        }

        .. figure:: ../_images/sustain_notes-cpw7dvpegge.png

        >>> auxjad.mutate(staff).sustain_notes()
        >>> abjad.f(staff)
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
            \times 2/3 {
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
            \times 4/5 {
                d''8
                d''2
            }
        }

        .. figure:: ../_images/sustain_notes-z8t2jwxsvar.png

    .. warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    leaves = abjad.select(container).leaves()
    pitch = None
    pitches = None
    for index, leaf in enumerate(leaves):
        if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
            if pitch is not None:
                replacement_leaf = abjad.Note(pitch,
                                              leaf.written_duration,
                                              )
            elif pitches is not None:
                replacement_leaf = abjad.Chord(pitches,
                                               leaf.written_duration,
                                               )
            if pitch is not None or pitches is not None:
                abjad.mutate(leaf).replace(replacement_leaf)
                previous_leaf = abjad.select(container).leaves()[index - 1]
                if abjad.inspect(previous_leaf).indicator(abjad.Tie) is None:
                    abjad.attach(abjad.Tie(), previous_leaf)
        elif isinstance(leaf, abjad.Note):
            pitch = leaf.written_pitch
            pitches = None
        elif isinstance(leaf, abjad.Chord):
            pitch = None
            pitches = leaf.written_pitches
    # rewriting meter
    auto_rewrite_meter(container)
