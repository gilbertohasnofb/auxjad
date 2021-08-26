import abjad


def merge_hairpins(selection: abjad.Selection) -> None:
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function merges all consecutive hairpins that share a same trend.

    Basic usage:
        Merging crescendo hairpins:

        >>> staff = abjad.Staff(r"c'4\pp\< d'4 e'4\p\< f'4 g'1\mp")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \pp
                \<
                d'4
                e'4
                \p
                \<
                f'4
                g'1
                \mp
            }

        ..  figure:: ../_images/merge_hairpins-b4it6YReZ9.png

        >>> abjad.mutate.merge_hairpins(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \pp
                \<
                d'4
                e'4
                f'4
                g'1
                \mp
            }

        ..  figure:: ../_images/merge_hairpins-s5cU8PINVO.png

        Merging diminuendo hairpins:

        >>> staff = abjad.Staff(r"c'4\ff\> d'4 e'4\mf\> f'4 g'1\pp")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \ff
                \>
                d'4
                e'4
                \mf
                \>
                f'4
                g'1
                \pp
            }

        ..  figure:: ../_images/merge_hairpins-GUIqXKDXaQ.png

        >>> abjad.mutate.merge_hairpins(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \ff
                \>
                d'4
                e'4
                f'4
                g'1
                \pp
            }

        ..  figure:: ../_images/merge_hairpins-adbT777qMg.png

        The merge only occurs when hairpins share a trend:

        >>> staff = abjad.Staff(r"c'4\pp\< d'4 e'4\p\> f'4 g'1\pp")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \pp
                \<
                d'4
                e'4
                \p
                \>
                f'4
                g'1
                \pp
            }

        ..  figure:: ../_images/merge_hairpins-Lvzn2f6PU6.png

        >>> abjad.mutate.merge_hairpins(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \pp
                \<
                d'4
                e'4
                \p
                \>
                f'4
                g'1
                \pp
            }

        ..  figure:: ../_images/merge_hairpins-EJdWJwkUJE.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate(staff[:]).merge_hairpins()
        >>> abjad.mutate(staff[:]).merge_hairpins()

    Gaps:
        If there are any gaps between hairpins (i.e. they finish on an earlier
        leaf than the start of the new hairpin), they will not be merged even
        if they share a trend.

        >>> staff = abjad.Staff(
        ...     r"c'1\pp\< d'2\f d'2\< e'1\ff f'1\f\> "
        ...     r"g'2\mp g'2\> a'1\! b'1\ppp"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                \pp
                \<
                d'2
                \f
                d'2
                \<
                e'1
                \ff
                f'1
                \f
                \>
                g'2
                \mp
                g'2
                \>
                a'1
                \!
                b'1
                \ppp
            }

        ..  figure:: ../_images/merge_hairpins-3Bo4GAfHaX.png

        >>> auxjad.mutate.merge_hairpins(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                \pp
                \<
                d'2
                \f
                d'2
                \<
                e'1
                \ff
                f'1
                \f
                \>
                g'2
                \mp
                g'2
                \>
                a'1
                \!
                b'1
                \ppp
            }

        ..  figure:: ../_images/merge_hairpins-HaF1ZUdqtx.png

    Multiple merges:
        This function can merge an indefinite number of hairpins:

        >>> staff = abjad.Staff(
        ...     r"c'4\pp\< d'4 e'4\p\< f'4 g'4\mp\< a'4 b'4\mf\< c''4"
        ...     r"d''4\f\> c''4 b'4\mf\> a'4 g'4\mp\> f'4 e'4\p\> d'4"
        ...     r"c'1\pp"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \pp
                \<
                d'4
                e'4
                \p
                \<
                f'4
                g'4
                \mp
                \<
                a'4
                b'4
                \mf
                \<
                c''4
                d''4
                \f
                \>
                c''4
                b'4
                \mf
                \>
                a'4
                g'4
                \mp
                \>
                f'4
                e'4
                \p
                \>
                d'4
                c'1
                \pp
            }

        ..  figure:: ../_images/merge_hairpins-DrT5XyaGWQ.png

        >>> auxjad.mutate.merge_hairpins(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \pp
                \<
                d'4
                e'4
                f'4
                g'4
                a'4
                b'4
                c''4
                d''4
                \f
                \>
                c''4
                b'4
                a'4
                g'4
                f'4
                e'4
                d'4
                c'1
                \pp
            }

        ..  figure:: ../_images/merge_hairpins-Z2yDxl8dlI.png
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    active_hairpin = None
    for leaf in selection.leaves():
        leaf_hairpin = abjad.get.indicator(leaf, abjad.StartHairpin)
        if active_hairpin is not None and leaf_hairpin is not None:
            if active_hairpin.shape == leaf_hairpin.shape:
                abjad.detach(abjad.StartHairpin, leaf)
                if abjad.get.indicator(leaf, abjad.Dynamic) is not None:
                    abjad.detach(abjad.Dynamic, leaf)
        if (abjad.get.indicator(leaf, abjad.Dynamic) is not None
                or abjad.get.indicator(leaf, abjad.StopHairpin) is not None):
            if leaf_hairpin is None:
                active_hairpin = None
        if leaf_hairpin is not None:
            active_hairpin = leaf_hairpin
