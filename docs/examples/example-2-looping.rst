Looping with :class:`auxjad.LeafLooper`
=======================================

In this first example, we will use the class :class:`auxjad.LeafLooper` to loop
through some musical material. This class creates subselections of logical
ties and has a looping window of variable size.

First, we start by importing both ``abjad`` and ``auxjad``.

    >>> import abjad
    >>> import auxjad

Let's now create a container with some arbitrary material to be manipulated
by the looper. For that, let's use :class:`auxjad.TenneySelector` to generate
the random material. This class is an implementation of the Dissonant
Counterpoint Algorithm by James Tenney. In a nutshell, this algorithm can be
used to randomly select elements from a list, giving priority to elements that
have not been chosen for the longest time. It also ensures that elements are
not repeated.

To start, we create two selectors, one for pitches and one for durations.

    >>> pitch_selector = auxjad.TenneySelector(["c'", "fs'", "bf'",
    ...                                         "e''", "a''", "d'''"])
    >>> duration_selector = auxjad.TenneySelector([(1, 16),
    ...                                            (2, 16),
    ...                                            (3, 16),
    ...                                            (4, 16),
    ...                                            (5, 16),
    ...                                            (6, 16),
    ...                                            ])

Let's now use those selectors to create twelve random notes, which will serve
as our basic material.

    >>> pitches = []
    >>> durations = []
    >>> for _ in range(12):
    ...     pitches.append(pitch_selector())
    ...     durations.append(duration_selector())

We can now use ``abjad.LeafMaker`` to convert those two lists of pitches and
durations into Notes. It's important to note that there is no time signature
being imposed at this point, so LilyPond will fallback to a four by four when
displaying the container below. This is not a problem since this will be used
as the basic material for the looper, which will then automatically take care
of time signatures.

    >>> notes = abjad.LeafMaker()(pitches, durations)
    >>> container = abjad.Container(notes)
    >>> abjad.f(container)
    {
        a''16
        d'''4
        ~
        d'''16
        c'4
        e''16
        bf'4
        fs'8.
        a''8
        d'''4
        ~
        d'''16
        c'16
        d'''4
        a''4.
        e''4
        ~
        e''16
    }

    .. figure:: ../_images/image-example-2-looping-1.png

At this point, we can create the :class:`auxjad.LeafLooper` and initialise it
using the material we generated above. A ``window_size`` of size ``4`` will
select four notes at each iteration.

    >>> looper = auxjad.LeafLooper(container, window_size=4)

We can now use the ``output_n()`` to output several measures of the looping
process for us. In this case, let's output seven measures.

    >>> staff = abjad.Staff(looper.output_n(7))
    >>> abjad.f(container)
    \new Staff
    {
        \time 11/16
        a''16
        d'''4
        ~
        d'''16
        c'4
        e''16
        \time 7/8
        d'''4
        ~
        d'''16
        c'4
        e''16
        bf'4
        \time 3/4
        c'4
        e''16
        bf'4
        fs'8.
        \time 5/8
        e''16
        bf'4
        fs'8.
        a''8
        \time 7/8
        bf'4
        fs'8.
        a''8
        d'''4
        ~
        d'''16
        \time 11/16
        fs'8.
        a''8
        d'''4
        ~
        d'''16
        c'16
        \time 3/4
        a''8
        d'''4
        ~
        d'''16
        c'16
        d'''4
    }

    .. figure:: ../_images/image-example-2-looping-2.png

At this point, let's change the ``window_size`` to a smaller value and output
some more measures.

    >>> looper.window_size = 2
    >>> staff.append(looper.output_n(4))

This is the final result.

    >>> abjad.f(container)
    \new Staff
    {
        \time 11/16
        a''16
        d'''4
        ~
        d'''16
        c'4
        e''16
        \time 7/8
        d'''4
        ~
        d'''16
        c'4
        e''16
        bf'4
        \time 3/4
        c'4
        e''16
        bf'4
        fs'8.
        \time 5/8
        e''16
        bf'4
        fs'8.
        a''8
        \time 7/8
        bf'4
        fs'8.
        a''8
        d'''4
        ~
        d'''16
        \time 11/16
        fs'8.
        a''8
        d'''4
        ~
        d'''16
        c'16
        \time 3/4
        a''8
        d'''4
        ~
        d'''16
        c'16
        d'''4
        \time 3/8
        d'''4
        ~
        d'''16
        c'16
        \time 5/16
        c'16
        d'''4
        \time 5/8
        d'''4
        a''4.
        \time 11/16
        a''4.
        e''4
        ~
        e''16
    }

    .. figure:: ../_images/image-example-2-looping-3.png
