Looping with :class:`auxjad.WindowLooper`
=========================================

In this next example, we will use some of |auxjad|_'s classes to generate
a container of randomly selected material, and then use this material as input
for the looping and shuffling classes.

First, we start by importing both :mod:`abjad` and |auxjad|_.

    >>> import abjad
    >>> import auxjad

Let's start by deciding what random selectors will be responsible for
generating each parameter of our basic material. Let's use
:class:`auxjad.TenneySelector` for pitches, which is an implementation of
Tenney's Dissonant Counterpoint Algorithm; at each call, this algorithm
prioritises elements that haven't been select for the longest time. For the
durations, dynamics, and articulations, the example will use
:class:`auxjad.CartographySelector`. Each element input into this type of
selector has a probability of being selected which is dependent on its index.
By default, the probability of consecutive elements decay with a rate of
``0.75``. For more information on both of these classes, check |auxjad|_'s API
page (link in the left panel).

    >>> pitch_selector = auxjad.TenneySelector([0, 7, 8, 2, 3, 10])
    >>> duration_selector = auxjad.CartographySelector([(2, 8),
    ...                                                 (3, 8),
    ...                                                 (5, 8),
    ...                                                 ])
    >>> dynamic_selector = auxjad.CartographySelector(['p', 'mp', 'mf', 'f'])
    >>> articulation_selector = auxjad.CartographySelector([None, '-', '>'])

Let's now create eight random notes, each with four parameters randomly
selected by the classes above.

    >>> pitches = [pitch_selector() for _ in range(8)]
    >>> durations = [duration_selector() for _ in range(8)]
    >>> dynamics = [dynamic_selector() for _ in range(8)]
    >>> articulations = [articulation_selector() for _ in range(8)]

With these :obj:`list`'s' of pitches, durations, dynamics, and articulations,
we can now use :class:`auxjad.LeafDynMaker` to create the individual abjad
leaves for us. It's important to note that there is no time signature being
imposed at this point, so LilyPond will fallback to a four by four when
displaying the container below. This is not a problem since this will be used
as the basic material for the looper, which will then automatically take care
of time signatures.

    >>> leaf_dyn_maker = auxjad.LeafDynMaker()
    >>> notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    >>> container = abjad.Container(notes)
    >>> abjad.show(container)

    ..  docs::

        {
            bf'4.
            \f
            g'4.
            \f
            af'4
            \mf
            c'4.
            \mf
            - \tenuto
            g'4
            \f
            ef'4.
            \p
            bf'2
            \p
            ~
            bf'8
            af'2
            \p
            - \tenuto
            ~
            af'8
        }

    ..  figure:: ../_images/example-3-looping-wcsvsyfmwm.png

Let's now use :class:`auxjad.WindowLooper` to output loops of windows of the
material. By default, this class uses a window size of a 4/4 measure, and each
step forward has the size of a semiquaver, but we will adjust those to a 5/4
time signature and a crotchet for the step size. Please refer to this library's
API for more information.

    >>> looper = auxjad.WindowLooper(container,
    ...                              window_size=(5, 4),
    ...                              step_size=(1, 4),
    ...                              )

We can now use the :meth:`~auxjad.WindowLooper.output_n` to output several
measures of the looping process for us. In this case, let's output six measures.

    >>> staff = abjad.Staff()
    >>> notes = looper.output_n(6)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 5/4
            bf'4.
            \f
            g'4.
            af'4
            \mf
            c'4
            - \tenuto
            bf'8
            \f
            g'4.
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            g'4
            af'4
            \mf
            c'4
            - \tenuto
            ~
            c'8
            g'4
            \f
            ef'8
            \p
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            ~
            g'8
            ef'4.
            \p
            c'4.
            \mf
            - \tenuto
            g'4
            \f
            ef'8
            \p
            ~
            ef'4
            bf'4
            c'8
            \mf
            - \tenuto
            g'4
            \f
            ef'4.
            \p
            bf'2
        }

    ..  figure:: ../_images/example-3-looping-002erek662ml6.png

