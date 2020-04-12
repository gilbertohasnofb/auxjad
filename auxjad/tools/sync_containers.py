import abjad
from .close_container import close_container
from .is_container_full import is_container_full
from .simplified_time_signature_ratio import simplified_time_signature_ratio
from .underfull_duration import underfull_duration


def sync_containers(*containers: abjad.Container,
                    use_multimeasure_rests: bool = True,
                    adjust_last_time_signature: bool = True,
                    ):
    r"""Takes an arbitrary number of ``abjad.Container``'s (or child classes),
    finds the longest one and adds rests to all the shorter ones, making them
    the same length. By default, it rewrites the last time signature if
    necessary, and uses multi-measure rests whenever possible.

    ..  container:: example

        Input two or more containers. This function will fill the shortest ones
        with rests ensuring all their lengths become the same.

        >>> container1 = abjad.Container(r"\time 4/4 g'2.")
        >>> container2 = abjad.Container(r"\time 4/4 c'1")
        >>> auxjad.sync_containers(container1, container2)
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            g'2.
            r4
        }
        >>> abjad.f(container2)
        {
            %%% \time 4/4 %%%
            c'1
        }

        Notice that the time signatures in the output are commented out with
        ``%%%``. This is because Abjad only applies time signatures to
        containers that belong to a ``abjad.Staff``. The present function works
        with either ``abjad.Container`` and ``abjad.Staff``.

        >>> container1 = abjad.Container(r"\time 4/4 g'2.")
        >>> container2 = abjad.Container(r"\time 4/4 c'1")
        >>> auxjad.sync_containers(container1, container2)
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            g'2.
            r4
        }
        >>> staff = abjad.Staff([container1])
        >>> abjad.f(container1)
        {
            \time 4/4
            g'2.
            r4
        }

    ..  container:: example

        If all containers have the same size, no modification is applied.

        >>> container1 = abjad.Container(r"\time 3/4 g'2.")
        >>> container2 = abjad.Container(r"\time 3/4 c'2.")
        >>> auxjad.sync_containers(container1, container2)
        >>> abjad.f(container1)
        {
            %%% \time 3/4 %%%
            g'2.
        }
        >>> abjad.f(container2)
        {
            %%% \time 3/4 %%%
            c'2.
        }

    ..  container:: example

        By default, this function closes the longest container by rewriting the
        time signature of its last bar if necessary (if it is underfull), and
        uses multi-measure rests whenever possible.

        >>> container1 = abjad.Container(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Container(r"\time 4/4 c'1")
        >>> auxjad.sync_containers(container1, container2)
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            g'1
            %%% \time 1/4 %%%
            f'4
        }
        >>> abjad.f(container2)
        {
            %%% \time 4/4 %%%
            c'1
            %%% \time 1/4 %%%
            R1*1/4
        }

    ..  container:: example

        To disable multi-measure rests, set the keyword argument
        ``use_multimeasure_rests`` to ``False``.

        >>> container1 = abjad.Container(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Container(r"\time 4/4 c'1")
        >>> auxjad.sync_containers(container1,
        ...                        container2,
        ...                        use_multimeasure_rests=False,
        ...                        )
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            g'1
            %%% \time 1/4 %%%
            f'4
        }
        >>> abjad.f(container2)
        {
            %%% \time 4/4 %%%
            c'1
            %%% \time 1/4 %%%
            r4
        }

    ..  container:: example

        To allow containers to be left open (with underfull bars), set the
        keyword argument ``adjust_last_time_signature`` to ``False``.

        >>> container1 = abjad.Container(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Container(r"\time 4/4 c'1")
        >>> auxjad.sync_containers(container1,
        ...                        container2,
        ...                        adjust_last_time_signature=False,
        ...                        )
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            g'1
            f'4
        }
        >>> abjad.f(container2)
        {
            %%% \time 4/4 %%%
            c'1
            r4
        }

    ..  container:: example

        This function can take an arbitrary number of containers.

        >>> container1 = abjad.Container(r"\time 4/4 c'1 | g'4")
        >>> container2 = abjad.Container(r"\time 4/4 c'1 | g'2")
        >>> container3 = abjad.Container(r"\time 4/4 c'1 | g'2.")
        >>> container4 = abjad.Container(r"\time 4/4 c'1")
        >>> auxjad.sync_containers(container1,
        ...                        container2,
        ...                        container3,
        ...                        container4,
        ...                        )
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            c'1
            %%% \time 3/4 %%%
            g'4
            r2
        }
        >>> abjad.f(container2)
        {
            %%% \time 4/4 %%%
            c'1
            %%% \time 3/4 %%%
            g'2
            r4
        }
        >>> abjad.f(container3)
        {
            %%% \time 4/4 %%%
            c'1
            %%% \time 3/4 %%%
            g'2.
        }
        >>> abjad.f(container4)
        {
            %%% \time 4/4 %%%
            c'1
            %%% \time 3/4 %%%
            R1*3/4
        }

    ..  container:: example

        The containers can be of different length, can have different time
        signatures, and can contain time signature changes as well.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 4/4 c'4")
        >>> container3 = abjad.Container(r"\time 5/4 g''1 ~ g''4")
        >>> container4 = abjad.Container(r"\time 6/8 c'2")
        >>> auxjad.sync_containers(container1,
        ...                        container2,
        ...                        container3,
        ...                        container4,
        ...                        )
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            %%% \time 1/4 %%%
            R1*1/4
        }
        >>> abjad.f(container2)
        {
            %%% \time 3/4 %%%
            a2.
            %%% \time 2/4 %%%
            c'4
            r4
        }
        >>> abjad.f(container3)
        {
            %%% \time 5/4 %%%
            g''1
            ~
            g''4
        }
        >>> abjad.f(container4)
        {
            %%% \time 6/8 %%%
            c'2
            r4
            %%% \time 2/4 %%%
            R1*1/2
        }

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
        >>> auxjad.sync_containers(container1,
        ...                        container2,
        ...                        container3,
        ...                        container4,
        ...                        )
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

    ..  container:: example

        If one or more containers is malformed, i.e. it has an underfilled bar
        before a time signature change, the function raises a ``ValueError``
        exception.

        >>> container1 = abjad.Container(r"\time 4/4 g'1 | f'4")
        >>> container2 = abjad.Container(r"\time 5/4 c'1 | \time 4/4 d'4")
        >>> auxjad.sync_containers(container1, container2)
        ValueError: at least one 'container' is malformed, with an underfull
        bar preceeding a time signature change
    """
    for container in containers:
        if not isinstance(container, abjad.Container):
            raise TypeError("all 'containers' must be 'abjad.Container' or "
                            "child class")
        try:
            is_container_full(container)
        except:
            raise ValueError("at least one 'container' is malformed, with an "
                             "underfull bar preceeding a time signature "
                             "change")
    durations = [abjad.inspect(container[:]).duration() for container
                 in containers]
    max_duration = max(durations)
    for container, duration in zip(containers, durations):
        duration_difference = max_duration - duration
        if duration_difference > abjad.Duration(0):
            # handling duration left in the last bar, if any
            if not is_container_full(container):
                duration_left = underfull_duration(container)
                underfull_rests_duration = min(duration_difference,
                                               duration_left,
                                               )
                underfull_rests = abjad.LeafMaker()(None,
                                                    underfull_rests_duration,
                                                    )
                duration_difference -= underfull_rests_duration
                container.extend(underfull_rests)
                if adjust_last_time_signature and duration_difference == \
                        abjad.Duration(0):
                    close_container(container)
                if duration_difference == abjad.Duration(0):
                    continue
            # finding out last effective time signature
            for leaf in abjad.select(container).leaves()[::-1]:
                effective_time_signature = abjad.inspect(leaf).effective(
                    abjad.TimeSignature)
                if effective_time_signature:
                    break
            else:
                effective_time_signature = abjad.TimeSignature((4, 4))
            # creating new bars for any leftover duratin
            if use_multimeasure_rests and (adjust_last_time_signature or \
                    duration_difference == effective_time_signature.duration):
                multiplier = duration_difference.pair
                if multiplier[0] == multiplier[1]:  # avoiding R1 * 1
                    multiplier = None
                rests = [abjad.MultimeasureRest((4, 4), multiplier=multiplier)]
            else:
                rests = abjad.LeafMaker()(None, duration_difference)
            if adjust_last_time_signature:
                rests_time_signature = abjad.TimeSignature(duration_difference)
                rests_time_signature = simplified_time_signature_ratio(
                    rests_time_signature)
                if rests_time_signature != effective_time_signature:
                    abjad.attach(rests_time_signature, rests[0])
            container.extend(rests)
        else:
            # closing longest container if necessary
            if adjust_last_time_signature and not is_container_full(container):
                close_container(container)


# SETUP
container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
# container2 = abjad.Container(r"\time 3/4 a2. c'4")
# container3 = abjad.Container(r"\time 5/4 g''1 ~ g''4")
# container4 = abjad.Container(r"\time 6/8 c'2")
container2 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g' a'")
container3 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g' a' b'")
container4 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'")

staves = [abjad.Staff([container1]),
          abjad.Staff([container2]),
          abjad.Staff([container3]),
          abjad.Staff([container4]),
          ]

sync_containers(container1,
                container2,
                container3,
                container4,
                #use_multimeasure_rests=False,
                )

# =============================================================================
# TODO: function for this below?
lilypond_file = abjad.LilyPondFile.new()
score = abjad.Score(staves)
score_block = abjad.Block(name='score')
layout_block = abjad.Block(name='layout')
score_block.items.append(score)
score_block.items.append(layout_block)
lilypond_file.items.append(score_block)
layout_block.items.append(
    r'''
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
    ''')

# abjad.show(lilypond_file)
