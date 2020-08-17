import abjad


def rests_to_multimeasure_rest(selection: abjad.Selection):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function looks for measures filled with regular rests and converts
    them into an |abjad.MultimeasureRest|.

    Basic usage:
        Converts any measure filled with regular rests into a measure with a
        single multi-measure rest.

        >>> container = abjad.Container(r"r1")
        >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()
        >>> abjad.f(container)
        {
            R1
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-uvebc7ft1zo.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).rests_to_multimeasure_rest()
        >>> abjad.mutate(staff[:]).rests_to_multimeasure_rest()

    Multiple rests:
        Works with measures with multiple regular rests.

        >>> container = abjad.Container(r"r2 r8.. r32 r16 r8 r16")
        >>> abjad.f(container)
        {
            r2
            r8..
            r32
            r16
            r8
            r16
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-jk4m1wzsyfa.png

        >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()
        >>> abjad.f(container)
        {
            R1
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-z8u0cs3fzdi.png

    .. note::

        When using |abjad.Container|'s, all time signatures in the output will
        be commented out with ``%%%.`` This is because Abjad only applies time
        signatures to containers that belong to a |abjad.Staff|. The present
        function works with either |abjad.Container| and |abjad.Staff|.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> abjad.f(container)
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-qtq55xbkkts.png

        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-9hceg93vrmv.png

    Time signature changes:
        Works with selections from containers with multiple time signatures as
        well as notes.

        >>> container = abjad.Staff(r"\time 3/4 r2. | "
        ...                         "\time 6/8 r2. | "
        ...                         "\time 5/4 c'1 ~ c'4 | r1 r4"
        ...                         )
        >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()
        >>> abjad.f(container)
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

        .. figure:: ../_images/rests_to_multimeasure_rest-a9sqdcznoq.png

    Tuplets:
        Works with containers with tuplets.

        >>> container = abjad.Container(r"\times 2/3 {r2 r2 r2}")
        >>> abjad.f(container)
        {
            \times 2/3 {
                r2
                r2
                r2
            }
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-480a9zqvk2a.png

        >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()
        >>> abjad.f(container)
        {
            R1
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-r5yg3a3f97q.png

        It also works with containers with tuplets within tuplets.

        >>> container = abjad.Container(
        ...     r"r2 \times 2/3 {r2 r4} \times 4/5 {r2. \times 2/3 {r2 r4}}"
        ... )
        >>> abjad.f(container)
        {
            r2
            \times 2/3 {
                r2
                r4
            }
            \times 4/5 {
                r2.
                \times 2/3 {
                    r2
                    r4
                }
            }
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-codydc205jw.png

        >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()
        >>> abjad.f(container)
        {
            R1
            R1
        }

        .. figure:: ../_images/rests_to_multimeasure_rest-f647t5j3jgw.png

    .. warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")

    measures = selection.group_by_measure()
    effective_time_signature = abjad.TimeSignature((4, 4))
    for measure in measures:
        head = abjad.select(measure).leaf(0)
        time_signature = abjad.inspect(head).indicator(abjad.TimeSignature)
        if time_signature is not None:
            effective_time_signature = time_signature
        if all([isinstance(leaf, abjad.Rest) for leaf in measure.leaves()]):
            duration = abjad.inspect(measure).duration()
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
                abjad.mutate(measure).replace(multimeasure_rest)
