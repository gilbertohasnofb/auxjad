Looping with :class:`auxjad.LeafLooper`
=======================================

In this first example, we will use the class :class:`auxjad.LeafLooper` to loop
through some musical material. This class creates subselections of logical
ties and has a looping window of variable size.

First, we start by importing both :mod:`abjad` and |auxjad|_.

    >>> import abjad
    >>> import auxjad

Let's now create a container with some arbitrary material to be manipulated
by the looper. For that, let's use :class:`auxjad.TenneySelector` to generate
the random material. This class is an implementation of the Dissonant
Counterpoint Algorithm by James Tenney. In a nutshell, this algorithm can be
used to randomly select elements from a :obj:`list`, giving priority to
elements that have not been chosen for the longest time. It also ensures that
elements are not repeated.

To start, we create two selectors, one for pitches and one for durations.

    >>> pitch_selector = auxjad.TenneySelector(["d'",
    ...                                         ("c'", "d'", "e'"),
    ...                                         ("b", "d'", "g'"),
    ...                                         ("bf", "d'", "a'"),
    ...                                         ("a", "d'", "b'"),
    ...                                         ])
    >>> duration_selector = auxjad.TenneySelector([(1, 16),
    ...                                            (2, 16),
    ...                                            (3, 16),
    ...                                            (4, 16),
    ...                                            ])

Let's now use those selectors to create fourteen random notes and chords, which
will serve as our input material for the looper.

    >>> pitches = []
    >>> durations = []
    >>> for _ in range(14):
    ...     pitches.append(pitch_selector())
    ...     durations.append(duration_selector())

We can now use |abjad.LeafMaker| to convert those two :obj:`list`'s of pitches
and durations into notes. It's important to note that there is no time
signature being imposed at this point, so LilyPond will fallback to a four by
four when displaying the container below. This is not a problem since this will
be used as the basic material for the looper, which will then automatically
take care of time signatures.

    >>> notes = abjad.LeafMaker()(pitches, durations)
    >>> container = abjad.Container(notes)
    >>> abjad.show(container)

    ..  docs::

        {
            <bf d' a'>16
            <a d' b'>8.
            d'4
            <b d' g'>16
            <bf d' a'>8
            <c' d' e'>8.
            <a d' b'>16
            <bf d' a'>4
            d'16
            <a d' b'>8
            <bf d' a'>4
            <b d' g'>8.
            <c' d' e'>16
            <bf d' a'>8
        }

    ..  figure:: ../_images/example-2-looping-4qwapicxjz3.png

At this point, we can create the :class:`auxjad.LeafLooper` and initialise it
using the material we generated above. A :attr:`~auxjad.LeafLooper.window_size`
of size ``4`` will select four notes at each iteration. Setting
:attr:`~auxjad.LeafLooper.after_rest` to the duration ``(1, 2)`` will add
minim rests in between consecutive outputs of this looper. Setting
:attr:`~auxjad.LeafLooper.after_rest_in_new_measure` to ``True`` ensure that
these rests (which work as separators of consecutive windows) are in a new
measure by themselves.

    >>> looper = auxjad.LeafLooper(container,
    ...                            window_size=4,
    ...                            after_rest=(1, 2),
    ...                            after_rest_in_new_measure=True,
    ...                            )

We can now use the :meth:`~auxjad.LeafLooper.output_n` to output several
measures of the looping process for us. In this case, let's output seven
measures.

    >>> staff = abjad.Staff(looper.output_n(7))
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 9/16
            <bf d' a'>16
            <a d' b'>8
            ~
            <a d' b'>16
            d'8
            ~
            d'8
            <b d' g'>16
            \time 2/4
            R1 * 1/2
            \time 5/8
            <a d' b'>8.
            d'8.
            ~
            d'16
            <b d' g'>16
            <bf d' a'>8
            \time 2/4
            R1 * 1/2
            \time 5/8
            d'4
            <b d' g'>16
            <bf d' a'>16
            ~
            <bf d' a'>16
            <c' d' e'>8.
            \time 2/4
            R1 * 1/2
            \time 7/16
            <b d' g'>16
            <bf d' a'>8
            <c' d' e'>8.
            <a d' b'>16
            \time 2/4
            R1 * 1/2
            \time 5/8
            <bf d' a'>8
            <c' d' e'>8.
            <a d' b'>16
            <bf d' a'>4
            \time 2/4
            R1 * 1/2
            \time 9/16
            <c' d' e'>8.
            <a d' b'>16
            <bf d' a'>8
            ~
            <bf d' a'>8
            d'16
            \time 2/4
            R1 * 1/2
            <a d' b'>16
            <bf d' a'>8.
            ~
            <bf d' a'>16
            d'16
            <a d' b'>8
            R1 * 1/2
        }

    ..  figure:: ../_images/example-2-looping-9mzjqtfcru8.png

