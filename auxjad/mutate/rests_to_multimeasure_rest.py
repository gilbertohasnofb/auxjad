import abjad


def rests_to_multimeasure_rest(selection: abjad.Selection,
                               *,
                               ignore_clefs: bool = False,
                               ignore_dynamics: bool = False,
                               ) -> None:
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function looks for measures filled with regular rests and converts
    them into an |abjad.MultimeasureRest|.

    Basic usage:
        Converts any measure filled with regular rests into a measure with a
        single multi-measure rest.

        >>> container = abjad.Container(r"\time 3/4 r2.")
        >>> abjad.show(container)

        ..  docs::

            {
                \time 3/4
                r2.
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-VIj5iWyLCG.png

        >>> auxjad.mutate.rests_to_multimeasure_rest(container[:])
        >>> abjad.show(container)

        ..  docs::

            {
                \time 3/4
                R1 * 3/4
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-uvebc7ft1zo.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.rests_to_multimeasure_rest(staff[:])
        >>> abjad.mutate.rests_to_multimeasure_rest(staff[:])

    Multiple rests:
        Works with measures with multiple regular rests.

        >>> container = abjad.Container(r"r2 r8.. r32 r16 r8 r16")
        >>> abjad.show(container)

        ..  docs::

            {
                r2
                r8..
                r32
                r16
                r8
                r16
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-jk4m1wzsyfa.png

        >>> auxjad.mutate.rests_to_multimeasure_rest(container[:])
        >>> abjad.show(container)

        ..  docs::

            {
                R1
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-z8u0cs3fzdi.png

    ..  note::

        When using |abjad.Container|'s, all time signatures in the output will
        be commented out with ``%%%.`` This is because Abjad only applies time
        signatures to containers that belong to a |abjad.Staff|. The present
        function works with either |abjad.Container| and |abjad.Staff|.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> abjad.show(container)

        ..  docs::

            {
                %%% \time 3/4 %%%
                c'4
                d'4
                e'4
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-qtq55xbkkts.png

        >>> staff = abjad.Staff([container])
        >>> abjad.show(container)

        ..  docs::

            {
                \time 3/4
                c'4
                d'4
                e'4
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-9hceg93vrmv.png

    Time signature changes:
        Works with selections from containers with multiple time signatures as
        well as notes.

        >>> container = abjad.Staff(
        ...     r"\time 3/4 r2. | "
        ...     "\time 6/8 r2. | "
        ...     "\time 5/4 c'1 ~ c'4 | r1 r4"
        ... )
        >>> abjad.show(container)

        ..  docs::

            \new Staff
            {
                \time 3/4
                r2.
                \time 6/8
                r2.
                \time 5/4
                c'1
                ~
                c'4
                r1
                r4
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-oQfFRihzEY.png

        >>> auxjad.mutate.rests_to_multimeasure_rest(container[:])
        >>> abjad.show(container)

        ..  docs::

            \new Staff
            {
                \time 3/4
                R1 * 3/4
                \time 6/8
                R1 * 3/4
                \time 5/4
                c'1
                ~
                c'4
                R1 * 5/4
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-a9sqdcznoq.png

    Tuplets:
        Works with containers with tuplets.

        >>> container = abjad.Container(r"\times 2/3 {r2 r2 r2}")
        >>> abjad.show(container)

        ..  docs::

            {
                \times 2/3
                {
                    r2
                    r2
                    r2
                }
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-480a9zqvk2a.png

        >>> auxjad.mutate.rests_to_multimeasure_rest(container[:])
        >>> abjad.show(container)

        ..  docs::

            {
                R1
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-r5yg3a3f97q.png

        It also works with containers with tuplets within tuplets.

        >>> container = abjad.Container(
        ...     r"r2 \times 2/3 {r2 r4} \times 4/5 {r2. \times 2/3 {r2 r4}}"
        ... )
        >>> abjad.show(container)

        ..  docs::

            {
                r2
                \times 2/3
                {
                    r2
                    r4
                }
                \times 4/5
                {
                    r2.
                    \times 2/3
                    {
                        r2
                        r4
                    }
                }
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-codydc205jw.png

        >>> auxjad.mutate.rests_to_multimeasure_rest(container[:])
        >>> abjad.show(container)

        ..  docs::

            {
                R1
                R1
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-f647t5j3jgw.png

    ``ignore_clefs``
        By default, the last clef of an empty measure is preserved when
        replacing it with a multi-measure rest:

        >>> staff = abjad.Staff(
        ...     r"\clef bass r4 r4 \times 2/3 {r4 r8} r4 "
        ...     r"\time 3/4 \clef treble r2. "
        ...     r"\time 5/4 r2 \clef bass r2."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \clef "bass"
                r4
                r4
                \times 2/3
                {
                    r4
                    r8
                }
                r4
                \time 3/4
                \clef "treble"
                r2.
                \time 5/4
                r2
                \clef "bass"
                r2.
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-6GMRGmYkEQ.png

        >>> abjad.mutate.rests_to_multimeasure_rest(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \clef "bass"
                R1
                \time 3/4
                \clef "treble"
                R1 * 3/4
                \time 5/4
                \clef "bass"
                R1 * 5/4
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-UnL6ZoFoDC.png

        Invoke the mutation with ``ignore_clefs`` set to ``True`` to disable
        this behaviour and ignore all clefs:

        >>> staff = abjad.Staff(
        ...     r"\clef bass r4 r4 \times 2/3 {r4 r8} r4 "
        ...     r"\time 3/4 \clef treble r2. "
        ...     r"\time 5/4 r2 \clef bass r2."
        ... )
        >>> abjad.mutate.rests_to_multimeasure_rest(
        ...     staff[:],
        ...     ignore_clefs=True,
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                R1
                \time 3/4
                R1 * 3/4
                \time 5/4
                R1 * 5/4
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-KGRZJ8fvQF.png

    ``ignore_dynamics``
        By default, the last dynamic or hairpin of an empty measure is
        preserved when replacing it with a multi-measure rest:

        >>> staff = abjad.Staff(r"c'1\p\< r2\! r2 d'1\f\> r2 r2\ppp")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                \p
                \<
                r2
                \!
                r2
                d'1
                \f
                \>
                r2
                r2
                \ppp
            }


        ..  figure:: ../_images/rests_to_multimeasure_rest-J9T5UY8r9w.png

        >>> abjad.mutate.rests_to_multimeasure_rest(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                \p
                \<
                R1
                \!
                d'1
                \f
                \>
                R1
                \ppp
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-77r9QeaZBA.png

        Invoke the mutation with ``ignore_dynamics`` set to ``True`` to disable
        this behaviour and ignore all dynamics and hairpins:

        >>> staff = abjad.Staff(r"c'1\p\< r2\! r2 d'1\f\> r2 r2\ppp")
        >>> abjad.mutate.rests_to_multimeasure_rest(
        ...     staff[:],
        ...     ignore_dynamics=True,
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'1
                \p
                \<
                R1
                d'1
                \f
                \>
                R1
            }

        ..  figure:: ../_images/rests_to_multimeasure_rest-3UhZukx9Pw.png

        ..  warning::

            Note that dynamics are only ignored when converting rests to
            multi-measure rests. All other dynamics are preserved in the score.
            This can result in problems displaying dynamics when one or more
            unterminated hairpins is present. In the example above, the last
            note's hairpin is unterminated and, because of that, LilyPond
            ignores all dynamics in that staff:

            >>> staff = abjad.Staff(r"c'1\p\< r2\! r2 d'1\f\> r2 r2\ppp")
            >>> abjad.mutate.rests_to_multimeasure_rest(
            ...     staff[:],
            ...     ignore_dynamics=True,
            ... )
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'1
                \p
                \<
                R1
                d'1
                \f
                \>
                R1
            }

    ..  warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    if not isinstance(ignore_clefs, bool):
        raise TypeError("'ignore_clefs' must be 'bool'")
    if not isinstance(ignore_dynamics, bool):
        raise TypeError("'ignore_dynamics' must be 'bool'")

    measures = selection.group_by_measure()
    effective_time_signature = abjad.TimeSignature((4, 4))
    indicators_tuple = (abjad.BarLine,
                        abjad.Fermata,
                        abjad.KeySignature,
                        abjad.LilyPondLiteral,
                        abjad.MetronomeMark,
                        abjad.RehearsalMark,
                        abjad.Repeat,
                        abjad.StaffChange,
                        abjad.StartMarkup,
                        abjad.StartTextSpan,
                        abjad.StopTextSpan,
                        )

    for measure in measures:
        head = abjad.select(measure).leaf(0)
        time_signature = abjad.get.indicator(head, abjad.TimeSignature)
        if time_signature is not None:
            effective_time_signature = time_signature
        if all([isinstance(leaf, abjad.Rest) for leaf in measure.leaves()]):
            if not ignore_clefs:
                for leaf in measure.leaves()[::-1]:
                    clef = abjad.get.indicator(leaf, abjad.Clef)
                    if clef is not None:
                        break
            if not ignore_dynamics:
                for leaf in measure.leaves()[::-1]:
                    dynamics = abjad.get.indicator(leaf, (abjad.Dynamic,
                                                          abjad.StartHairpin,
                                                          abjad.StopHairpin,
                                                          ))
                    if dynamics is not None:
                        break
            duration = abjad.get.duration(measure)
            if duration == effective_time_signature.duration:
                if duration == 1:
                    multiplier = None
                else:
                    multiplier = abjad.Multiplier(duration)
                multimeasure_rest = abjad.MultimeasureRest(
                    (4, 4),
                    multiplier=multiplier,
                )
                if time_signature is not None:
                    abjad.attach(time_signature, multimeasure_rest)
                if not ignore_clefs and clef is not None:
                    abjad.attach(clef, multimeasure_rest)
                if not ignore_dynamics and dynamics is not None:
                    abjad.attach(dynamics, multimeasure_rest)
                for indicator in abjad.get.indicators(head):
                    if isinstance(indicator, indicators_tuple):
                        abjad.attach(indicator, multimeasure_rest)
                abjad.mutate.replace(measure, multimeasure_rest)
