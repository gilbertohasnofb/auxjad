import abjad


def remove_repeated_time_signatures(container: abjad.Container):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function removes all consecutive
    repeated time signatures.

    Example:
        When two consecutive bars have identical time signatures, the second
        one is removed:

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

        .. figure:: ../_images/image-remove_repeated_time_signatures-1.png

        >>> auxjad.remove_repeated_time_signatures(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            c'4
            d'8
        }

        .. figure:: ../_images/image-remove_repeated_time_signatures-2.png

    Example:
        The function also removes time signatures that are separated by an
        arbitrary number of bars without one:

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

        .. figure:: ../_images/image-remove_repeated_time_signatures-3.png

        >>> auxjad.remove_repeated_time_signatures(staff)
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

        .. figure:: ../_images/image-remove_repeated_time_signatures-4.png

    Example:
        The input container can also handle subcontainers, including cases in
        which the time signatures are attached to leaves of subcontainers:

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

        .. figure:: ../_images/image-remove_repeated_time_signatures-5.png

        >>> auxjad.remove_repeated_time_signatures(staff)
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

        .. figure:: ../_images/image-remove_repeated_time_signatures-6.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")

    measures = abjad.select(container[:]).group_by_measure()

    head = abjad.select(container).leaf(0)
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
