import abjad


def remove_repeated_time_signatures(container: abjad.Container):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value. This function removes all consecutive
    repeated time signatures.

    ..  container:: example

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

    ..  container:: example

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

    ..  container:: example

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

    measures = [measure for measure in
                abjad.select(container).leaves().group_by_measure()]

    previous_time_signature = None
    for measure in measures:
        time_signature = abjad.inspect(measure[0]).indicator(
            abjad.TimeSignature
        )
        if time_signature == previous_time_signature:
            abjad.detach(abjad.TimeSignature, measure[0])
        if time_signature:
            previous_time_signature = time_signature
