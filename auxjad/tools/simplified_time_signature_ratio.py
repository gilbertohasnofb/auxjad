import abjad


def simplified_time_signature_ratio(ratio,
                                    *,
                                    min_denominator: int = 4,
                                    ) -> tuple:
    r"""A function simplifies the ratio of a given time signature respecting a
    minimum denominator value. Input is a tuple of two integers.

    ..  container:: example

        By default, the function simplifies the ratio of numerator/denominator
        using a minimum denominator value of 4 (that is, the denominator will
        not get smaller than 4). In the case below, (2, 4) is the simplest
        representaion of the ratio (4, 8) with a denominator equal to or larger
        than 4.

        >>> ratio = auxjad.simplified_time_signature_ratio((4, 8))
        >>> time_signature = abjad.TimeSignature(ratio)
        >>> format(time_signature)
        abjad.TimeSignature((2, 4))

        If a ratio cannot be simplified at all, the function returns the
        original values.

        >>> ratio = auxjad.simplified_time_signature_ratio((7, 8))
        >>> time_signature = abjad.TimeSignature(ratio)
        >>> format(time_signature)
        abjad.TimeSignature((7, 8))

        The min_denominator can be set to values other than 4. If set to 2,
        the simplest representaion of the ratio (4, 8) becomes (1, 2).

        >>> ratio = auxjad.simplified_time_signature_ratio((4, 8),
        ...                                                min_denominator=2
        ...                                                )
        >>> time_signature = abjad.TimeSignature(ratio)
        >>> format(time_signature)
        abjad.TimeSignature((1, 2))

    """
    if not isinstance(ratio, (tuple, abjad.Duration, abjad.TimeSignature)):
        raise TypeError("'ratio' must be 'tuple' or duration")
    if not isinstance(min_denominator, int):
        raise TypeError("'min_denominator' must be 'int'")

    abjad_duration = False
    abjad_time_signature = False
    if isinstance(ratio, abjad.Duration):
        abjad_duration = True
        numerator, denominator = ratio.pair
    elif isinstance(ratio, abjad.TimeSignature):
        abjad_time_signature = True
        numerator, denominator = ratio.pair
    else:
        numerator, denominator = ratio
        if not isinstance(numerator, int):
            raise TypeError("'ratio's elements must be 'int'")
        if not isinstance(denominator, int):
            raise TypeError("'ratio's elements must be 'int'")

    while denominator < min_denominator:
        numerator *= 2
        denominator *= 2
    while True:
        if numerator % 2 == 0 and denominator % 2 == 0 and \
                denominator >= 2 * min_denominator:
            numerator /= 2
            denominator /= 2
        else:
            if abjad_duration:
                return abjad.Duration(int(numerator), int(denominator))
            elif abjad_time_signature:
                return abjad.TimeSignature((int(numerator), int(denominator)))
            else:
                return int(numerator), int(denominator)
