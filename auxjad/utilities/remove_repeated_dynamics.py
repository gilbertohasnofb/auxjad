import abjad


def remove_repeated_dynamics(container: abjad.Container,
                             *,
                             ignore_hairpins: bool = False,
                             reset_after_rests: bool = False,
                             ):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value. This function removes all consecutive
    repeated dynamic markings.

    ..  container:: example

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

        .. figure:: ../_images/image-remove_repeated_dynamics-1.png

        >>> auxjad.remove_repeated_dynamics(staff)
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

        .. figure:: ../_images/image-remove_repeated_dynamics-2.png

    ..  container:: example

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

        .. figure:: ../_images/image-remove_repeated_dynamics-3.png

        >>> auxjad.remove_repeated_dynamics(staff)
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

        .. figure:: ../_images/image-remove_repeated_dynamics-4.png

    ..  container:: example

        The input container can also handle subcontainers:

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

        .. figure:: ../_images/image-remove_repeated_dynamics-5.png

        >>> auxjad.remove_repeated_dynamics(staff)
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

        .. figure:: ../_images/image-remove_repeated_dynamics-6.png

    ..  container:: example

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

        .. figure:: ../_images/image-remove_repeated_dynamics-7.png

        >>> auxjad.remove_repeated_dynamics(staff)
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

        .. figure:: ../_images/image-remove_repeated_dynamics-8.png

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

        .. figure:: ../_images/image-remove_repeated_dynamics-9.png

        >>> auxjad.remove_repeated_dynamics(staff, ignore_hairpins=True)
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

        .. figure:: ../_images/image-remove_repeated_dynamics-10.png

    ..  container:: example

        By default, rests are treated just like any other leaf and thus notes
        with an identical dynamic separated by an arbitrary number of rests
        will be considered as repeated and the second dynamic will be removed.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> auxjad.remove_repeated_dynamics(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
        }

        .. figure:: ../_images/image-remove_repeated_dynamics-11.png

        To override the previous behaviour, set ``reset_after_rests=True`` and
        dynamics will always be restated after a rest.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> auxjad.remove_repeated_dynamics(staff, reset_after_rests=True)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
            \pp
        }

        .. figure:: ../_images/image-remove_repeated_dynamics-12.png

    ..  container:: example

        The argument ``reset_after_rests`` takes not only boolean values but
        also duration (``abjad.Duration``, tuple, float, etc.). This sets the
        maximum length of rests before which identical dynamics are restated.
        If the total length of rests falls below that value, then repeated
        dynamics are removed.

        In the case below, a rest of ``r2``. is shorter than a duration of
        (4, 4), so the repeated dynamic is removed.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> auxjad.remove_repeated_dynamics(staff, reset_after_rests=(4, 4))
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
        }

        .. figure:: ../_images/image-remove_repeated_dynamics-13.png

        But setting the duration to 2/4 forces the dynamic to be restated.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> auxjad.remove_repeated_dynamics(staff, reset_after_rests=2/4)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
            \pp
        }

        .. figure:: ../_images/image-remove_repeated_dynamics-14.png

    ..  container:: example

        The function also handles measure rests with ``reset_after_rests``.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp r2. |R1 | c'4\pp")
        >>> auxjad.remove_repeated_dynamics(
        ...     staff,
        ...     reset_after_rests=abjad.Duration(4, 4),
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
            c'4
            \pp
        }

        .. figure:: ../_images/image-remove_repeated_dynamics-15.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not isinstance(ignore_hairpins, bool):
        raise TypeError("'ignore_hairpins' must be 'bool'")
    if not isinstance(reset_after_rests,
                      (bool, int, float, tuple, str, abjad.Duration),
                      ):
        raise TypeError("'reset_after_rests' must be a number, 'bool' or "
                        "'abjad.Duration'")

    leaves = [leaf for leaf in abjad.select(container).leaves()]

    previous_dynamic = None
    duration_since_last_note = abjad.Duration(0)
    for leaf in leaves:
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
                        current_dynamic = None
                    else:
                        current_dynamic = indicator
            if current_dynamic != previous_dynamic:
                previous_dynamic = current_dynamic
            elif current_dynamic is not None:
                abjad.detach(abjad.Dynamic, leaf)
