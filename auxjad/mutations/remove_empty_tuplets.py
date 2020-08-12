import abjad


def remove_empty_tuplets(selection: abjad.Selection):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function looks for tuplets filled with rests and replaces them with a
    single rest.

    Basic usage:
        Usage is simple:

        >>> container = abjad.Container(r"\times 2/3 {r2 r2 r2}")
        >>> abjad.f(container)
        {
            \times 2/3 {
                r2
                r2
                r2
            }
        }

        .. figure:: ../_images/image-remove_empty_tuplets-1.png

        >>> auxjad.mutate(container[:]).remove_empty_tuplets()
        >>> abjad.f(container)
        {
            r1
        }

        .. figure:: ../_images/image-remove_empty_tuplets-2.png

        It also works with containers with tuplets within tuplets.

        >>> container = abjad.Container(r"\times 4/5 {r2. \times 2/3 {r2 r4}}")
        >>> abjad.f(container)
        {
            \times 4/5 {
                r2.
                \times 2/3 {
                    r2
                    r4
                }
            }
        }

        .. figure:: ../_images/image-remove_empty_tuplets-3.png

        >>> auxjad.mutate(container[:]).remove_empty_tuplets()
        >>> abjad.f(container)
        {
            r1
        }

        .. figure:: ../_images/image-remove_empty_tuplets-4.png

        This function also simplifies a mixture of tuplets of rests and tuplets
        with notes.

        >>> container = abjad.Container(
        ...     r"r2 \times 2/3 {r2 r4} \times 4/5 {c'2. \times 2/3 {r2 r4}}")
        >>> abjad.f(container)
        {
            r2
            \times 2/3 {
                r2
                r4
            }
            \times 4/5 {
                c'2.
                \times 2/3 {
                    r2
                    r4
                }
            }
        }

        .. figure:: ../_images/image-remove_empty_tuplets-5.png

        >>> auxjad.mutate(container[:]).remove_empty_tuplets()
        >>> abjad.f(container)
        {
            r2
            r2
            \times 4/5 {
                c'2.
                r2
            }
        }

        .. figure:: ../_images/image-remove_empty_tuplets-6.png

    ..  note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).remove_empty_tuplets()
        >>> abjad.mutate(staff[:]).remove_empty_tuplets()

    ..  tip::

        Use |auxjad.mutate().rests_to_multimeasure_rest()| to replace measures
        filled with rests by a single multi-measure rest. That function makes
        use of |auxjad.mutate().remove_empty_tuplets()|, so it is not necessary
        to flatten the empty tuplets beforehand.

    Time signature changes:
        Works with measures with any time signature.

        >>> container = abjad.Container(r"\time 3/4 r2. \times 3/2 {r4 r4}")
        >>> auxjad.mutate(container[:]).remove_empty_tuplets()
        >>> abjad.f(container)
        {
            %%% \time 3/4 %%%
            r2.
            r2.
        }

        .. figure:: ../_images/image-remove_empty_tuplets-7.png

    .. note::

        Notice that the time signatures in the output are commented out with
        ``%%%``. This is because Abjad only applies time signatures to
        containers that belong to a |abjad.Staff|. The present function works
        with either |abjad.Container| and |abjad.Staff|.

        >>> container = abjad.Container(r"\time 3/4 r2. \times 3/2 {r4 r4}")
        >>> auxjad.mutate(container[:]).remove_empty_tuplets()
        >>> abjad.f(container)
        {
            %%% \time 3/4 %%%
            r2.
            r2.
        }
        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            r2.
            r2.
        }

    ..  warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")

    tuplets = selection.tuplets()
    if len(tuplets) == 0:
        return

    for tuplet in tuplets:
        leaves = abjad.select(tuplet).leaves()
        if all(isinstance(leaf, abjad.Rest) for leaf in leaves):
            duration = tuplet.multiplied_duration
            rest = abjad.Rest(duration)
            time_signature = abjad.inspect(leaves[0]).indicator(
                abjad.TimeSignature)
            if time_signature is not None:
                abjad.attach(time_signature, rest)
            abjad.mutate(tuplet).replace(rest)
