import abjad


def simplified_time_signature_ratio(ratio: (tuple,
                                            abjad.TimeSignature,
                                            abjad.Duration,
                                            abjad.Meter,
                                            ),
                                    *,
                                    min_denominator: int = 4,
                                    output_pair_of_int: bool = False,
                                    ) -> (abjad.TimeSignature, tuple):
    r"""Returns an ``abjad.TimeSignature`` with the simplified ratio of an
    input ratio according to a minimum denominator value. The input ratio can
    be a ``tuple`` of integers, an ``abjad.TimeSignature``, ``abjad.Duration``,
    or an ``abjad.Meter``).

    ..  container:: example

        By default, the function simplifies the ratio of numerator/denominator
        using a minimum denominator value of 4 (that is, the denominator will
        not get smaller than 4). In the case below, (2, 4) is the simplest
        representation of the ratio (4, 8) with a denominator equal to or
        larger than 4.

        >>> time_signature = auxjad.simplified_time_signature_ratio((4, 8))
        >>> format(time_signature)
        abjad.TimeSignature((2, 4))
        >>> time_signature = auxjad.simplified_time_signature_ratio((1, 1))
        >>> format(time_signature)
        abjad.TimeSignature((4, 4))

        If a ratio cannot be simplified at all, the function returns a time
        signature with the original ratio.

        >>> time_signature = auxjad.simplified_time_signature_ratio((7, 8))
        >>> format(time_signature)
        abjad.TimeSignature((7, 8))

        The ``min_denominator`` can be set to values other than 4. If set to 2,
        the simplest representaion of the ratio (4, 8) becomes (1, 2).

        >>> time_signature = auxjad.simplified_time_signature_ratio(
        ...     (4, 8),
        ...     min_denominator=2,
        ... )
        >>> format(time_signature)
        abjad.TimeSignature((1, 2))
        >>> time_signature = auxjad.simplified_time_signature_ratio(
        ...     (1, 1),
        ...     min_denominator=1,
        ... )
        >>> format(time_signature)
        abjad.TimeSignature((1, 1))

    ..  container:: example

        By default, the function returns an ``abjad.TimeSignature`` for
        whatever type of argument it receives (which can be a ``tuple`` of
        integers, an ``abjad.TimeSignature``, an ``abjad.Duration``, or an
        ``abjad.Meter``).

        >>> arg = (4, 8)
        >>> time_signature = auxjad.simplified_time_signature_ratio(arg)
        >>> format(time_signature)
        abjad.TimeSignature((2, 4))

        >>> arg = abjad.Duration((4, 8))
        >>> time_signature = auxjad.simplified_time_signature_ratio(arg)
        >>> format(time_signature)
        abjad.TimeSignature((2, 4))

        >>> arg = abjad.Meter((4, 8))
        >>> time_signature = auxjad.simplified_time_signature_ratio(arg)
        >>> format(time_signature)
        abjad.TimeSignature((2, 4))

        >>> arg = abjad.TimeSignature((4, 8))
        >>> time_signature = auxjad.simplified_time_signature_ratio(arg)
        >>> format(time_signature)
        abjad.TimeSignature((2, 4))

        Call the function with the keyword argument ``output_pair_of_int`` set
        to ``True`` and the output will be a ``tuple`` of integers, regardless
        of the input argument.

        >>> arg = (4, 8)
        >>> pair = auxjad.simplified_time_signature_ratio(
        ...     arg,
        ...     output_pair_of_int=True,
        ... )
        >>> pair
        (2, 4)

        >>> arg = abjad.Duration((4, 8))
        >>> pair = auxjad.simplified_time_signature_ratio(
        ...     arg,
        ...     output_pair_of_int=True,
        ... )
        >>> assert pair == (2, 4)

        arg = abjad.Meter((4, 8))
        >>> pair = auxjad.simplified_time_signature_ratio(
        ...     arg,
        ...     output_pair_of_int=True,
        ... )
        >>> pair
        (2, 4)

        arg = abjad.TimeSignature((4, 8))
        >>> pair = auxjad.simplified_time_signature_ratio(
        ...     arg,
        ...     output_pair_of_int=True,
        ... )
        >>> pair
        (2, 4)
    """
    if not isinstance(ratio, (tuple, abjad.TimeSignature,
                              abjad.Duration, abjad.Meter)):
        raise TypeError("argument must be 'tuple', 'abjad.Duration', or "
                        "'abjad.TimeSignature'")
    if not isinstance(min_denominator, int):
        raise TypeError("'min_denominator' must be 'int'")
    if not isinstance(output_pair_of_int, bool):
        raise TypeError("'output_pair_of_int' must be 'bool'")

    if isinstance(ratio, (abjad.TimeSignature, abjad.Duration, abjad.Meter)):
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
        if (numerator % 2 == 0 and denominator % 2 == 0
                and denominator >= 2 * min_denominator):
            numerator /= 2
            denominator /= 2
        else:
            if not output_pair_of_int:
                return abjad.TimeSignature((int(numerator), int(denominator)))
            else:
                return int(numerator), int(denominator)
