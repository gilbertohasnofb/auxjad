import abjad


def reposition_slurs(container: abjad.Container,
                     *,
                     allow_slurs_under_rests: bool = False,
                     remove_unterminated_slurs: bool = True,
                     ):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function repositions all slurs that
    starts or ends on rests.

    Example:
        This function will shift slurs that ends on rests to the previous
        pitched leaf.

        >>> staff = abjad.Staff(r"c'1( d'2 r2) r1 e'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            r2
            )
            r1
            e'1
        }

        .. figure:: ../_images/image-reposition_slurs-1.png

        >>> staff = abjad.Staff(r"c'1( d'2 r2) r1 e'1")
        >>> auxjad.reposition_slurs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            r1
            e'1
        }

        .. figure:: ../_images/image-reposition_slurs-2.png

    Example:
        Slurs starting on rests are shifted to the next pitched leaf.

        >>> staff = abjad.Staff(r"c'1 r2( d'2 e'1)")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            r2
            (
            d'2
            e'1
            )
        }

        .. figure:: ../_images/image-reposition_slurs-3.png

        >>> staff = abjad.Staff(r"c'1 r2( d'2 e'1)")
        >>> auxjad.reposition_slurs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            r2
            d'2
            (
            e'1
            )
        }

        .. figure:: ../_images/image-reposition_slurs-4.png

    Example:
        This function also works when multiple rests are present.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 r1) e'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            r2
            r1
            )
            e'1
        }

        .. figure:: ../_images/image-reposition_slurs-5.png

        >>> staff = abjad.Staff(r"c'1( d'2 r2 r1) e'1")
        >>> auxjad.reposition_slurs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            r1
            e'1
        }

        .. figure:: ../_images/image-reposition_slurs-6.png

    Example:
        By default, a slur crossing a rest is broken into two.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'1 f'1)")
        >>> auxjad.reposition_slurs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'1
            (
            f'1
            )
        }

        .. figure:: ../_images/image-reposition_slurs-7.png

        Set the optional keyword argument ``allow_slurs_under_rests`` to
        ``True`` to allow slurs under rests.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'1 f'1)")
        >>> auxjad.reposition_slurs(staff, allow_slurs_under_rests=True)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            r2
            e'1
            f'1
            )
        }

        .. figure:: ../_images/image-reposition_slurs-8.png

    Example:
        By default, unterminated slurs are removed.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1(")
        >>> auxjad.reposition_slurs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'2
            (
            f'2
            )
            g'1
        }

        .. figure:: ../_images/image-reposition_slurs-9.png

        Set the optional keyword argument ``remove_unterminated_slurs`` to
        ``True`` to disable this behaviour.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1(")
        >>> auxjad.reposition_slurs(staff, remove_unterminated_slurs=False)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'2
            (
            f'2
            )
            g'1
            (
        }

        .. figure:: ../_images/image-reposition_slurs-10.png

    ..  warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containings
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    if not isinstance(allow_slurs_under_rests, bool):
        raise TypeError("'allow_slurs_under_rests' must be 'bool'")

    leaves = abjad.select(container[:]).leaves()

    # checking for unfinished slurs
    if remove_unterminated_slurs:
        for leaf in leaves[::-1]:
            inspector = abjad.inspect(leaf)
            if inspector.indicator(abjad.StartSlur) is not None:
                if leaf is leaves[-1]:
                    abjad.detach(abjad.StartSlur(), leaf)
                elif (abjad.inspect(leaves[-1]).indicator(abjad.StopSlur)
                        is None):
                    abjad.attach(abjad.StopSlur(), leaves[-1])
            if inspector.indicator(abjad.StopSlur) is not None:
                break

    # shifting slurs from rests to notes
    shifted_startslur = None
    for leaf in leaves:
        inspector = abjad.inspect(leaf)
        if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
            if inspector.indicator(abjad.StartSlur) is not None:
                shifted_startslur = inspector.indicator(abjad.StartSlur)
                abjad.detach(abjad.StartSlur, leaf)
        else:
            if inspector.indicator(abjad.StartSlur) is None:
                if shifted_startslur is not None:
                    abjad.attach(shifted_startslur, leaf)
                    shifted_startslur = None
    shifted_stopslur = None
    for leaf in leaves[::-1]:
        inspector = abjad.inspect(leaf)
        if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
            if inspector.indicator(abjad.StopSlur) is not None:
                shifted_stopslur = inspector.indicator(abjad.StopSlur)
                abjad.detach(abjad.StopSlur, leaf)
        else:
            if inspector.indicator(abjad.StopSlur) is None:
                if shifted_stopslur is not None:
                    abjad.attach(shifted_stopslur, leaf)
                    shifted_stopslur = None

    # splitting slurs under rests
    if not allow_slurs_under_rests:
        active_slur = False
        for index, leaf in enumerate(leaves):
            inspector = abjad.inspect(leaf)
            if inspector.indicator(abjad.StartSlur) is not None:
                active_slur = True
            elif inspector.indicator(abjad.StopSlur) is not None:
                if not active_slur:
                    abjad.detach(abjad.StopSlur, leaf)
                active_slur = False
            if (isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest))
                    and active_slur):
                previous_leaf = abjad.select(leaf).with_previous_leaf()[0]
                if (abjad.inspect(previous_leaf).indicator(abjad.StopSlur)
                        is None):
                    abjad.attach(abjad.StopSlur(), previous_leaf)
                for next_leaf in leaves[index + 1:]:
                    if not isinstance(next_leaf, (abjad.Rest,
                                                  abjad.MultimeasureRest)):
                        if (abjad.inspect(next_leaf).indicator(abjad.StartSlur)
                                is None):
                            abjad.attach(abjad.StartSlur(), next_leaf)
                        break
        for leaf in leaves:
            inspector = abjad.inspect(leaf)
            if (inspector.indicator(abjad.StartSlur) is not None
                    and inspector.indicator(abjad.StopSlur) is not None):
                abjad.detach(abjad.StartSlur, leaf)
                abjad.detach(abjad.StopSlur, leaf)

    # removing slurs spanning a single logical tie
    for logical_tie in abjad.select(container[:]).logical_ties():
        inspector_head = abjad.inspect(logical_tie[0])
        inspector_tail = abjad.inspect(logical_tie[-1])
        if (inspector_head.indicator(abjad.StartSlur) is not None
                and inspector_tail.indicator(abjad.StopSlur) is not None):
            abjad.detach(abjad.StartSlur, logical_tie[0])
            abjad.detach(abjad.StopSlur, logical_tie[-1])
