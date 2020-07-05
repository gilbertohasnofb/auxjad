import abjad


def remove_empty_tuplets(container: abjad.Container):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function looks for tuplets filled
    with rests and replaces them with a single rest.

    Example:
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

        >>> auxjad.remove_empty_tuplets(container)
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

        >>> auxjad.remove_empty_tuplets(container)
        >>> abjad.f(container)
        {
            r1
        }

        .. figure:: ../_images/image-remove_empty_tuplets-4.png

        This function also simplifies a mix of tuplets of rests and tuplets
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

        >>> auxjad.remove_empty_tuplets(container)
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

    ..  tip::

        Use ``auxjad.rests_to_multimeasure_rest()`` to replace bars filled with
        rests by a single multi-measure rest. That function makes use of
        ``remove_empty_tuplets()``, so it is not necessary to flatten the
        empty tuplets beforehand.

    Example:
        Works with measures with any time signature.

        >>> container = abjad.Container(r"\time 3/4 r2. \times 3/2 {r4 r4}")
        >>> auxjad.remove_empty_tuplets(container)
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
        containers that belong to a ``abjad.Staff``. The present function works
        with either ``abjad.Container`` and ``abjad.Staff``.

        >>> container = abjad.Container(r"\time 3/4 r2. \times 3/2 {r4 r4}")
        >>> auxjad.remove_empty_tuplets(container)
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
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")

    tuplets = abjad.select(container).tuplets()
    if len(tuplets) == 0:
        return

    # checking if there are tuplets. First, finding the deepest depth of a
    # tuplet
    tuplet_count = []
    for tuplet in tuplets:
        tuplet_count.append(
            abjad.inspect(tuplet).parentage().count(abjad.Tuplet)
        )
    max_count = max(tuplet_count)

    # going from the deepest depth to the shallowest, replace tuplets
    # containing only rests with a single rest of that value
    for current_count in range(max_count, -1, -1):
        for tuplet in abjad.select(container).tuplets():
            parentage = abjad.inspect(tuplet).parentage()
            tuplet_count = parentage.count(abjad.Tuplet)
            if tuplet_count == current_count:
                leaves = abjad.select(tuplet).leaves()
                if all(isinstance(leaf, abjad.Rest) for leaf in leaves):
                    duration = tuplet.multiplied_duration
                    rest = abjad.Rest(duration)
                    time_signature = abjad.inspect(leaves[0]).indicator(
                        abjad.TimeSignature)
                    if time_signature is not None:
                        abjad.attach(time_signature, rest)
                    abjad.mutate(tuplet).replace(rest)