Let's now change the value of :attr:`~auxjad.WindowLooper.step_size` from a
crotchet into a semiquaver and output six more measures.

    >>> looper.step_size = (1, 16)
    >>> notes = looper.output_n(6)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 5/4
            bf'4.
            \f
            g'4.
            af'4
            \mf
            c'4
            - \tenuto
            bf'8
            \f
            g'4.
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            g'4
            af'4
            \mf
            c'4
            - \tenuto
            ~
            c'8
            g'4
            \f
            ef'8
            \p
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            ~
            g'8
            ef'4.
            \p
            c'4.
            \mf
            - \tenuto
            g'4
            \f
            ef'8
            \p
            ~
            ef'4
            bf'4
            c'8
            \mf
            - \tenuto
            g'4
            \f
            ef'4.
            \p
            bf'2
            \time 5/4
            c'16
            \mf
            - \tenuto
            g'8.
            \f
            ~
            g'16
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4..
            ~
            bf'16
            g'4
            \f
            ef'4.
            \p
            bf'8
            ~
            bf'4.
            ~
            bf'8
            g'8.
            \f
            ef'16
            \p
            ~
            ef'4
            ~
            ef'16
            bf'8.
            ~
            bf'4
            ~
            bf'16
            ~
            bf'8
            af'16
            - \tenuto
            g'8
            \f
            ef'4.
            \p
            bf'4
            ~
            bf'4
            ~
            bf'8
            af'8
            - \tenuto
            g'16
            \f
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4
            ~
            bf'4
            ~
            bf'16
            af'8.
            - \tenuto
            ef'4.
            bf'4.
            ~
            bf'4
            af'4
            - \tenuto
        }

    ..  figure:: ../_images/example-3-looping-qodelstkbvo.png

Notice that the time signature has been repeated. While the method
:meth:`~auxjad.WindowLooper.output_n()` takes care of repeated time signatures,
dynamics, and clefs, consecutive calls may result in repetitions. But we can
simply use |auxjad.mutate.remove_repeated_time_signatures()| to take care of
that for us. This function is also available as the extension method
|abjad.mutate.remove_repeated_time_signatures()| which Auxjad automatically
adds to |abjad.mutate|.


    >>> abjad.mutate.remove_repeated_time_signatures(staff[:])
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 5/4
            bf'4.
            \f
            g'4.
            af'4
            \mf
            c'4
            - \tenuto
            bf'8
            \f
            g'4.
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            g'4
            af'4
            \mf
            c'4
            - \tenuto
            ~
            c'8
            g'4
            \f
            ef'8
            \p
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            ~
            g'8
            ef'4.
            \p
            c'4.
            \mf
            - \tenuto
            g'4
            \f
            ef'8
            \p
            ~
            ef'4
            bf'4
            c'8
            \mf
            - \tenuto
            g'4
            \f
            ef'4.
            \p
            bf'2
            c'16
            \mf
            - \tenuto
            g'8.
            \f
            ~
            g'16
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4..
            ~
            bf'16
            g'4
            \f
            ef'4.
            \p
            bf'8
            ~
            bf'4.
            ~
            bf'8
            g'8.
            \f
            ef'16
            \p
            ~
            ef'4
            ~
            ef'16
            bf'8.
            ~
            bf'4
            ~
            bf'16
            ~
            bf'8
            af'16
            - \tenuto
            g'8
            \f
            ef'4.
            \p
            bf'4
            ~
            bf'4
            ~
            bf'8
            af'8
            - \tenuto
            g'16
            \f
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4
            ~
            bf'4
            ~
            bf'16
            af'8.
            - \tenuto
            ef'4.
            bf'4.
            ~
            bf'4
            af'4
            - \tenuto
        }

    ..  figure:: ../_images/example-3-looping-5vih5zhn6de.png

