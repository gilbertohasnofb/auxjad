Shuffling and fading harmonics
==============================

In this example, we will use some of |auxjad|_'s classes to manipulate
some musical material using the :class:`auxjad.Shuffler` and
:class:`auxjad.Fader` classes.

First, we start by importing both :mod:`abjad` and |auxjad|_.

    >>> import abjad
    >>> import auxjad

Let's now create a container with some arbitrary material to be manipulated.
Let's use the class :class:`auxjad.ArtificialHarmonic` as well as some chords
and rests.

    >>> container = abjad.Container([
    ...     auxjad.ArtificialHarmonic(r"<ds' gs'>4"),
    ...     auxjad.ArtificialHarmonic(r"<b e'>8."),
    ...     auxjad.ArtificialHarmonic(r"<g c'>16", is_parenthesized=True),
    ...     abjad.Rest(r"r4"),
    ...     abjad.Chord([2, 8, 9], (1, 8)),
    ...     auxjad.ArtificialHarmonic(r"<d' a'>8", is_parenthesized=True),
    ... ])
    >>> abjad.f(container)
    {
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        r4
        <d' af' a'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
    }

.. figure:: ../_images/image-example-5-shuffling-harmonics-1.png

The spelling of the chord ``<d' af' a'>`` could be improved. This can be done
by using either :func:`auxjad.respell_chord()` on that specific chord or
:func:`auxjad.respell_container()` on the whole container.

    >>> auxjad.respell_container(container)
    >>> abjad.f(container)
    {
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        r4
        <d' gs' a'>8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
    }

.. figure:: ../_images/image-example-5-shuffling-harmonics-2.png

Let's now use this material as input for :class:`auxjad.Shuffler`. This class
will randomly shuffle the logical ties of the input container.

    >>> shuffler = auxjad.Shuffler(container,
    ...                            disable_rewrite_meter=True,
    ...                            )

We can now use the method ``shuffle_n()`` to generate some measures of shuffled
logical ties.

    >>> staff = abjad.Staff()
    >>> notes = shuffler.shuffle_n(4)
    >>> staff.append(notes)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 4/4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        r8.
        r16
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        r4
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <
            b
            \tweak style #'harmonic
            e'
        >16
        ~
        <
            b
            \tweak style #'harmonic
            e'
        >8
        <d' gs' a'>8
        r4
    }

.. figure:: ../_images/image-example-5-shuffling-harmonics-3.png

We can now grab the last window output by shuffler and use it as the input
container of a :class:`auxjad.Fader`. When its ``fader_type`` is set to
``'out'``, it will remove a logical tie one by one at each iteration. Note how
:class:`auxjad.Fader` removes the notes of chords one by one, but consider an
:class:`auxjad.ArtificialHarmonic` as a single note.

    >>> container = abjad.Container(shuffler.current_window)
    >>> fader = auxjad.Fader(container, fader_type='out')

    >>> notes = fader.output_all()
    >>> staff.append(notes)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 4/4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        r8.
        r16
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        r4
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <
            b
            \tweak style #'harmonic
            e'
        >16
        ~
        <
            b
            \tweak style #'harmonic
            e'
        >8
        <d' gs' a'>8
        r4
        \time 4/4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        <
            b
            \tweak style #'harmonic
            e'
        >16
        ~
        <
            b
            \tweak style #'harmonic
            e'
        >8
        <d' gs' a'>8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        r16
        r8
        <d' gs' a'>8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        r16
        r8
        <d' gs'>8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        r16
        r8
        gs'8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        r16
        r2
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        ~
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >16
        r16
        r2
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        r8.
        r2
        R1
    }

.. figure:: ../_images/image-example-5-shuffling-harmonics-4.png

To finalise the score, let's improve the spelling of some rhythms. Most classes
and functions in this library use |abjad.mutate().rewrite_meter()| mutation
to adjust the spelling of rhythms according to a meter. Unfortunately, this
mutation sometimes uses ties within a single beat, resulting in rhythms that
are less ideally notated than they could.
:func:`auxjad.prettify_rewrite_meter()` fuses pitched leaves according to some
specific rules, improving the default output of
|abjad.mutate().rewrite_meter()|.

Notice that the time signature has been repeated. While the ``output_n()``
method takes care of repeated time signatures, dynamics, and clefs, consecutive
calls may result in repetitions. But we can simply use
:func:`auxjad.remove_repeated_time_signatures()` to take care of that for us.

    >>> auxjad.prettify_rewrite_meter(staff, meter=abjad.Meter((4, 4)))
    >>> auxjad.remove_repeated_time_signatures(staff)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 4/4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        r8.
        r16
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        r4
        <
            b
            \tweak style #'harmonic
            e'
        >8.
        <d' gs' a'>16
        ~
        <d' gs' a'>16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        <
            b
            \tweak style #'harmonic
            e'
        >16
        ~
        <
            b
            \tweak style #'harmonic
            e'
        >8
        <d' gs' a'>8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        <
            b
            \tweak style #'harmonic
            e'
        >16
        ~
        <
            b
            \tweak style #'harmonic
            e'
        >8
        <d' gs' a'>8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        r16
        r8
        <d' gs' a'>8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        r16
        r8
        <d' gs'>8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        r16
        r8
        gs'8
        r4
        <
            ds'
            \tweak style #'harmonic
            gs'
        >4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        r16
        r2
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            d'
            \tweak style #'harmonic
            a'
        >8
        r16
        r2
        r4
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >16
        r8.
        r2
        R1
    }

.. figure:: ../_images/image-example-5-shuffling-harmonics-5.png

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: ../api/index.html

.. include:: ../api/abjad-targets.rst
