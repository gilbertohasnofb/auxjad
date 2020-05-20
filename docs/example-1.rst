Example 1
---------

In this second example, we will use some of ``auxjad``'s classes to manipulate
some musical material using the looping and shuffling classes.

First, we start by importing both ``abjad`` and ``auxjad``.

    >>> import abjad
    >>> import auxjad

Let's now create a container with some arbitrary material to be manipulated.
Let's use the class ``auxjad.ArtificialHarmonic`` as well as some chords and
rests.

    >>> container = abjad.Staff([
    ...     auxjad.ArtificialHarmonic("<ds' gs'>4"),
    ...     auxjad.ArtificialHarmonic("<b ds'>8."),
    ...     auxjad.ArtificialHarmonic("<g c'>2.", is_parenthesized=True),
    ...     abjad.Rest("r4"),
    ...     abjad.Chord([0, 1, 7], (1, 8)),
    ...     auxjad.ArtificialHarmonic("<d' a'>2.", is_parenthesized=True),
    ... ])

Let's now add a time signature of the length of the container.

    >>> container_length = abjad.inspect(container).duration()
    >>> abjad.attach(abjad.TimeSignature(container_length), container[0])
    >>> abjad.f(container)
    \new Staff
    {
        \time 37/16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' cs' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >2.
    }

.. figure:: ./_images/image-example-1-1.png

The spelling of the chord ``<c' cs' g'>`` could be improved. This can be done
using either ``auxjad.respell_chord`` or ``auxjad.respell_container``.

    >>> auxjad.respell_container(container)
    >>> abjad.f(container)
    \new Staff
    {
        \time 37/16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >2.
    }

.. figure:: ./_images/image-example-1-2.png

Let's now use this material as input for ``auxjad.LoopByNotes``. This
is one of the many loopers included in ``auxjad``. It works by selecting groups
of _n_ elements (given by the argument ``window_size``). With ``window_size``
set to 4, this looper will first output the first four elements, then output
elements 2 through 5, then 3 through 6, and so on.

    >>> looper = auxjad.LoopByNotes(container, window_size=4)
    >>> staff = abjad.Staff()
    >>> for _ in range(3):
    ...     music = looper()
    ...     staff.append(music)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 23/16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        \time 21/16
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' df' g'>8
        \time 15/8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >2.
    }

.. figure:: ./_images/image-example-1-3.png

Let's now grab the last window output by the looper object above and use it as
input for ``auxjad.Shuffler``. This will randomly shuffles the leaves of
the input container.

    >>> container = abjad.Container(looper.current_window)
    >>> shuffler = auxjad.Shuffler(container, omit_time_signatures=True)
    >>> for _ in range(3):
    ...     music = shuffler()
    ...     staff.append(music)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 23/16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        \time 21/16
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' df' g'>8
        \time 15/8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >2.
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >2.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >4
        r8
        r8
        <c' df' g'>8
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        r4
    }

.. figure:: ./_images/image-example-1-4.png

To finalise the score, let's add an initial dynamic to the first leaf of the
staff.

    >>> abjad.attach(abjad.Dynamic('ppp'), staff[0])
    >>> abjad.f(staff)
    \new Staff
    {
        \time 23/16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        \ppp
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        \time 21/16
        <
            b
            \tweak style #'harmonic
            ds'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' df' g'>8
        \time 15/8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        r4
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >2.
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >2.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >4
        r8
        r8
        <c' df' g'>8
        <c' df' g'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >2
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >4.
        r4
    }

.. figure:: ./_images/image-example-1-5.png
