import abjad


def add_double_bar_lines_before_time_signatures(
    selection: abjad.Selection,
) -> None:
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function adds double bar lines before all time signatures.

    Basic usage:
        Whenever a new time signature appears, the function adds a double bar
        line before it:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
        ... )
        >>> auxjad.mutate.add_double_bar_lines_before_time_signatures(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2.
                \bar "||"
                \time 4/4
                d'1
                e'1
                \bar "||"
                \time 6/4
                f'2.
                g'2.
            }

        ..  figure:: ../_images/remove_repeated_time_signatures-2O7JyxN1CS.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.add_double_bar_lines_before_time_signatures(staff[:])
        >>> abjad.mutate.add_double_bar_lines_before_time_signatures(staff[:])

    Multi-measure rests:
        This function can handle multi-measure rests too.

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 R1 * 3/4 "
        ...     r"\time 4/4 R1 * 2 "
        ...     r"\time 6/4 R1 * 6/4 "
        ...     r"\time 4/4 R1"
        ... )
        >>> auxjad.mutate.add_double_bar_lines_before_time_signatures(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                R1 * 3/4
                \bar "||"
                \time 4/4
                R1 * 2
                \bar "||"
                \time 6/4
                R1 * 3/2
                \bar "||"
                \time 4/4
                R1
            }

        ..  figure:: ../_images/remove_repeated_time_signatures-aYmnnFDdRh.png

    Input with bar lines:
        If the input selection already contains bar lines at poinst where a
        time signature change, the function will only replace those of type
        ``"|"`` or ``""``, keeping all others as they were.

        >>> staff = abjad.Staff(
        ...     r"R1 "
        ...     r"\time 3/4 c'2. "
        ...     r"\time 4/4 d'1 "
        ...     r"e'1 "
        ...     r"\time 6/4 f'2. g'2. "
        ...     r"\time 2/4 a'2"
        ... )
        >>> abjad.attach(abjad.BarLine('.|:'), staff[0])
        >>> abjad.attach(abjad.BarLine(':|.'), staff[1])
        >>> abjad.attach(abjad.BarLine('|'), staff[3])
        >>> abjad.attach(abjad.BarLine('!'), staff[5])
        >>> auxjad.mutate.add_double_bar_lines_before_time_signatures(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                R1
                \bar ".|:"
                \time 3/4
                c'2.
                \bar ":|."
                \time 4/4
                d'1
                e'1
                \bar "||"
                \time 6/4
                f'2.
                g'2.
                \bar "!"
                \time 2/4
                a'2
            }

        ..  figure:: ../_images/remove_repeated_time_signatures-jUymJWLdR7.png

    ..  warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")

    leaves = selection.leaves()

    for i, leaf in enumerate(leaves[1:], 1):
        time_signature = abjad.get.indicator(leaf, abjad.TimeSignature)
        if time_signature is not None:
            bar_line = abjad.get.indicator(leaves[i - 1], abjad.BarLine)
            if bar_line is not None and bar_line.abbreviation in ('|', ''):
                abjad.detach(abjad.BarLine, leaves[i - 1])
                bar_line = None
            if bar_line is None:
                abjad.attach(abjad.BarLine("||"),
                             leaves[i - 1],
                             context='Staff',
                             )
