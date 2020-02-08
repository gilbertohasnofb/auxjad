import abjad


def remove_repeated_dynamics(container: abjad.Container,
                             *,
                             ignore_hairpins: bool = False,
                             reset_after_rests: bool = False,
                             ) -> abjad.Container:
    r"""A function which removes all consecutive repeated dynamics. It removes
    consecutive effective dynamics, even if separated by any number of
    notes without one. It resets its memory of what was the previous dynamic
    every time it finds a hairpin, since notation such as "c'4\f\> c'4\f\>" is
    quite common; this behaviour can be toggled off using the ignore_hairpins
    keyword. By default, it remembers the previous dynamic even with notes
    separated by rests; this can be toggled off using reset_after_rests=True.
    To set a maximum length of silence after which dynamics are restated, set
    reset_after_rests to a duration using abjad.Duration() or any other
    duration format accepted by Abjad.

    ..  container:: example

        When two consecutive leaves have identical dynamics, the second
        one is removed:

        >>> staff = abjad.Staff(r"c'4\pp d'8\pp | c'4\f d'8\f")
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            d'8
            \pp
            c'4
            \f
            d'8
            \f
        }
        >>> staff = auxjad.remove_repeated_dynamics(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            d'8
            c'4
            \f
            d'8
        }

    ..  container:: example

        The function also removes dynamics that are separated by an arbitrary
        number of leaves without dynamics:

        >>> staff = abjad.Staff(r"c'4\p d'8 | e'4.\p | c'4\p d'8\f")
        >>> abjad.f(staff)
        \new Staff
        {
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
        >>> staff = auxjad.remove_repeated_dynamics(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \p
            d'8
            e'4.
            c'4
            d'8
            \f
        }

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
        >>> staff = auxjad.remove_repeated_dynamics(staff)
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

    ..  container:: example

        By default, repeated dynamics with hairpins in between are not removed,
        but consecutive ones will.

        >>> staff = abjad.Staff(r"c'4\pp\< d'8\f\> | c'4\f d'8\f")
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            \f
            d'8
            \f
        }
        >>> staff = auxjad.remove_repeated_dynamics(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            \f
            d'8
        }

        To override the previous behaviour, set ignore_hairpins to True and
        hairpins will be ignored.

        >>> staff = abjad.Staff(r"c'4\pp\< d'8\f\> | c'4\f d'8\f")
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            \f
            d'8
            \f
        }
        >>> staff = auxjad.remove_repeated_dynamics(staff,
        ...                                         ignore_hairpins=True,
        ...                                         )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            d'8
        }

    ..  container:: example

        By default, rests are treated just like any other leaf and thus notes
        with an identical dynamic separated by an arbitrary number of rests
        will be considered as repeated and the second dynamic will be removed.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> staff = auxjad.remove_repeated_dynamics(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
        }

        To override the previous behaviour, set reset_after_rests to True and
        dynamics will always be restated after a rest.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> staff = auxjad.remove_repeated_dynamics(staff,
        ...                                         reset_after_rests=True,
        ...                                         )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
            \pp
        }

    ..  container:: example

        The argument reset_after_rests takes not only boolean values but also
        duration (abjad.Duration, tuple, float, etc.). This sets the maximum
        length of rests before which identical dynamics are restated. If the
        total length of rests falls below that value, then repeated dynamics
        are removed.

        In the case below, a rest of r2. is shorter than a duration of (4, 4),
        so the repeated dynamic is removed.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> staff = auxjad.remove_repeated_dynamics(staff,
        ...                                         reset_after_rests=(4, 4),
        ...                                         )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
        }

        But setting the duration to 2/4 forces the dynamic to be restated.

        >>> staff = abjad.Staff(r"c'4\pp r2. | c'4\pp")
        >>> staff = auxjad.remove_repeated_dynamics(staff,
        ...                                         reset_after_rests=2/4,
        ...                                         )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            c'4
            \pp
        }

    ..  container:: example

        The function also handles measure rests with reset_after_rests.

        >>> staff = abjad.Staff(r"c'4\pp r2. | R1 | c'4\pp")
        >>> staff = auxjad.remove_repeated_dynamics(
        ...     staff,
        ...     reset_after_rests=abjad.Duration(4, 4),
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            r2.
            R1
            c'4
            \pp
        }

    """
    if not isinstance(container, abjad.Container):
        raise TypeError("'container' must be 'abjad.Container' or child class")
    if not isinstance(ignore_hairpins, bool):
        raise TypeError("'ignore_hairpins' must be 'bool'")
    if not isinstance(reset_after_rests,
                      (bool, int, float, tuple, str, abjad.Duration),
                      ):
        raise TypeError("'reset_after_rests' must be 'bool' or duration")

    leaves = [leaf for leaf in abjad.select(container).leaves()]

    previous_dynamic = None
    duration_since_last_note = abjad.Duration(0)
    for leaf in leaves:
        if type(leaf) in (abjad.Rest, abjad.MultimeasureRest):
            if reset_after_rests is True:
                previous_dynamic = None
            elif reset_after_rests:
                duration_since_last_note += leaf.written_duration
                if duration_since_last_note >= \
                        abjad.Duration(reset_after_rests):
                    previous_dynamic = None
        else:
            duration_since_last_note = abjad.Duration(0)
            indicators = abjad.inspect(leaf).indicators()
            hairpin_present = any([type(indicator) == abjad.StartHairpin for
                                   indicator in indicators])
            for indicator in indicators:
                if type(indicator) == abjad.Dynamic:
                    if hairpin_present and not ignore_hairpins:
                        current_dynamic = None
                    else:
                        current_dynamic = indicator
            if current_dynamic != previous_dynamic:
                previous_dynamic = current_dynamic
            elif current_dynamic is not None:
                abjad.detach(abjad.Dynamic, leaf)

    return container
