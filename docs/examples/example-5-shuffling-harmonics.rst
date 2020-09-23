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

.. figure:: ../_images/example-5-shuffling-harmonics-vuu4ho4hjk7.png

The spelling of the chord ``<d' af' a'>`` could be improved. This can be done
by using either |auxjad.mutate().respell_accidentals()| on a selection. Auxjad
automatically adds this mutation as an extension method to |abjad.mutate()| so
it can also be accessed using |abjad.mutate().respell_accidentals()|.

    >>> abjad.mutate(container[:]).respell_accidentals()
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

.. figure:: ../_images/example-5-shuffling-harmonics-yast6lxvpz.png

Let's now use this material as input for :class:`auxjad.Shuffler`. This class
will randomly shuffle the logical ties of the input container.

    >>> shuffler = auxjad.Shuffler(container,
    ...                            disable_rewrite_meter=True,
    ...                            )

We can now use the method :meth:`~auxjad.Shuffler.shuffle_n` to generate some
measures of shuffled logical ties.

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

.. figure:: ../_images/example-5-shuffling-harmonics-rnpvdobaxw.png

We can now grab the last window output by shuffler and use it as the input
container of a :class:`auxjad.Fader`. When its property
:attr:`~auxjad.Fader.fader_type` is set to ``'out'``, it will remove a logical
tie one by one at each iteration. Note how :class:`auxjad.Fader` removes the
notes of chords one by one, but consider an :class:`auxjad.ArtificialHarmonic`
as a single note.

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

.. figure:: ../_images/example-5-shuffling-harmonics-1rxgv2my0lr.png

To finalise the score, let's improve the spelling of some rhythms. Most classes
and functions in this library use |abjad.mutate().rewrite_meter()| mutation
to adjust the spelling of rhythms according to a meter. Unfortunately, this
mutation sometimes uses ties within a single beat, resulting in rhythms that
are less ideally notated than they could.
|auxjad.mutate().prettify_rewrite_meter()| fuses pitched leaves according to
some specific rules, improving the default output of
|abjad.mutate().rewrite_meter()|. This function is also available as the method
|abjad.mutate().prettify_rewrite_meter()|, which Auxjad automatically adds as
an extension method to |abjad.mutate()|.

Notice that the time signature has been repeated. While the method
:meth:`~auxjad.Fader.output_all()` takes care of repeated time signatures,
dynamics, and clefs, consecutive calls may result in repetitions. But we can
simply use |auxjad.mutate().remove_repeated_time_signatures()| to take care of
that for us. This function is also available as the extension method
|abjad.mutate().remove_repeated_time_signatures()|, which Auxjad automatically
adds to |abjad.mutate()|.

    >>> abjad.mutate(staff[:]).prettify_rewrite_meter(abjad.Meter((4, 4)))
    >>> abjad.mutate(staff[:]).remove_repeated_time_signatures()
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

.. figure:: ../_images/example-5-shuffling-harmonics-rmw99goyuc.png

.. include:: ../api/abjad-targets.rst
.. include:: ../api/auxjad-targets.rst
