import abjad

from .remove_repeated_dynamics import (
    remove_repeated_dynamics as remove_repeated_dynamics_,
)


def reposition_dynamics(selection: abjad.Selection,
                        *,
                        allow_hairpins_under_rests: bool = False,
                        check_hairpin_trends: bool = True,
                        remove_repeated_dynamics: bool = True,
                        allow_hairpin_to_rest_with_dynamic: bool = True,
                        ):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function shifts all dynamics from rests to the next pitched leaves. It
    will also adjust hairpins if necessary.

    Basic usage:
        This function will shift dynamics under rests to the next pitched leaf.

        >>> staff = abjad.Staff(r"c'1\p d'2 r2\f r1 e'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'2
            r2
            \f
            r1
            e'1
        }

        .. figure:: ../_images/reposition_dynamics-sqwvevg7o9.png

        >>> staff = abjad.Staff(r"c'1\p d'2 r2\f r1 e'1")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'2
            r2
            r1
            e'1
            \f
        }

        .. figure:: ../_images/reposition_dynamics-v18uzh1zjs.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.mutate(staff[:]).reposition_dynamics()

    Removing dynamics:
        If the next pitched leaf already contain a dynamic, this function will
        simply remove the dynamic under the rest.

        >>> staff = abjad.Staff(r"c'1\p d'2 r2\f r1\mf e'1\pp")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'2
            r2
            \f
            r1
            \mf
            e'1
            \pp
        }

        .. figure:: ../_images/reposition_dynamics-aom2qywcn9m.png

        >>> staff = abjad.Staff(r"c'1\p d'2 r2\f r1\mf e'1\pp")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'2
            r2
            r1
            e'1
            \pp
        }

        .. figure:: ../_images/reposition_dynamics-2ua73x102fp.png

    ``remove_repeated_dynamics``:
        By default indentical repeated dynamics are omitted.

        >>> staff = abjad.Staff(r"c'1\p d'1 r1\f e'1\p")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'1
            r1
            e'1
        }

        .. figure:: ../_images/reposition_dynamics-i4x8b1z1ak.png

        Set the optional keyword argument ``remove_repeated_dynamics`` to
        ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"c'1\p d'1 r1\f e'1\p")
        >>> auxjad.mutate(staff[:]).reposition_dynamics(
        ...     remove_repeated_dynamics=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'1
            r1
            e'1
            \p
        }

        .. figure:: ../_images/reposition_dynamics-se8a5aeqer.png

    ``allow_hairpins_under_rests``:
        This function will shorten hairpins until rests by default.

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2 r1\f e'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            r1
            \f
            e'1
        }

        .. figure:: ../_images/reposition_dynamics-r28po3j3hd.png

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2 r1\f e'1")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            \!
            r1
            e'1
            \f
        }

        .. figure:: ../_images/reposition_dynamics-n60vvnqrcnr.png

        Set the optional keyword argument ``allow_hairpins_under_rests`` to
        ``True`` to allow hairpins to extend cross rests.

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2 r1\f e'1")
        >>> auxjad.mutate(staff[:]).reposition_dynamics(
        ...     allow_hairpins_under_rests=True,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            r1
            e'1
            \f
        }

        .. figure:: ../_images/reposition_dynamics-ugit7ijz89h.png

    ``allow_hairpin_to_rest_with_dynamic``:
        Notice that if a hairpin leads to a rest with dynamic, that one is not
        removed.

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            \f
            r1
            e'1
        }

        .. figure:: ../_images/reposition_dynamics-t9z4y5zzj6.png

        Set the argument ``allow_hairpin_to_rest_with_dynamic`` to ``False`` to
        disable this behaviour.

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
        >>> auxjad.mutate(staff[:]).reposition_dynamics(
        ...     allow_hairpin_to_rest_with_dynamic=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            \!
            r1
            e'1
            \f
        }

        .. figure:: ../_images/reposition_dynamics-wpwweov55qf.png

    ``check_hairpin_trends``:
        This function will remove any hairpins connecting dynamics that grow in
        the opposite direction to the hairpin's trend, such as a diminuendo
        hairpin from piano to forte.

        >>> staff = abjad.Staff(r"c'1\p\> d'1\f\> e'1\p")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'1
            \f
            \>
            e'1
            \p
        }

        .. figure:: ../_images/reposition_dynamics-f0b4ppb71ii.png

        This behaviour can be disabled by setting the argument
        ``check_hairpin_trends`` to ``False``.

        >>> staff = abjad.Staff(r"c'1\p\> d'1\f\> e'1\p")
        >>> auxjad.mutate(staff[:]).reposition_dynamics(
        ...     check_hairpin_trends=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \>
            d'1
            \f
            \>
            e'1
            \p
        }

        .. figure:: ../_images/reposition_dynamics-1e2ugszm95fi.png

    .. note::

        The behaviour described above is only applicable when a hairpin ends
        on a dynamic. Using the hairpin terminator ``\!`` before a dynamic
        change will not cause a hairpin to be removed as it is not considered
        to be connecting dynamics of the opposite trend.

        >>> staff = abjad.Staff(r"c'1\p\> d'1\! e'1\f\> f'1\p")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \>
            d'1
            \!
            e'1
            \f
            \>
            f'1
            \p
        }

        .. figure:: ../_images/reposition_dynamics-77g0uwthbgd.png

    Types of hairpins:
        This function can handle multiple types of hairpins as well as niente
        dynamics.

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 r1\mf r1\ff f'1 r1 g'1")
        >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[0])
        >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[7])
        >>> abjad.attach(abjad.StartHairpin('o<'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('>o'), staff[4])
        >>> abjad.attach(abjad.StopHairpin(), staff[7])
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            - \tweak circled-tip ##t
            \<
            d'1
            e'1
            r1
            \mf
            r1
            f'1
            \ff
            - \tweak circled-tip ##t
            \>
            r1
            \!
            g'1
        }

        .. figure:: ../_images/reposition_dynamics-m8it9awv1ce.png

        >>> staff = abjad.Staff(
        ...     r"c'1\p d'1\f\> e'1\ff\< r1\fff f'1\p\> g'1\ppp"
        ... )
        >>> abjad.attach(abjad.StartHairpin('--'), staff[0])
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            - \tweak stencil #constante-hairpin
            \<
            d'1
            \f
            e'1
            \ff
            \<
            r1
            \fff
            f'1
            \p
            \>
            g'1
            \ppp
        }

        .. figure:: ../_images/reposition_dynamics-fosad5ltzj.png

    Multi-measure rests:
        Multi-measure rests are also supported.

        >>> staff = abjad.Staff(r"c'1\p R1\f d'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            R1
            \f
            d'1
        }

        .. figure:: ../_images/reposition_dynamics-uj6jasfs2uh.png

        >>> staff = abjad.Staff(r"c'1\p R1\f d'1")
        >>> auxjad.mutate(staff[:]).reposition_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            R1
            d'1
            \f
        }

        .. figure:: ../_images/reposition_dynamics-axpcbm9hocd.png

    .. warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not abjad.select(selection).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    if not isinstance(allow_hairpins_under_rests, bool):
        raise TypeError("'allow_hairpins_under_rests' must be 'bool'")
    if not isinstance(check_hairpin_trends, bool):
        raise TypeError("'check_hairpin_trends' must be 'bool'")
    if not isinstance(remove_repeated_dynamics, bool):
        raise TypeError("'remove_repeated_dynamics' must be 'bool'")
    if not isinstance(allow_hairpin_to_rest_with_dynamic, bool):
        raise TypeError("'allow_hairpin_to_rest_with_dynamic' must be 'bool'")

    leaves = selection.leaves()

    # shifting dynamics and hairpins from rests to notes
    shifted_dynamic = None
    shifted_hairpin = None
    active_hairpin = None
    for leaf in leaves:
        inspector = abjad.inspect(leaf)
        if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
            if inspector.indicator(abjad.Dynamic) is not None:
                previous_leaf = abjad.select(leaf).with_previous_leaf()[0]
                if (allow_hairpin_to_rest_with_dynamic
                        and active_hairpin is not None
                        and not isinstance(
                            previous_leaf,
                            (abjad.Rest, abjad.MultimeasureRest),
                        )):
                    active_hairpin = None
                else:
                    shifted_dynamic = inspector.indicator(abjad.Dynamic)
                    abjad.detach(abjad.Dynamic, leaf)
            if inspector.indicator(abjad.StartHairpin) is not None:
                shifted_hairpin = inspector.indicator(abjad.StartHairpin)
                abjad.detach(abjad.StartHairpin, leaf)
        else:
            if inspector.indicator(abjad.Dynamic) is None:
                if shifted_dynamic is not None:
                    abjad.attach(shifted_dynamic, leaf)
                    if inspector.indicator(abjad.StopHairpin) is not None:
                        abjad.detach(abjad.StopHairpin, leaf)
                if shifted_hairpin is not None:
                    abjad.attach(shifted_hairpin, leaf)
            else:
                active_hairpin = None
            if inspector.indicator(abjad.StopHairpin) is not None:
                active_hairpin = None
            shifted_dynamic = None
            shifted_hairpin = None
            if active_hairpin is None:
                active_hairpin = inspector.indicator(abjad.StartHairpin)

    # stopping hairpins under rests if not allowed
    if not allow_hairpins_under_rests:
        effective_hairpin = None
        for leaf in leaves:
            inspector = abjad.inspect(leaf)
            start_hairpin = inspector.indicator(abjad.StartHairpin)
            if start_hairpin is not None:
                effective_hairpin = start_hairpin
                continue
            if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
                if effective_hairpin is not None:
                    if inspector.indicator(abjad.StopHairpin) is None:
                        abjad.attach(abjad.StopHairpin(), leaf)
                    effective_hairpin = None
            else:
                dynamic = inspector.indicator(abjad.Dynamic)
                stop_hairpin = inspector.indicator(abjad.StopHairpin)
                if dynamic is not None or stop_hairpin is not None:
                    effective_hairpin = None

    # cleaning up hairpins
    effective_dynamic = None
    for index, leaf in enumerate(leaves[:-1]):
        inspector = abjad.inspect(leaf)
        if inspector.indicator(abjad.Dynamic) is not None:
            effective_dynamic = inspector.indicator(abjad.Dynamic)
        start_hairpin = inspector.indicator(abjad.StartHairpin)
        if start_hairpin is not None and check_hairpin_trends:
            for next_leaf in leaves[index + 1:]:
                next_inspector = abjad.inspect(next_leaf)
                next_dynamic = next_inspector.indicator(abjad.Dynamic)
                if next_dynamic is not None and effective_dynamic is not None:
                    if '<' in start_hairpin.shape:
                        if next_dynamic.ordinal <= effective_dynamic.ordinal:
                            abjad.detach(abjad.StartHairpin, leaf)
                    elif '>' in start_hairpin.shape:
                        if next_dynamic.ordinal >= effective_dynamic.ordinal:
                            abjad.detach(abjad.StartHairpin, leaf)
                    break
                elif next_inspector.indicator(abjad.StopHairpin) is not None:
                    break
    if abjad.inspect(leaves[-1]).indicator(abjad.StartHairpin) is not None:
        abjad.detach(abjad.StartHairpin, leaves[-1])

    # removing unecessary StopHairpin's
    for leaf in leaves:
        inspector = abjad.inspect(leaf)
        if (inspector.indicator(abjad.StopHairpin) is not None
                and inspector.indicator(abjad.Dynamic) is not None):
            abjad.detach(abjad.StopHairpin, leaf)
    target_leaf = None
    for leaf in leaves[::-1]:
        inspector = abjad.inspect(leaf)
        if inspector.indicator(abjad.StopHairpin) is not None:
            if target_leaf is not None:
                abjad.detach(abjad.StopHairpin, target_leaf)
            target_leaf = leaf
        elif (inspector.indicator(abjad.StartHairpin) is not None
                or inspector.indicator(abjad.Dynamic)) is not None:
            target_leaf = None

    # removing repeated dynamics if required
    if remove_repeated_dynamics:
        remove_repeated_dynamics_(selection)
