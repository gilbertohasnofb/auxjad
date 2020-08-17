import abjad


def extract_trivial_tuplets(selection: abjad.Selection):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function looks for tuplets filled with rests or with tied notes or
    chords and replaces them with a single leaf.

    Basic usage:
        Usage is simple:

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {r4 r2} \times 2/3 {c'8 ~ c'8 ~ c'2}"
        ... )
        >>> abjad.f(container)
        {
            \times 2/3 {
                r4
                r2
            }
            \times 2/3 {
                c'8
                ~
                c'8
                ~
                c'2
            }
        }

        .. figure:: ../_images/extract_trivial_tuplets-4htz2xebxwf.png

        >>> auxjad.mutate(container[:]).extract_trivial_tuplets()
        >>> abjad.f(container)
        {
            r2
            c'2
        }

        .. figure:: ../_images/extract_trivial_tuplets-2dbuwo4erhb.png

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

        .. figure:: ../_images/extract_trivial_tuplets-8d5bcyxcmhc.png

        >>> auxjad.mutate(container[:]).extract_trivial_tuplets()
        >>> abjad.f(container)
        {
            r1
        }

        .. figure:: ../_images/extract_trivial_tuplets-2a2fvwimyrx.png

        >>> container = abjad.Container(
        ...     r"\times 4/5 {c'2. ~ \times 2/3 {c'2 ~ c'4}}"
        ... )
        >>> abjad.f(container)
        {
            \times 4/5 {
                c'2.
                ~
                \times 2/3 {
                    c'2
                    ~
                    c'4
                }
            }
        }

        .. figure:: ../_images/extract_trivial_tuplets-xka6r5iyo4l.png

        >>> auxjad.mutate(staff[:]).extract_trivial_tuplets()
        >>> abjad.f(container)
        {
            c'1
        }

        .. figure:: ../_images/extract_trivial_tuplets-f1qxi44xcsw.png

    Partial extraction:
        This function also extracts tuplets within tuplets.

        >>> container = abjad.Container(
        ...     r"r2 \times 2/3 {r2 r4} \times 4/5 {c'2. \times 2/3 {r2 r4}}"
        ... )
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

        .. figure:: ../_images/extract_trivial_tuplets-adibnkb1mbs.png

        >>> auxjad.mutate(container[:]).extract_trivial_tuplets()
        >>> abjad.f(container)
        {
            r2
            r2
            \times 4/5 {
                c'2.
                r2
            }
        }

        .. figure:: ../_images/extract_trivial_tuplets-xldohyedqs.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).extract_trivial_tuplets()
        >>> abjad.mutate(staff[:]).extract_trivial_tuplets()

    .. tip::

        Use |auxjad.mutate().rests_to_multimeasure_rest()| to replace measures
        filled with rests by a single multi-measure rest. That function makes
        use of |auxjad.mutate().extract_trivial_tuplets()|, so it is not
        necessary to flatten the empty tuplets beforehand.

    Time signature changes:
        Works with measures with any time signature.

        >>> container = abjad.Staff(r"\time 3/4 r2. \times 3/2 {r4 r4}")
        >>> auxjad.mutate(container[:]).extract_trivial_tuplets()
        >>> abjad.f(container)
        \new Staff
        {
            \time 3/4
            r2.
            r2.
        }

        .. figure:: ../_images/extract_trivial_tuplets-sa1tqmvtkx.png

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

        .. figure:: ../_images/extract_trivial_tuplets-6wymsb7z1n4.png

        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/extract_trivial_tuplets-moavfyqtxza.png

    .. warning::

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
                abjad.TimeSignature
            )
            if time_signature is not None:
                abjad.attach(time_signature, rest)
            abjad.mutate(tuplet).replace(rest)
        if tuplet.sustained():
            duration = tuplet.multiplied_duration
            n_elements = len(tuplet)
            for _ in range(n_elements - 1):
                tuplet.pop(-1)
            abjad.detach(abjad.Tie(), leaves[0])
            leaves[0].written_duration = duration
            abjad.mutate(tuplet).extract()
    for tuplet in tuplets:
        if tuplet.trivializable():
            tuplet.trivialize()
            abjad.mutate(tuplet).extract()
