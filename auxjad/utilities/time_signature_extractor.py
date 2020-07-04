import abjad


def time_signature_extractor(container: abjad.Container,
                             *,
                             do_not_use_none: bool = False,
                             implicit_common_time: bool = True,
                             omit_repeated: bool = False,
                             ):
    r"""Returns a ``list`` with the ``abjad.TimeSignature`` for all measures of
    an input ``abjad.Container``.

    Example:
        This function returns a list with one ``abjad.TimeSignature`` per
        measure.

        >>> container = abjad.Container(r"\time 3/4 c'2. \time 4/4 e'1")
        >>> time_signatures = auxjad.time_signature_extractor(container)
        >>> time_signatures
        [TimeSignature((3, 4)), TimeSignature((4, 4))]

    Example:
        By default, the list will contain a ``None`` if a measure does
        not have an explicit time signature.

        >>> container = abjad.Container(
        ...     r"\time 5/8 c'4 ~ c'16 \time 3/8 d'4. e'4.")
        >>> time_signatures = auxjad.time_signature_extractor(container)
        >>> time_signatures
        [TimeSignature((5, 8)), TimeSignature((3, 8)), None]

        Set the keyword argument ``do_not_use_none`` to ``True`` to change this
        behaviour.

        >>> time_signatures = auxjad.time_signature_extractor(
        ...     container,
        ...     do_not_use_none=True,
        ... )
        >>> time_signatures
        [TimeSignature((5, 8)), TimeSignature((3, 8)), TimeSignature((3, 8))]

    Example:
        By default, time signatures are output according to the container, even
        if there are multiple instances of a same time signature.

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'2. d'2. \time 3/4 e'2. f'2.")
        >>> time_signatures = auxjad.time_signature_extractor(container)
        >>> time_signatures
        [abjad.TimeSignature((3, 4)), None, abjad.TimeSignature((3, 4)), None]

        Set the keyword argument ``omit_repeated`` to ``True`` to replace
        repeated time signatures with ``None``.

        >>> time_signatures = auxjad.time_signature_extractor(
        ...     container,
        ...     omit_repeated=True,
        ... )
        >>> time_signatures
        [abjad.TimeSignature((3, 4)), None, None, None]

    ..  error::

        Setting both ``do_not_use_none`` and ``omit_repeated`` to ``True``
        will raise an exception:

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'2. d'2. \time 3/4 e'2. f'2.")
        >>> time_signatures = auxjad.time_signature_extractor(
        ...     container,
        ...     do_not_use_none=True,
        ...     omit_repeated=True,
        ... )
        ValueError: 'omit_repeated' and 'do_not_use_none' cannot be both set to
        'True'

    Example:
        LilyPond uses an implicit time signature of 4/4 whenever a time
        signature is not found. This function behaves the same way.

        >>> container = abjad.Container(r"c'1 d'1 e'1 f'1")
        >>> time_signatures = auxjad.time_signature_extractor(container)
        >>> time_signatures
        [TimeSignature((4, 4)), None, None, None]

        To disable this behaviour, set ``implicit_common_time`` to ``False``.

        >>> time_signatures = auxjad.time_signature_extractor(
        ...     container,
        ...     implicit_common_time=False,
        ... )
        >>> time_signatures
        [None, None, None, None]

    ..  error::

        Setting ``do_not_use_none`` to ``True`` and ``implicit_common_time`` to
        ``False`` on a container that starts with no time signature will raise
        an exception:

        >>> container = abjad.Container(r"c'1 d'1 e'1 f'1")
        >>> time_signatures = auxjad.time_signature_extractor(
        ...     container,
        ...     do_not_use_none=True,
        ...     implicit_common_time=False,
        ... )
        ValueError: container does not have a time signature attached to its
        first leaf, with 'implicit_common_time' set to 'False' and
        'omit_repeated' set to 'True'
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first argument must be 'abjad.Container' or "
                        "child class")
    if not isinstance(do_not_use_none, bool):
        raise TypeError("'do_not_use_none' must be 'bool'")
    if not isinstance(implicit_common_time, bool):
        raise TypeError("'implicit_common_time' must be 'bool'")
    if not isinstance(omit_repeated, bool):
        raise TypeError("'omit_repeated' must be 'bool'")
    if omit_repeated and do_not_use_none:
        raise ValueError("'omit_repeated' and 'do_not_use_none' cannot be "
                         "both set to 'True'")
    if not implicit_common_time and do_not_use_none:
        if not abjad.inspect(abjad.select(container).leaf(0)).indicator(
                abjad.TimeSignature):
            raise ValueError("container does not have a time signature "
                             "attached to its first leaf, with "
                             "'implicit_common_time' set to 'False' and "
                             "'omit_repeated' set to 'True'")

    measures = abjad.select(container[:]).group_by_measure()
    time_signatures = []

    for i, measure in enumerate(measures):
        head = abjad.select(measure).leaf(0)
        time_signature = abjad.inspect(head).indicator(abjad.TimeSignature)
        if i == 0 and time_signature is None:
            if implicit_common_time:
                time_signature = abjad.TimeSignature((4, 4))
        time_signatures.append(time_signature)

    if do_not_use_none:
        if time_signatures[0] is None:
            time_signatures[0] = abjad.TimeSignature((4, 4))
        for i in range(1, len(time_signatures)):
            if time_signatures[i] is None:
                time_signatures[i] = abjad.TimeSignature(
                    time_signatures[i - 1].pair)
    elif omit_repeated:
        effective_time_signature = None
        for i in range(len(time_signatures)):
            current_time_signature = time_signatures[i]
            if current_time_signature is not None:
                current_time_signature = abjad.TimeSignature(
                    current_time_signature.pair)
            if current_time_signature == effective_time_signature:
                time_signatures[i] = None
            else:
                if current_time_signature is not None:
                    effective_time_signature = current_time_signature

    return time_signatures
