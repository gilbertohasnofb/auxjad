import abjad


def merge_partial_tuplets(selection: abjad.Selection,
                          *,
                          merge_across_barlines: bool = False,
                          ):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function merges all consecutive partial tuplets with the same ratio
    and which sum up to an assignable duration. Partial tuplets can result from
    algorithmic manipulations such as phasing or looping, which can slice
    through a tuplet.

    Basic usage:
        Usage is simple:

        >>> staff = abjad.Staff(r"\times 2/3 {c'1} \times 2/3 {d'2}")
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'1
            }
            \times 2/3 {
                d'2
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-ilr68s15kqb.png

        >>> auxjad.mutate(staff[:]).merge_partial_tuplets()
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'1
                d'2
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-qe29etsedx.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).merge_partial_tuplets()
        >>> abjad.mutate(staff[:]).merge_partial_tuplets()

    Multiple consecutive partial tuplets:
        This function can also handle several consecutive partial tuplets:

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'2} \times 2/3 {d'2} \times 2/3 {e'2}"
        ... )
        >>> abjad.f(staff)
        {
            \times 2/3 {
                c'2
            }
            \times 2/3 {
                d'2
            }
            \times 2/3 {
                e'2
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-9rh7vpu208j.png

        >>> auxjad.mutate(staff[:]).merge_partial_tuplets()
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'2
                d'2
                e'2
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-oy1imqisx2.png

    ``merge_across_barlines``:
        By default, partial tuplets are not merged across barlines.

        >>> staff = abjad.Staff(r"\time 3/4 c'2. "
        ...                     r"\times 2/3 {d'4} r4 \times 2/3 {e'2} "
        ...                     r"\times 2/3 {f'4} r4 \times 2/3 {g'2}")
        >>> auxjad.mutate(staff[:]).merge_partial_tuplets()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'4
            }
            r4
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                e'2
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'4
            }
            r4
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g'2
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-3rjib7pctml.png

        To change  this behaviour, set ``merge_across_barlines`` to ``True``.

        >>> staff = abjad.Staff(r"\time 3/4 c'2. "
        ...                     r"\times 2/3 {d'4} r4 \times 2/3 {e'2} "
        ...                     r"\times 2/3 {f'4} r4 \times 2/3 {g'2}")
        >>> auxjad.mutate(staff[:]).merge_partial_tuplets(
        ...     merge_across_barlines=True,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'4
            }
            r4
            \times 2/3 {
                e'2
                f'4
            }
            r4
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g'2
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-icud1ejcmzc.png

    Tied partial tuplets:
        Tied partial tuplets are also handled by this function.

        >>> staff = abjad.Staff(r"\times 2/3 {r4} \times 2/3 {c'2} "
        ...                     r"\times 4/5 {d'2~} \times 4/5{d'8}")
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                r4
            }
            \times 2/3 {
                c'2
            }
            \times 4/5 {
                d'2
                ~
            }
            \times 4/5 {
                d'8
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-st4zw38qfce.png

        >>> auxjad.mutate(staff[:]).merge_partial_tuplets()
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                r4
                c'2
            }
            \times 4/5 {
                d'2
                ~
                d'8
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-1pky5fsh2nl.png

    Indicators:
        Indicators stay the same in the merged tuplet.

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'2\p\< d'2} \times 2/3 {e'2\ff}"
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'2
                \p
                \<
                d'2
            }
            \times 2/3 {
                e'2
                \ff
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-7cdtafl348h.png

        >>> auxjad.mutate(staff[:]).merge_partial_tuplets()
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'2
                \p
                \<
                d'2
                e'2
                \ff
            }
        }

        .. figure:: ../_images/merge_partial_tuplets-j9rmdfbawce.png

    .. tip::

        The method |auxjad.mutate().extract_trivial_tuplets()| can be used
        after merging partial tuplets to further clean the output. The method
        |auxjad.mutate().auto_rewrite_meter()| can also be used for this
        purpose, as it will not only rewrite the metric notation of a staff but
        also apply both |auxjad.mutate().merge_partial_tuplets()| and
        |auxjad.mutate().extract_trivial_tuplets()| to the output.

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

        .. figure:: ../_images/merge_partial_tuplets-945s36mfdn.png

        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/merge_partial_tuplets-3b4tyqrnttw.png

    .. warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not isinstance(merge_across_barlines, bool):
        raise TypeError("'merge_across_barlines' must be 'bool'")

    tuplets = selection.tuplets()
    if len(tuplets) <= 1:
        return

    def _process_tuplets(tuplets):
        for index in range(len(tuplets[:-1])):
            for upper_index in range(index, len(tuplets)):
                if (tuplets[index].multiplier
                        == tuplets[upper_index].multiplier):
                    tuplet_group = tuplets[index:upper_index + 1]
                else:
                    break
                if tuplet_group.are_contiguous_logical_voice():
                    durations = [abjad.inspect(tuplet).duration()
                                 for tuplet in tuplet_group]
                    sum_durations = sum(durations)
                    if (all(not duration.has_power_of_two_denominator
                            for duration in durations)
                            and sum_durations.has_power_of_two_denominator):
                        for tuplet in tuplet_group[1:]:
                            tuplet_group[0].extend(tuplet)
                            abjad.mutate(tuplet).extract()

    if not merge_across_barlines:
        measures = selection.group_by_measure()
        for measure in measures:
            tuplets = abjad.select(measure).tuplets()
            if len(tuplets) <= 1:
                continue
            _process_tuplets(tuplets)
    else:
        _process_tuplets(tuplets)
