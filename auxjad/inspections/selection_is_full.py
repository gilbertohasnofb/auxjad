import abjad

from .underfull_duration import underfull_duration


def selection_is_full(selection: abjad.Selection) -> bool:
    r"""Returns a :obj:`bool` representing whether the last measure of an input
    |abjad.Selection| is fully filled in or not.

    Basic usage:
        Returns ``True`` if the last measure of a selection is full, otherwise
        returns ``False``. If no time signature is encountered at the
        beginning, it uses LilyPond's convention and considers the container
        as in 4/4.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.inspect(container1[:]).selection_is_full()
        True
        >>> auxjad.inspect(container2[:]).selection_is_full()
        False
        >>> auxjad.inspect(container3[:]).selection_is_full()
        False
        >>> auxjad.inspect(container4[:]).selection_is_full()
        True

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.inspect()|. Therefore it can be used from either
        :func:`auxjad.inspect()` or |abjad.inspect()|, as shown below:

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> auxjad.inspect(container[:]).selection_is_full()
        True
        >>> abjad.inspect(container[:]).selection_is_full()
        True

    Time signature changes:
        Handles any time signatures as well as changes of time signature.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
        >>> auxjad.inspect(container1[:]).selection_is_full()
        True
        >>> auxjad.inspect(container2[:]).selection_is_full()
        True
        >>> auxjad.inspect(container3[:]).selection_is_full()
        False
        >>> auxjad.inspect(container4[:]).selection_is_full()
        False

    Partial time signatures:
        Correctly handles partial time signatures.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, container[0])
        >>> auxjad.inspect(container[:]).selection_is_full()
        True

    Multi-measure rests:
        It also handles multi-measure rests.

        >>> container1 = abjad.Container(r"R1")
        >>> container2 = abjad.Container(r"\time 3/4 R1*3/4 \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 R1*5/4 \time 4/4 g''4")
        >>> container4 = abjad.Container(r"\time 6/8 R1*1/2")
        >>> auxjad.inspect(container1[:]).selection_is_full()
        True
        >>> auxjad.inspect(container2[:]).selection_is_full()
        True
        >>> auxjad.inspect(container3[:]).selection_is_full()
        False
        >>> auxjad.inspect(container4[:]).selection_is_full()
        False

    .. error::

        If a selection is malformed, i.e. it has an underfilled measure before
        a time signature change, the function raises a :exc:`ValueError`
        exception. This is also the case when a selection starts in the middle
        of a measure.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
        >>> auxjad.inspect(container[:]).selection_is_full()
        ValueError: 'selection' is malformed, with an underfull measure
        preceding a time signature change

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
    return underfull_duration(selection) == abjad.Duration(0)
