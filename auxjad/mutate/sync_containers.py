from collections.abc import Iterable
from typing import Union

import abjad

from .. import get
from .close_container import close_container
from .rests_to_multimeasure_rest import rests_to_multimeasure_rest


def sync_containers(containers: Union[Iterable[abjad.Container],
                                      abjad.Score,
                                      ],
                    *,
                    use_multimeasure_rests: bool = True,
                    adjust_last_time_signature: bool = True,
                    ) -> None:
    r"""Mutates two or more input containers in place and has no return value;
    this function finds the longest container among the inputs and adds rests
    to all the shorter ones, making them the same length. Input argument can
    be a single |abjad.Score| with multiple containers, or an iterable with
    elements of type |abjad.Container| or child classes.

    Basic usage:
        Input two or more containers. This function will fill the shortest ones
        with rests ensuring all their lengths become the same.

        >>> staff1 = abjad.Staff(r"\time 4/4 g'2.")
        >>> staff2 = abjad.Staff(r"\time 4/4 c'1")
        >>> abjad.show(staff1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'2.
            }

        ..  figure:: ../_images/sync_containers-H7jNwGEtFQ.png

        >>> abjad.show(staff2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
            }

        ..  figure:: ../_images/sync_containers-EjKqQCinPy.png

        >>> auxjad.mutate.sync_containers([staff1, staff2])
        >>> abjad.show(staff1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'2.
                r4
            }

        ..  figure:: ../_images/sync_containers-akcdf8t9e5.png

        >>> abjad.show(staff2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
            }

        ..  figure:: ../_images/sync_containers-l7tru1tjoli.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.sync_containers([container1, container2])
        >>> abjad.mutate.sync_containers([container1, container2])

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

        ..  figure:: ../_images/sync_containers-9sl3dnd2uwn.png

        >>> staff = abjad.Staff([container])
        >>> abjad.show(container)

        ..  docs::

            {
                \time 3/4
                c'4
                d'4
                e'4
            }

        ..  figure:: ../_images/sync_containers-08v2pv2tmqqn.png

    Containers of same size:
        If all containers have the same size, no modification is applied.

        >>> container1 = abjad.Staff(r"\time 3/4 g'2.")
        >>> container2 = abjad.Staff(r"\time 3/4 c'2.")
        >>> auxjad.mutate.sync_containers([container1, container2])
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 3/4
                g'2.
            }

        ..  figure:: ../_images/sync_containers-e0yszxejbh.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2.
            }

        ..  figure:: ../_images/sync_containers-2cgt4zds3h7.png

    Underfull containers:
        By default, this function closes the longest container by rewriting the
        time signature of its last measure if necessary (if it is underfull),
        and uses multi-measure rests whenever possible.

        >>> container1 = abjad.Staff(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Staff(r"\time 4/4 c'1")
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'1
                f'4
            }

        ..  figure:: ../_images/sync_containers-udnAjAZtkw.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
            }

        ..  figure:: ../_images/sync_containers-cy8dL4UUWV.png

        >>> auxjad.mutate.sync_containers([container1, container2])
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'1
                \time 1/4
                f'4
            }

        ..  figure:: ../_images/sync_containers-nztndgecrof.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                \time 1/4
                R1 * 1/4
            }

        ..  figure:: ../_images/sync_containers-iaag195ty1d.png

    ``adjust_last_time_signature``:
        To allow containers to be left open (with underfull measures), set the
        keyword argument ``adjust_last_time_signature`` to ``False``.

        >>> container1 = abjad.Staff(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Staff(r"\time 4/4 c'1")
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'1
                f'4
            }

        ..  figure:: ../_images/sync_containers-uldd5Vni8a.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
            }

        ..  figure:: ../_images/sync_containers-eTCrjHBr39.png

        >>> auxjad.mutate.sync_containers(
        ...     [container1, container2],
        ...     adjust_last_time_signature=False,
        ... )
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'1
                f'4
            }

        ..  figure:: ../_images/sync_containers-37iesjp4dqs.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                r4
            }

        ..  figure:: ../_images/sync_containers-lqm4itxlwu.png

    ``use_multimeasure_rests``:
        To disable multi-measure rests, set the keyword argument
        ``use_multimeasure_rests`` to ``False``.

        >>> container1 = abjad.Staff(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Staff(r"\time 4/4 c'1")
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'1
                \time 1/4
                f'4
            }

        ..  figure:: ../_images/sync_containers-Mbmjf7JLH8.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
            }

        ..  figure:: ../_images/sync_containers-3RZwROEIt1.png

        >>> auxjad.mutate.sync_containers(
        ...     [container1, container2],
        ...     use_multimeasure_rests=False,
        ... )
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                g'1
                \time 1/4
                f'4
            }

        ..  figure:: ../_images/sync_containers-rhagiugx42o.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                \time 1/4
                r4
            }

        ..  figure:: ../_images/sync_containers-oss03t1qnf8.png

    Adjusting last time signatures:
        When adjusting the last time signature, this function will maintain the
        same time effective signature for as long as possible and only add a
        new one at the last measure if its duration is shorter.

        >>> container1 = abjad.Staff(r"\time 7/4 a'1 ~ a'2.")
        >>> container2 = abjad.Staff(r"\time 3/4 c'2.")
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 7/4
                a'1
                ~
                a'2.
            }

        ..  figure:: ../_images/sync_containers-g61gTyfZGV.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2.
            }

        ..  figure:: ../_images/sync_containers-UZvmef5N16.png

        >>> auxjad.mutate.sync_containers([container1, container2])
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 7/4
                a'1
                ~
                a'2.
            }

        ..  figure:: ../_images/sync_containers-dQnq2ASkTu.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2.
                R1 * 3/4
                \time 1/4
                R1 * 1/4
            }

        ..  figure:: ../_images/sync_containers-jhx0r9skgwi.png

    Multiple input containers:
        This function can take an arbitrary number of containers.

        >>> container1 = abjad.Staff(r"\time 4/4 c'1 | g'4")
        >>> container2 = abjad.Staff(r"\time 4/4 c'1 | g'2")
        >>> container3 = abjad.Staff(r"\time 4/4 c'1 | g'2.")
        >>> container4 = abjad.Staff(r"\time 4/4 c'1")
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                g'4
            }

        ..  figure:: ../_images/sync_containers-epvaWYPYT7.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                g'2
            }

        ..  figure:: ../_images/sync_containers-Yja5mx93Fi.png

        >>> abjad.show(container3)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                g'2.
            }

        ..  figure:: ../_images/sync_containers-GTtAEELheA.png

        >>> abjad.show(container4)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
            }

        ..  figure:: ../_images/sync_containers-VCFpuJX7ID.png

        >>> containers = [container1,
        ...               container2,
        ...               container3,
        ...               container4,
        ...               ]
        >>> auxjad.mutate.sync_containers(containers)
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                \time 3/4
                g'4
                r2
            }

        ..  figure:: ../_images/sync_containers-1wbsyvks33r.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                \time 3/4
                g'2
                r4
            }

        ..  figure:: ../_images/sync_containers-td1whqky24b.png

        >>> abjad.show(container3)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                \time 3/4
                g'2.
            }

        ..  figure:: ../_images/sync_containers-g07scyil9jh.png

        >>> abjad.show(container4)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'1
                \time 3/4
                R1 * 3/4
            }

        ..  figure:: ../_images/sync_containers-8b6vn3azaom.png

    Single input |abjad.Score|:
        This function can also take a single |abjad.Score| instead of
        multiple |abjad.Container|'s or |abjad.Staff|'s.

        >>> staff1 = abjad.Staff(r"\time 3/8 c'4. | d'4")
        >>> staff2 = abjad.Staff(r"\time 3/8 c'4. | d'8")
        >>> staff3 = abjad.Staff(r"\time 3/8 c'4. | d'16")
        >>> staff4 = abjad.Staff(r"\time 3/8 c'4.")
        >>> score = abjad.Score([staff1,
        ...                      staff2,
        ...                      staff3,
        ...                      staff4,
        ...                      ])
        >>> auxjad.mutate.sync_containers(score)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \time 3/8
                    c'4.
                    \time 1/4
                    d'4
                }
                \new Staff
                {
                    \time 3/8
                    c'4.
                    \time 1/4
                    d'8
                    r8
                }
                \new Staff
                {
                    \time 3/8
                    c'4.
                    \time 1/4
                    d'16
                    r8.
                }
                \new Staff
                {
                    \time 3/8
                    c'4.
                    \time 1/4
                    R1 * 1/4
                }
            >>

        ..  figure:: ../_images/sync_containers-0g0651fs0luq.png

    Time signature changes:
        The containers can be of different length, can have different time
        signatures, and can contain time signature changes as well.

        >>> container1 = abjad.Staff(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"\time 3/4 a2. \time 4/4 c'4")
        >>> container3 = abjad.Staff(r"\time 5/4 g''1 ~ g''4")
        >>> container4 = abjad.Staff(r"\time 6/8 c'2")
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
            }

        ..  figure:: ../_images/sync_containers-qAt4FSyAIl.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 3/4
                a2.
                \time 4/4
                c'4
            }

        ..  figure:: ../_images/sync_containers-EKrqsCDVNs.png

        >>> abjad.show(container3)

        ..  docs::

            \new Staff
            {
                \time 5/4
                g''1
                ~
                g''4
            }

        ..  figure:: ../_images/sync_containers-lw5fknvt4o.png

        >>> abjad.show(container4)

        ..  docs::

            \new Staff
            {
                \time 6/8
                c'2
            }

        ..  figure:: ../_images/sync_containers-iXGajGKBZl.png

        >>> containers = [container1,
        ...               container2,
        ...               container3,
        ...               container4,
        ...               ]
        >>> auxjad.mutate.sync_containers(containers)
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
                \time 1/4
                R1 * 1/4
            }

        ..  figure:: ../_images/sync_containers-mec52wgbrz9.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 3/4
                a2.
                \time 2/4
                c'4
                r4
            }

        ..  figure:: ../_images/sync_containers-33odhzqyo6r.png

        >>> abjad.show(container3)

        ..  docs::

            \new Staff
            {
                \time 5/4
                g''1
                ~
                g''4
            }

        ..  figure:: ../_images/sync_containers-s7rmadmd1f.png

        >>> abjad.show(container4)

        ..  docs::

            \new Staff
            {
                \time 6/8
                c'2
                r4
                \time 2/4
                R1 * 1/2
            }

        ..  figure:: ../_images/sync_containers-msu922pcn6e.png

    Polymetric notation:
        It's important to note that LilyPond does not support simultanoues
        staves with different time signatures (i.e. polymetric notation) by
        default. In order to enable it, the ``"Timing_translator"`` and
        ``"Default_bar_line_engraver"`` must be removed from the ``Score``
        context and added to the ``Staff`` context. Below is a full example of
        how this can be accomplished using Abjad.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 4/4 c'4")
        >>> container3 = abjad.Container(r"\time 5/4 g''1 ~ g''4")
        >>> container4 = abjad.Container(r"\time 6/8 c'2")
        >>> containers = [container1,
        ...               container2,
        ...               container3,
        ...               container4,
        ...               ]
        >>> auxjad.mutate.sync_containers(containers)
        >>> staves = [abjad.Staff([container1]),
        ...           abjad.Staff([container2]),
        ...           abjad.Staff([container3]),
        ...           abjad.Staff([container4]),
        ...           ]
        >>> score = abjad.Score(staves)
        >>> lilypond_file = abjad.LilyPondFile.new()
        >>> score_block = abjad.Block(name='score')
        >>> layout_block = abjad.Block(name='layout')
        >>> score_block.items.append(score)
        >>> score_block.items.append(layout_block)
        >>> lilypond_file.items.append(score_block)
        >>> layout_block.items.append(
        ...     r'''
        ...     \context {
        ...         \Score
        ...         \remove "Timing_translator"
        ...         \remove "Default_bar_line_engraver"
        ...     }
        ...     \context {
        ...         \Staff
        ...         \consists "Timing_translator"
        ...         \consists "Default_bar_line_engraver"
        ...     }
        ...     ''')
        >>> abjad.show(lilypond_file)

        ..  docs::

            \score { %! abjad.LilyPondFile._get_formatted_blocks()
                \new Score
                <<
                    \new Staff
                    {
                        {
                            \time 4/4
                            c'4
                            d'4
                            e'4
                            f'4
                            \time 1/4
                            R1 * 1/4
                        }
                    }
                    \new Staff
                    {
                        {
                            \time 3/4
                            a2.
                            \time 2/4
                            c'4
                            r4
                        }
                    }
                    \new Staff
                    {
                        {
                            \time 5/4
                            g''1
                            ~
                            g''4
                        }
                    }
                    \new Staff
                    {
                        {
                            \time 6/8
                            c'2
                            r4
                            \time 2/4
                            R1 * 1/2
                        }
                    }
                >>
                \layout {
                    \context {
                        \Score
                        \remove "Timing_translator"
                        \remove "Default_bar_line_engraver"
                    }
                    \context {
                        \Staff
                        \consists "Timing_translator"
                        \consists "Default_bar_line_engraver"
                    }
                }
            } %! abjad.LilyPondFile._get_formatted_blocks()

        ..  figure:: ../_images/sync_containers-1lbrepesgil.png

    ..  error::

        If one or more containers is malformed, i.e. it has an underfilled
        measure before a time signature change, the function raises a
        :exc:`ValueError` exception.

        >>> container1 = abjad.Container(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Container(r"\time 5/4 c'1 | \time 4/4 d'4")
        >>> auxjad.mutate.sync_containers([container1, container2])
        ValueError: at least one 'container' is malformed, with an underfull
        measure preceding a time signature change
    """
    if not isinstance(containers, (Iterable, abjad.Score)):
        raise TypeError("argument must be 'abjad.Score' or iterable of "
                        "'abjad.Container's")
    if isinstance(containers, abjad.Score):
        containers = containers[:]
    for container in containers:
        if not isinstance(container, abjad.Container):
            raise TypeError("argument must be 'abjad.Score' or iterable of "
                            "'abjad.Container's")
        if not abjad.select(container).leaves().are_contiguous_logical_voice():
            raise ValueError("argument must each be contiguous logical voice")
        try:
            get.selection_is_full(container[:])
        except ValueError as err:
            raise ValueError("at least one 'container' is malformed, with an "
                             "underfull measure preceding a time signature "
                             "change") from err
    if not isinstance(use_multimeasure_rests, bool):
        raise TypeError("'use_multimeasure_rests' must be 'bool'")
    if not isinstance(adjust_last_time_signature, bool):
        raise TypeError("'adjust_last_time_signature' must be 'bool'")

    durations = [abjad.get.duration(container[:]) for container
                 in containers]
    max_duration = max(durations)
    for container, duration in zip(containers, durations):
        duration_difference = max_duration - duration
        if duration_difference > abjad.Duration(0):
            # handling duration left in the last measure, if any
            if not get.selection_is_full(container[:]):
                duration_left = get.underfull_duration(container[:])
                underfull_rests_duration = min(duration_difference,
                                               duration_left,
                                               )
                underfull_rests = abjad.LeafMaker()(None,
                                                    underfull_rests_duration,
                                                    )
                duration_difference -= underfull_rests_duration
                container.extend(underfull_rests)
                if (duration_difference == abjad.Duration(0)
                        and adjust_last_time_signature):
                    close_container(container)
                if duration_difference == abjad.Duration(0):
                    continue
            # finding out last effective time signature
            for leaf in abjad.select(container).leaves()[::-1]:
                effective_time_signature = abjad.get.effective(
                    leaf,
                    abjad.TimeSignature,
                )
                if effective_time_signature is not None:
                    break
            else:
                effective_time_signature = abjad.TimeSignature((4, 4))
            # creating new measures for any leftover duration
            measure_duration = effective_time_signature.duration
            while duration_difference > measure_duration:
                rests = abjad.LeafMaker()(None, measure_duration)
                duration_difference -= measure_duration
                container.extend(rests)
            if duration_difference > abjad.Duration(0):
                rests = abjad.LeafMaker()(None, duration_difference)
                if adjust_last_time_signature:
                    rests_time_signature = abjad.TimeSignature(
                        duration_difference,
                    )
                    rests_time_signature.simplify_ratio()
                    if rests_time_signature != effective_time_signature:
                        abjad.attach(rests_time_signature, rests[0])
                container.extend(rests)
            if use_multimeasure_rests:
                rests_to_multimeasure_rest(container[:])
        else:
            # closing longest container if necessary
            if (adjust_last_time_signature
                    and not get.selection_is_full(container[:])):
                close_container(container)
