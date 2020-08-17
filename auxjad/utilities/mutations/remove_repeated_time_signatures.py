import abjad


def remove_repeated_time_signatures(selection: abjad.Selection):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function removes all consecutive repeated time signatures.

    Basic usage:
        When two consecutive measures have identical time signatures, the
        second one is removed:

        >>> staff = abjad.Staff(r"c'4 d'8 | c'4 d'8")
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[2])
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            \time 3/8
            c'4
            d'8
        }

        .. figure:: ../_images/remove_repeated_time_signatures-feZSi4Trsg.png

        >>> auxjad.mutate(staff[:]).remove_repeated_time_signatures()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            c'4
            d'8
        }

        .. figure:: ../_images/remove_repeated_time_signatures-ImmpJOWn5U.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).remove_repeated_time_signatures()
        >>> abjad.mutate(staff[:]).remove_repeated_time_signatures()

    Time signature structure:
        The function also removes time signatures that are separated by an
        arbitrary number of measures without one:

        >>> staff = abjad.Staff(r"c'4 d'8 e'4. c'4 d'8")
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[3])
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            e'4.
            \time 3/8
            c'4
            d'8
        }

        .. figure:: ../_images/remove_repeated_time_signatures-ihs4kU1dMe.png

        >>> auxjad.mutate(staff[:]).remove_repeated_time_signatures()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            e'4.
            c'4
            d'8
        }

        .. figure:: ../_images/remove_repeated_time_signatures-Ans1RrG5ZW.png

    Subcontainers:
        The container from which the selection is made can also have
        subcontainers, including cases in which the time signatures are
        attached to leaves of subcontainers:

        >>> staff = abjad.Staff([abjad.Note("c'2"),
        ...                      abjad.Chord("<d' f'>2"),
        ...                      abjad.Tuplet((2, 3), "g2 a2 b2"),
        ...                      ])
        >>> abjad.attach(abjad.TimeSignature((2, 2)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((2, 2)), staff[2][0])
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/2
            c'2
            <d' f'>2
            \times 2/3 {
                \time 2/2
                g2
                a2
                b2
            }
        }

        .. figure:: ../_images/remove_repeated_time_signatures-Nybwh816FT.png

        >>> auxjad.mutate(staff[:]).remove_repeated_time_signatures()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/2
            c'2
            <d' f'>2
            \times 2/3 {
                g2
                a2
                b2
            }
        }

        .. figure:: ../_images/remove_repeated_time_signatures-PNCfPcnTtj.png

    .. warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")

    measures = selection.group_by_measure()
    head = selection.leaf(0)
    previous_time_signature = abjad.inspect(head).indicator(
        abjad.TimeSignature
    )
    if previous_time_signature is None:
        previous_time_signature = abjad.TimeSignature((4, 4))
    for measure in measures[1:]:
        head = abjad.select(measure).leaf(0)
        time_signature = abjad.inspect(head).indicator(abjad.TimeSignature)
        if time_signature == previous_time_signature:
            abjad.detach(abjad.TimeSignature, head)
        elif time_signature is not None:
            previous_time_signature = time_signature
