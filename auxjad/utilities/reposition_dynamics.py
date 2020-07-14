import abjad

from .remove_repeated_dynamics import (
    remove_repeated_dynamics as remove_repeated_dynamics_,
)


def reposition_dynamics(container: abjad.Container,
                        *,
                        allow_hairpins_under_rests: bool = False,
                        check_hairpin_trends: bool = True,
                        remove_repeated_dynamics: bool = True,
                        allow_rests_with_dynamics_after_hairpins: bool = True,
                        ):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function shifts all dynamics from
    rests to the next pitched leaves. It will also adjust hairpins if
    necessary.

    Example:
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

        .. figure:: ../_images/image-reposition_dynamics-1.png

        >>> staff = abjad.Staff(r"c'1\p d'2 r2\f r1 e'1")
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-2.png

    Example:
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

        .. figure:: ../_images/image-reposition_dynamics-3.png

        >>> staff = abjad.Staff(r"c'1\p d'2 r2\f r1\mf e'1\pp")
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-4.png

    Example:
        By default indentical repeated dynamics are omitted.

        >>> staff = abjad.Staff(r"c'1\p d'1 r1\f e'1\p")
        >>> auxjad.reposition_dynamics(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            d'1
            r1
            e'1
        }

        .. figure:: ../_images/image-reposition_dynamics-5.png

        Set the optional keyword argument ``remove_repeated_dynamics`` to
        ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"c'1\p d'1 r1\f e'1\p")
        >>> auxjad.reposition_dynamics(staff, remove_repeated_dynamics=False)
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

        .. figure:: ../_images/image-reposition_dynamics-6.png

    Example:
        This function will shorten hairpins until rests by default

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

        .. figure:: ../_images/image-reposition_dynamics-7.png

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-8.png

        Set the optional keyword argument ``allow_hairpins_under_rests`` to
        ``True`` to allow hairpins to extend cross rests.

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
        >>> auxjad.reposition_dynamics(staff, allow_hairpins_under_rests=True)
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

        .. figure:: ../_images/image-reposition_dynamics-9.png

    Example:
        Notice that if a hairpin leads to a rest with dynamic, that one is not
        removed.

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-10.png

        Set the argument ``allow_rests_with_dynamics_after_hairpins`` to
        ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
        >>> auxjad.reposition_dynamics(
        ...     staff,
        ...     allow_rests_with_dynamics_after_hairpins=False,
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

        .. figure:: ../_images/image-reposition_dynamics-11.png

    Example:
        This function will remove any hairpins connecting dynamics that grow in
        the opposite direction to the hairpin's trend, such as a diminuendo
        hairpin from piano to forte.

        >>> staff = abjad.Staff(r"c'1\p\> d'1\f\> e'1\p")
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-12.png

        This behaviour can be disabled by setting the argument
        ``check_hairpin_trends`` to ``False``.

        >>> staff = abjad.Staff(r"c'1\p\> d'1\f\> e'1\p")
        >>> auxjad.reposition_dynamics(staff, check_hairpin_trends=False)
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

        .. figure:: ../_images/image-reposition_dynamics-13.png

    ..  note::

        The behaviour described above is only applicable when a hairpin ends
        on a dynamic. Using the hairpin terminator ``\!`` before a dynamic
        change will not cause a hairpin to be removed as it is not considered
        to be connecting dynamics of the opposite trend.

        >>> staff = abjad.Staff(r"c'1\p\> d'1\! e'1\f\> f'1\p")
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-14.png

    Example:
        This function can handle multiple types of hairpins as well as niente
        dynamics.

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 r1\mf r1\ff f'1 r1 g'1")
        >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[0])
        >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[7])
        >>> abjad.attach(abjad.StartHairpin('o<'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('>o'), staff[4])
        >>> abjad.attach(abjad.StopHairpin(), staff[7])
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-15.png

        >>> staff = abjad.Staff(
        ...     r"c'1\p d'1\f\> e'1\ff\< r1\fff f'1\p\> g'1\ppp")
        >>> abjad.attach(abjad.StartHairpin('--'), staff[0])
        >>> auxjad.reposition_dynamics(staff)
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

        .. figure:: ../_images/image-reposition_dynamics-16.png

    Example:
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

        .. figure:: ../_images/image-reposition_dynamics-17.png

        >>> staff = abjad.Staff(r"c'1\p R1\f d'1")
        >>> auxjad.reposition_dynamics(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            R1
            d'1
            \f
        }

        .. figure:: ../_images/image-reposition_dynamics-18.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not isinstance(allow_hairpins_under_rests, bool):
        raise TypeError("'allow_hairpins_under_rests' must be 'bool'")
    if not isinstance(check_hairpin_trends, bool):
        raise TypeError("'check_hairpin_trends' must be 'bool'")
    if not isinstance(remove_repeated_dynamics, bool):
        raise TypeError("'remove_repeated_dynamics' must be 'bool'")

    leaves = abjad.select(container[:]).leaves()

    # shifting dynamics and hairpins from rests to notes
    shifted_dynamic = None
    shifted_hairpin = None
    active_hairpin = None
    for leaf in leaves:
        inspector = abjad.inspect(leaf)
        if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
            if inspector.indicator(abjad.Dynamic) is not None:
                previous_leaf = abjad.select(leaf).with_previous_leaf()[0]
                if (allow_rests_with_dynamics_after_hairpins
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
                if next_inspector.indicator(abjad.Dynamic) is not None:
                    next_dynamic = next_inspector.indicator(abjad.Dynamic)
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
        remove_repeated_dynamics_(container, ignore_hairpins=True)
