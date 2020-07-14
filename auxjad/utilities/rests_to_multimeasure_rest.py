import abjad

from .remove_empty_tuplets import remove_empty_tuplets


def rests_to_multimeasure_rest(container: abjad.Container):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function looks for bars filled with
    regular rests and converts them into an ``abjad.MultimeasureRest``.

    Example:
        Converts any measure filled with regular rests into a measure with a
        single multi-measure rest.

        >>> container = abjad.Container(r"r1")
        >>> auxjad.rests_to_multimeasure_rest(container)
        >>> abjad.f(container)
        {
            R1
        }

        .. figure:: ../_images/image-rests_to_multimeasure_rest-1.png

    Example:
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

        .. figure:: ../_images/image-rests_to_multimeasure_rest-2.png

        >>> auxjad.rests_to_multimeasure_rest(container)
        >>> abjad.f(container)
        {
            R1
        }

        .. figure:: ../_images/image-rests_to_multimeasure_rest-3.png

    .. note::

        Notice that the time signatures in the output are commented out with
        ``%%%``. This is because Abjad only applies time signatures to
        containers that belong to a ``abjad.Staff``. The present function works
        with either ``abjad.Container`` and ``abjad.Staff``.

        >>> container = abjad.Container(r"\time 3/4 r4 r4 r4")
        >>> auxjad.rests_to_multimeasure_rest(container)
        >>> abjad.f(container)
        {
            %%% \time 3/4 %%%
            R1 * 3/4
        }
        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            R1 * 3/4
        }

    Example:
        Works with containers with multiple time signatures as well as notes.

        >>> container = abjad.Staff(r"\time 3/4 r2. | "
        ...                         "\time 6/8 r2. | "
        ...                         "\time 5/4 c'1 ~ c'4 | r1 r4"
        ...                         )
        >>> auxjad.rests_to_multimeasure_rest(container)
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

        .. figure:: ../_images/image-rests_to_multimeasure_rest-6.png

    Example:
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

        .. figure:: ../_images/image-rests_to_multimeasure_rest-7.png

        >>> auxjad.rests_to_multimeasure_rest(container)
        >>> abjad.f(container)
        {
            R1
        }

        .. figure:: ../_images/image-rests_to_multimeasure_rest-8.png

        It also works with containers with tuplets within tuplets.

        >>> container = abjad.Container(
        ...     r"r2 \times 2/3 {r2 r4} \times 4/5 {r2. \times 2/3 {r2 r4}}")
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

        .. figure:: ../_images/image-rests_to_multimeasure_rest-9.png

        >>> auxjad.rests_to_multimeasure_rest(container)
        >>> abjad.f(container)
        {
            R1
            R1
        }

        .. figure:: ../_images/image-rests_to_multimeasure_rest-10.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")

    remove_empty_tuplets(container)
    measures = abjad.select(container[:]).group_by_measure()
    effective_time_signature = abjad.TimeSignature((4, 4))

    for measure in measures:
        head = abjad.select(measure).leaf(0)
        time_signature = abjad.inspect(head).indicator(abjad.TimeSignature)
        if time_signature is not None:
            effective_time_signature = time_signature
        if all([isinstance(leaf, abjad.Rest) for leaf in measure]):
            duration = abjad.inspect(measure).duration()
            if duration == effective_time_signature.duration:
                if duration == 1:
                    multiplier = None
                else:
                    multiplier = abjad.Multiplier(duration)
                multimeasure_rest = abjad.MultimeasureRest(
                    (4, 4), multiplier=multiplier)
                if time_signature is not None:
                    abjad.attach(time_signature, multimeasure_rest)
                abjad.mutate(measure).replace(multimeasure_rest)