At this point, let's change the :attr:`~auxjad.LeafLooper.window_size` to a
smaller value as well as change the duration of the separator rest. Let's then
output five more measures.

    >>> looper.window_size = 3
    >>> looper.after_rest = (3, 16)
    >>> staff.append(looper.output_n(5))
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 9/16
            <bf d' a'>16
            <a d' b'>8
            ~
            <a d' b'>16
            d'8
            ~
            d'8
            <b d' g'>16
            \time 2/4
            R1 * 1/2
            \time 5/8
            <a d' b'>8.
            d'8.
            ~
            d'16
            <b d' g'>16
            <bf d' a'>8
            \time 2/4
            R1 * 1/2
            \time 5/8
            d'4
            <b d' g'>16
            <bf d' a'>16
            ~
            <bf d' a'>16
            <c' d' e'>8.
            \time 2/4
            R1 * 1/2
            \time 7/16
            <b d' g'>16
            <bf d' a'>8
            <c' d' e'>8.
            <a d' b'>16
            \time 2/4
            R1 * 1/2
            \time 5/8
            <bf d' a'>8
            <c' d' e'>8.
            <a d' b'>16
            <bf d' a'>4
            \time 2/4
            R1 * 1/2
            \time 9/16
            <c' d' e'>8.
            <a d' b'>16
            <bf d' a'>8
            ~
            <bf d' a'>8
            d'16
            \time 2/4
            R1 * 1/2
            <a d' b'>16
            <bf d' a'>8.
            ~
            <bf d' a'>16
            d'16
            <a d' b'>8
            R1 * 1/2
            \time 7/16
            <bf d' a'>4
            d'16
            <a d' b'>8
            \time 3/16
            R1 * 3/16
            \time 7/16
            d'16
            <a d' b'>8
            <bf d' a'>4
            \time 3/16
            R1 * 3/16
            \time 9/16
            <a d' b'>8
            <bf d' a'>4
            <b d' g'>8.
            \time 3/16
            R1 * 3/16
            \time 2/4
            <bf d' a'>4
            <b d' g'>8.
            <c' d' e'>16
            \time 3/16
            R1 * 3/16
            \time 3/8
            <b d' g'>8.
            <c' d' e'>16
            <bf d' a'>8
            \time 3/16
            R1 * 3/16
        }

    ..  figure:: ../_images/example-2-looping-v5h9hyfmjj.png


Let's now remove the last empty bar, add this staff to an |abjad.Score| and
call the method :meth:`~auxjad.Score.add_final_bar_line()` which Auxjad adds to
|abjad.Score|.

    >>> staff.pop(-1)
    >>> score = abjad.Score([staff])
    >>> score.add_final_bar_line()

This is the final result:

    >>> abjad.show(score)

    ..  docs::

        \new Score
        <<
            \new Staff
            {
                \time 9/16
                <bf d' a'>16
                <a d' b'>8
                ~
                <a d' b'>16
                d'8
                ~
                d'8
                <b d' g'>16
                \time 2/4
                R1 * 1/2
                \time 5/8
                <a d' b'>8.
                d'8.
                ~
                d'16
                <b d' g'>16
                <bf d' a'>8
                \time 2/4
                R1 * 1/2
                \time 5/8
                d'4
                <b d' g'>16
                <bf d' a'>16
                ~
                <bf d' a'>16
                <c' d' e'>8.
                \time 2/4
                R1 * 1/2
                \time 7/16
                <b d' g'>16
                <bf d' a'>8
                <c' d' e'>8.
                <a d' b'>16
                \time 2/4
                R1 * 1/2
                \time 5/8
                <bf d' a'>8
                <c' d' e'>8.
                <a d' b'>16
                <bf d' a'>4
                \time 2/4
                R1 * 1/2
                \time 9/16
                <c' d' e'>8.
                <a d' b'>16
                <bf d' a'>8
                ~
                <bf d' a'>8
                d'16
                \time 2/4
                R1 * 1/2
                <a d' b'>16
                <bf d' a'>8.
                ~
                <bf d' a'>16
                d'16
                <a d' b'>8
                R1 * 1/2
                \time 7/16
                <bf d' a'>4
                d'16
                <a d' b'>8
                \time 3/16
                R1 * 3/16
                \time 7/16
                d'16
                <a d' b'>8
                <bf d' a'>4
                \time 3/16
                R1 * 3/16
                \time 9/16
                <a d' b'>8
                <bf d' a'>4
                <b d' g'>8.
                \time 3/16
                R1 * 3/16
                \time 2/4
                <bf d' a'>4
                <b d' g'>8.
                <c' d' e'>16
                \time 3/16
                R1 * 3/16
                \time 3/8
                <b d' g'>8.
                <c' d' e'>16
                <bf d' a'>8
                \bar "|."
            }
        >>

    ..  figure:: ../_images/example-2-looping-KzWUHdwdBN.png

.. include:: ../api/abjad-targets.rst
.. include:: ../api/auxjad-targets.rst