Let's now change the :attr:`~auxjad.WindowLooper.window_size` and output some
more measures.

    >>> looper.window_size = (3, 4)
    >>> notes = looper.output_n(6)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 5/4
            bf'4.
            \f
            g'4.
            af'4
            \mf
            c'4
            - \tenuto
            bf'8
            \f
            g'4.
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            g'4
            af'4
            \mf
            c'4
            - \tenuto
            ~
            c'8
            g'4
            \f
            ef'8
            \p
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            ~
            g'8
            ef'4.
            \p
            c'4.
            \mf
            - \tenuto
            g'4
            \f
            ef'8
            \p
            ~
            ef'4
            bf'4
            c'8
            \mf
            - \tenuto
            g'4
            \f
            ef'4.
            \p
            bf'2
            c'16
            \mf
            - \tenuto
            g'8.
            \f
            ~
            g'16
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4..
            ~
            bf'16
            g'4
            \f
            ef'4.
            \p
            bf'8
            ~
            bf'4.
            ~
            bf'8
            g'8.
            \f
            ef'16
            \p
            ~
            ef'4
            ~
            ef'16
            bf'8.
            ~
            bf'4
            ~
            bf'16
            ~
            bf'8
            af'16
            - \tenuto
            g'8
            \f
            ef'4.
            \p
            bf'4
            ~
            bf'4
            ~
            bf'8
            af'8
            - \tenuto
            g'16
            \f
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4
            ~
            bf'4
            ~
            bf'16
            af'8.
            - \tenuto
            ef'4.
            bf'4.
            ~
            bf'4
            af'4
            - \tenuto
            \time 3/4
            ef'4
            \p
            ~
            ef'16
            bf'4..
            ef'4
            bf'2
            ef'8.
            bf'16
            ~
            bf'2
            ef'8
            bf'8
            ~
            bf'2
            ef'16
            bf'8.
            ~
            bf'4..
            af'16
            - \tenuto
            bf'2
            ~
            bf'8
            af'8
            - \tenuto
        }

    ..  figure:: ../_images/example-3-looping-snpku7bedo.png

At this point, let's use |auxjad.mutate.remove_repeated_dynamics()| to remove
all repeated dynamics. While the method :meth:`~auxjad.WindowLooper.output_n()`
removes repeated dynamics, clefs, and time signatures, this is necessary
because our example invoked :meth:`~auxjad.WindowLooper.output_n()` multiple
times, and there is a repetition of a dynamic at that transition. This function
is also available as the extension method
|abjad.mutate.remove_repeated_dynamics()|, which Auxjad automatically adds to
|abjad.mutate|.

The final result is shown below.

    >>> abjad.mutate.remove_repeated_dynamics(staff[:])
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 5/4
            bf'4.
            \f
            g'4.
            af'4
            \mf
            c'4
            - \tenuto
            bf'8
            \f
            g'4.
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            g'4
            af'4
            \mf
            c'4
            - \tenuto
            ~
            c'8
            g'4
            \f
            ef'8
            \p
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            ~
            g'8
            ef'4.
            \p
            c'4.
            \mf
            - \tenuto
            g'4
            \f
            ef'8
            \p
            ~
            ef'4
            bf'4
            c'8
            \mf
            - \tenuto
            g'4
            \f
            ef'4.
            \p
            bf'2
            c'16
            \mf
            - \tenuto
            g'8.
            \f
            ~
            g'16
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4..
            ~
            bf'16
            g'4
            \f
            ef'4.
            \p
            bf'8
            ~
            bf'4.
            ~
            bf'8
            g'8.
            \f
            ef'16
            \p
            ~
            ef'4
            ~
            ef'16
            bf'8.
            ~
            bf'4
            ~
            bf'16
            ~
            bf'8
            af'16
            - \tenuto
            g'8
            \f
            ef'4.
            \p
            bf'4
            ~
            bf'4
            ~
            bf'8
            af'8
            - \tenuto
            g'16
            \f
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4
            ~
            bf'4
            ~
            bf'16
            af'8.
            - \tenuto
            ef'4.
            bf'4.
            ~
            bf'4
            af'4
            - \tenuto
            \time 3/4
            ef'4
            ~
            ef'16
            bf'4..
            ef'4
            bf'2
            ef'8.
            bf'16
            ~
            bf'2
            ef'8
            bf'8
            ~
            bf'2
            ef'16
            bf'8.
            ~
            bf'4..
            af'16
            - \tenuto
            bf'2
            ~
            bf'8
            af'8
            - \tenuto
        }

    ..  figure:: ../_images/example-3-looping-16f4hdprg8k.png

.. include:: ../api/abjad-targets.rst
.. include:: ../api/auxjad-targets.rst
