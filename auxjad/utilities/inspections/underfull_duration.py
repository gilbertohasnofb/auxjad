import abjad


def underfull_duration(selection: abjad.Selection) -> abjad.Duration:
    r"""Returns a |abjad.Duration| representing the duration missing in the
    last measure of an input |abjad.Selection| which is not fully filled in.

    Basic usage:
        Returns the missing duration of the last measure of an
        |abjad.Selection|. If no time signature is encountered, it uses
        LilyPond's fallback time signature of ``4/4``.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.inspect(container1[:]).underfull_duration()
        0
        >>> auxjad.inspect(container2[:]).underfull_duration()
        1/4
        >>> auxjad.inspect(container3[:]).underfull_duration()
        3/4
        >>> auxjad.inspect(container4[:]).underfull_duration()
        0

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.inspect()|. Therefore it can be used from either
        :func:`auxjad.inspect()` or |abjad.inspect()|, as shown below:

        >>> container = abjad.Container(r"c'4 d'4 e'4")
        >>> auxjad.inspect(container[:]).underfull_duration()
        1/4
        >>> abjad.inspect(container[:]).underfull_duration()
        1/4

    Time signature changes:
        Handles any time signatures as well as changes of time signature.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
        >>> auxjad.inspect(container1[:]).underfull_duration()
        0
        >>> auxjad.inspect(container2[:]).underfull_duration()
        0
        >>> auxjad.inspect(container3[:]).underfull_duration()
        1/2
        >>> auxjad.inspect(container4[:]).underfull_duration()
        1/8

    Partial time signatures:
        Correctly handles partial time signatures.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, container[0])
        >>> auxjad.inspect(container[:]).underfull_duration()
        0

    Multi-measure rests:
        It also handles multi-measure rests.

        >>> container1 = abjad.Container(r"R1")
        >>> container2 = abjad.Container(r"\time 3/4 R1*3/4 \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 R1*5/4 \time 4/4 g''4")
        >>> container4 = abjad.Container(r"\time 6/8 R1*1/2")
        >>> auxjad.inspect(container1[:]).underfull_duration()
        0
        >>> auxjad.inspect(container2[:]).underfull_duration()
        0
        >>> auxjad.inspect(container3[:]).underfull_duration()
        3/4
        >>> auxjad.inspect(container4[:]).underfull_duration()
        1/4

    .. error::

        If a selection is malformed, i.e. it has an underfilled measure before
        a time signature change, the function raises a :exc:`ValueError`
        exception. This is also the case when a selection starts in the middle
        of a measure.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
        >>> auxjad.inspect(container[:]).underfull_duration()
        ValueError: 'selection' is malformed, with an underfull measure
        preceding a time signature change

    .. warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    leaves = selection.leaves()
    # handling first leaf
    time_signature = abjad.inspect(leaves[0]).effective(abjad.TimeSignature)
    if time_signature is not None:
        effective_time_signature = time_signature
    else:
        effective_time_signature = abjad.TimeSignature((4, 4))
    duration = abjad.inspect(leaves[0]).duration()
    # handling partial time signatures
    if effective_time_signature.partial is not None:
        duration += effective_time_signature.duration
        duration -= effective_time_signature.partial
    # all other leaves
    for leaf in leaves[1:]:
        time_signature = abjad.inspect(leaf).effective(abjad.TimeSignature)
        if (time_signature is not None
                and time_signature != effective_time_signature):
            if duration % effective_time_signature.duration != 0:
                raise ValueError("'selection' is malformed, with an underfull "
                                 "measure preceding a time signature change")
            effective_time_signature = time_signature
            duration = abjad.Duration(0)
        duration += abjad.inspect(leaf).duration()
    duration_last_bar = duration % effective_time_signature.duration
    duration_left = duration_last_bar
    if duration_last_bar > abjad.Duration(0):
        duration_left = effective_time_signature.duration - duration_last_bar
    return duration_left
