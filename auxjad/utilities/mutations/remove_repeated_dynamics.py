import abjad


def remove_repeated_dynamics(selection: abjad.Selection,
                             *,
                             ignore_hairpins: bool = False,
                             reset_after_rests: bool = False,
                             ):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function removes all consecutive repeated dynamic markings.

    Basic usage:
        When two consecutive leaves have identical dynamics, the second
        one is removed:

        >>> staff = abjad.Staff(r"\time 3/8 c'4\pp d'8\pp | c'4\f d'8\f")
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            \pp
            d'8
            \pp
            c'4
            \f
            d'8
            \f
        }

        .. figure:: ../_images/remove_repeated_dynamics-anw32e9i0f.png

        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            \pp
            d'8
            c'4
            \f
            d'8
        }

        .. figure:: ../_images/remove_repeated_dynamics-i5ylxkzv7md.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics()
        >>> abjad.mutate(staff[:]).remove_repeated_dynamics()

    Dynamic structure:
        The function also removes dynamics that are separated by an arbitrary
        number of leaves without dynamics:

        >>> staff = abjad.Staff(r"\time 3/8 c'4\p d'8 | e'4.\p | c'4\p d'8\f")
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            \p
            d'8
            e'4.
            \p
            c'4
            \p
            d'8
            \f
        }

        .. figure:: ../_images/remove_repeated_dynamics-ha1x7s8d2fb.png

        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            \p
            d'8
            e'4.
            c'4
            d'8
            \f
        }

        .. figure:: ../_images/remove_repeated_dynamics-g157jbbojhv.png

    Subcontainers:
        The container from which the selection is made can also have
        subcontainers:

        >>> staff = abjad.Staff([abjad.Note("c'2"),
        ...                      abjad.Chord("<d' f'>2"),
        ...                      abjad.Tuplet((2, 3), "g2 a2 b2"),
        ...                      ])
        >>> abjad.attach(abjad.Dynamic('ppp'), staff[0])
        >>> abjad.attach(abjad.Dynamic('ppp'), staff[1])
        >>> abjad.attach(abjad.Dynamic('ppp'), staff[2][0])
        >>> abjad.f(staff)
        \new Staff
        {
            c'2
            \ppp
            <d' f'>2
            \ppp
            \times 2/3 {
                g2
                \ppp
                a2
                b2
            }
        }

        .. figure:: ../_images/remove_repeated_dynamics-4h9xze4780d.png

        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'2
            \ppp
            <d' f'>2
            \times 2/3 {
                g2
                a2
                b2
            }
        }

        .. figure:: ../_images/remove_repeated_dynamics-7n9aaveoslu.png

    ``ignore_hairpins``:
        By default, repeated dynamics with hairpins in between are not removed,
        but consecutive ones will.

        >>> staff = abjad.Staff(r"c'2\p\< d'2\f\> | c'2\f d'2\f | e'1\p")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'1
            \f
            \>
            c'1
            \f
            d'1
            \f
            e'1
            \p
        }

        .. figure:: ../_images/remove_repeated_dynamics-frmlobo3gis.png

        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'1
            \f
            \>
            c'1
            \f
            d'1
            e'1
            \p
        }

        .. figure:: ../_images/remove_repeated_dynamics-ov05k1imubj.png

        To override the previous behaviour, set ``ignore_hairpins=True`` and
        hairpins will be ignored.

        >>> staff = abjad.Staff(r"c'2\p\< d'2\f\> | c'2\f d'2\f | e'1\p")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'1
            \f
            \>
            c'1
            \f
            d'1
            \f
            e'1
            \p
        }

        .. figure:: ../_images/remove_repeated_dynamics-2hdkt6cyca1.png

        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics(
        ...     ignore_hairpins=True,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \p
            \<
            d'1
            \f
            \>
            c'1
            d'1
            e'1
            \p
        }

        .. figure:: ../_images/remove_repeated_dynamics-xkaipizr2jr.png

    ``reset_after_rests``:
        By default, rests are treated just like any other leaf and thus notes
        with an identical dynamic separated by an arbitrary number of rests
        will be considered as repeated and the second dynamic will be removed.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
        }

        .. figure:: ../_images/remove_repeated_dynamics-wtno2t8qroh.png

        To override the previous behaviour, set ``reset_after_rests=True`` and
        dynamics will always be restated after a rest.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics(
        ...     reset_after_rests=True,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
            \pp
        }

        .. figure:: ../_images/remove_repeated_dynamics-3e6g7u0q1i1.png

    ``reset_after_rests`` and non-:obj:`bool` values:
        The argument ``reset_after_rests`` takes not only :obj:`bool` values
        but also durations (|abjad.Duration|, :obj:`tuple`, :obj:`float`,
        etc.). This sets the maximum length of rests before which identical
        dynamics are restated. If the total length of rests falls below that
        value, then repeated dynamics are removed.

        In the case below, a rest of ``r2``. is shorter than a duration of
        ``(4, 4)``, so the repeated dynamic is removed.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics(
        ...     reset_after_rests=(4, 4)
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
        }

        .. figure:: ../_images/remove_repeated_dynamics-b323xuesujc.png

        But setting the duration to ``2/4`` forces the dynamic to be restated.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics(
        ...     reset_after_rests=2 / 4
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
            \pp
        }

        .. figure:: ../_images/remove_repeated_dynamics-64dppx3cp99.png

    ``reset_after_rests``:
        The function also handles measure rests with ``reset_after_rests``.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp r2. | R1 | c'1\pp")
        >>> auxjad.mutate(staff[:]).remove_repeated_dynamics(
        ...     reset_after_rests=abjad.Duration(4, 4)
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
            r2.
            R1
            c'1
            \pp
        }

        .. figure:: ../_images/remove_repeated_dynamics-jt7akhtbsge.png

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
    if not isinstance(ignore_hairpins, bool):
        raise TypeError("'ignore_hairpins' must be 'bool'")
    if not isinstance(reset_after_rests,
                      (bool, int, float, tuple, str, abjad.Duration),
                      ):
        raise TypeError("'reset_after_rests' must be a number, 'bool' or "
                        "'abjad.Duration'")

    previous_dynamic = None
    current_dynamic = None
    duration_since_last_note = abjad.Duration(0)
    for leaf in selection.leaves():
        if type(leaf) in (abjad.Rest, abjad.MultimeasureRest):
            if isinstance(reset_after_rests, bool) and reset_after_rests:
                previous_dynamic = None
            elif reset_after_rests:
                duration_since_last_note += leaf.written_duration
                if (duration_since_last_note
                        >= abjad.Duration(reset_after_rests)):
                    previous_dynamic = None
        else:
            duration_since_last_note = abjad.Duration(0)
            indicators = abjad.inspect(leaf).indicators()
            hairpin_present = any([isinstance(indicator, abjad.StartHairpin)
                                   for indicator in indicators])
            for indicator in indicators:
                if isinstance(indicator, abjad.Dynamic):
                    if hairpin_present and not ignore_hairpins:
                        if (indicator is not None
                                and indicator == previous_dynamic):
                            abjad.detach(abjad.Dynamic, leaf)
                        current_dynamic = None
                    else:
                        current_dynamic = indicator
            if current_dynamic != previous_dynamic:
                previous_dynamic = current_dynamic
            elif current_dynamic is not None:
                abjad.detach(abjad.Dynamic, leaf)
