import abjad


def reposition_slurs(selection: abjad.Selection,
                     *,
                     allow_slurs_under_rests: bool = False,
                     close_unterminated_final_slur: bool = True,
                     ) -> None:
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function repositions all slurs that starts or ends on rests.

    Basic usage:
        This function will shift slurs that ends on rests to the previous
        pitched leaf.

        >>> staff = abjad.Staff(r"c'1( d'2 r2) r1 e'1")
        >>> abjad.show(staff)

        ..  docs::

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

        ..  figure:: ../_images/reposition_slurs-uxji4xx6ftk.png

        >>> staff = abjad.Staff(r"c'1( d'2 r2) r1 e'1")
        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.show(staff)

        ..  docs::

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

        ..  figure:: ../_images/reposition_slurs-7nnp5cttm4y.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.mutate.reposition_slurs(staff[:])

    Rests:
        Slurs starting on rests are shifted to the next pitched leaf.

        >>> staff = abjad.Staff(r"c'1 r2( d'2 e'1)")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                r2
                (
                d'2
                e'1
                )
            }

        ..  figure:: ../_images/reposition_slurs-2j7hgqd7bt1.png

        >>> staff = abjad.Staff(r"c'1 r2( d'2 e'1)")
        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                r2
                d'2
                (
                e'1
                )
            }

        ..  figure:: ../_images/reposition_slurs-i957u1wt30m.png

    Multiple rests:
        This function also works when multiple rests are present.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 r1) e'1")
        >>> abjad.show(staff)

        ..  docs::

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

        ..  figure:: ../_images/reposition_slurs-v76u42x7idk.png

        >>> staff = abjad.Staff(r"c'1( d'2 r2 r1) e'1")
        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.show(staff)

        ..  docs::

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

        ..  figure:: ../_images/reposition_slurs-burs1t0daid.png

    ``allow_slurs_under_rests``:
        By default, a slur crossing a rest is broken into two.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'1 f'1)")
        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.show(staff)

        ..  docs::

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

        ..  figure:: ../_images/reposition_slurs-8wb7orpt285.png

        Set the optional keyword argument ``allow_slurs_under_rests`` to
        ``True`` to allow slurs under rests.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'1 f'1)")
        >>> auxjad.mutate.reposition_slurs(
        ...     staff[:],
        ...     allow_slurs_under_rests=True,
        ... )
        >>> abjad.show(staff)

        ..  docs::

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

        ..  figure:: ../_images/reposition_slurs-ftb59kz6u8j.png

    ``close_unterminated_final_slur``:
        By default, unterminated slurs at the end of the selection are closed
        when possible or removed when not.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1( a'1")
        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.show(staff)

        ..  docs::

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
                a'1
                )
            }

        ..  figure:: ../_images/reposition_slurs-70dli8e0kqr.png

        Set the optional keyword argument ``close_unterminated_final_slur`` to
        ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1( a'1")
        >>> auxjad.mutate.reposition_slurs(
        ...     staff[:],
        ...     close_unterminated_final_slur=False,
        ... )
        >>> abjad.show(staff)

        ..  docs::

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
                a'1
            }

        ..  figure:: ../_images/reposition_slurs-1usa2dezl45.png

        When there are no pitched leaves left after an unterminated open slur,
        it is removed.

        >>> staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1( r1")
        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.show(staff)

        ..  docs::

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
                r1
            }

        ..  figure:: ../_images/reposition_slurs-a0uakfcltuf.png

    ..  note::

        Duplicate slur starts or stops are removed. Note that the score output
        will not change, as LilyPond also ignores duplicate slurs, but the
        output in the ``.ly`` file will be cleaner.

        >>> staff = abjad.Staff(r"c'1( d'2) e'2) f'2( g'2( a'1)")
        >>> auxjad.mutate.reposition_slurs(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                (
                d'2
                )
                e'2
                f'2
                (
                g'2
                a'1
                )
            }

        ..  figure:: ../_images/reposition_slurs-0ugn322x3tr.png

    ..  warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    if not isinstance(allow_slurs_under_rests, bool):
        raise TypeError("'allow_slurs_under_rests' must be 'bool'")
    if not isinstance(close_unterminated_final_slur, bool):
        raise TypeError("'close_unterminated_final_slur' must be 'bool'")

    leaves = selection.leaves()

    # checking for final unfinished slurs
    if close_unterminated_final_slur:
        for leaf in leaves[::-1]:
            if abjad.get.indicator(leaf, abjad.StartSlur) is not None:
                if leaf is leaves[-1]:
                    abjad.detach(abjad.StartSlur, leaf)
                elif (abjad.get.indicator(leaves[-1], abjad.StopSlur) is None):
                    abjad.attach(abjad.StopSlur(), leaves[-1])
            if abjad.get.indicator(leaf, abjad.StopSlur) is not None:
                break

    # checking for duplicate open or close slurs
    start_slur_count = 0
    stop_slur_count = 0
    for leaf in leaves:
        if abjad.get.indicator(leaf, abjad.StartSlur) is not None:
            start_slur_count += 1
            stop_slur_count = 0
            if start_slur_count > 1:
                abjad.detach(abjad.StartSlur, leaf)
        elif abjad.get.indicator(leaf, abjad.StopSlur) is not None:
            stop_slur_count += 1
            start_slur_count = 0
            if stop_slur_count > 1:
                abjad.detach(abjad.StopSlur, leaf)

    # shifting slurs from rests to notes
    shifted_startslur = None
    for leaf in leaves:
        if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
            if abjad.get.indicator(leaf, abjad.StartSlur) is not None:
                shifted_startslur = abjad.get.indicator(leaf, abjad.StartSlur)
                abjad.detach(abjad.StartSlur, leaf)
        else:
            if abjad.get.indicator(leaf, abjad.StartSlur) is None:
                if shifted_startslur is not None:
                    abjad.attach(shifted_startslur, leaf)
                    shifted_startslur = None
    shifted_stopslur = None
    for leaf in leaves[::-1]:
        if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
            if abjad.get.indicator(leaf, abjad.StopSlur) is not None:
                shifted_stopslur = abjad.get.indicator(leaf, abjad.StopSlur)
                abjad.detach(abjad.StopSlur, leaf)
        else:
            if abjad.get.indicator(leaf, abjad.StopSlur) is None:
                if shifted_stopslur is not None:
                    abjad.attach(shifted_stopslur, leaf)
                    shifted_stopslur = None

    # splitting slurs under rests
    if not allow_slurs_under_rests:
        active_slur = False
        for index, leaf in enumerate(leaves):
            if abjad.get.indicator(leaf, abjad.StartSlur) is not None:
                active_slur = True
            elif abjad.get.indicator(leaf, abjad.StopSlur) is not None:
                if not active_slur:
                    abjad.detach(abjad.StopSlur, leaf)
                active_slur = False
            if (isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest))
                    and active_slur):
                previous_leaf = abjad.select(leaf).with_previous_leaf()[0]
                if (abjad.get.indicator(previous_leaf, abjad.StopSlur)
                        is None):
                    abjad.attach(abjad.StopSlur(), previous_leaf)
                    active_slur = False
                for next_leaf in leaves[index + 1:]:
                    if not isinstance(next_leaf, (abjad.Rest,
                                                  abjad.MultimeasureRest,
                                                  )):
                        if (abjad.get.indicator(next_leaf, abjad.StartSlur)
                                is None):
                            abjad.attach(abjad.StartSlur(), next_leaf)
                        break
        for leaf in leaves:
            if (abjad.get.indicator(leaf, abjad.StartSlur) is not None
                    and abjad.get.indicator(leaf, abjad.StopSlur) is not None):
                abjad.detach(abjad.StartSlur, leaf)
                abjad.detach(abjad.StopSlur, leaf)

    # removing slurs spanning a single logical tie
    for logical_tie in selection.logical_ties():
        if (abjad.get.indicator(logical_tie[0], abjad.StartSlur) is not None
                and abjad.get.indicator(logical_tie[-1], abjad.StopSlur)
                is not None):
            abjad.detach(abjad.StartSlur, logical_tie[0])
            abjad.detach(abjad.StopSlur, logical_tie[-1])
