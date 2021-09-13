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

    >>> pitch_selector = auxjad.TenneySelector(["c'",
    ...                                         ("fs'", "g'"),
    ...                                         "ef''",
    ...                                         "a''",
    ...                                         ("b", "bf''"),
    ...                                         ])
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
            <b bf''>4.
            \f
            c'4.
            \f
            ef''4
            \mf
            c'4.
            \mf
            - \tenuto
            <fs' g'>4
            \f
            a''4.
            \p
            <b bf''>2
            \p
            ~
            <b bf''>8
            <fs' g'>2
            \p
            - \tenuto
            ~
            <fs' g'>8
        }

    ..  figure:: ../_images/example-3-looping-wcsvsyfmwm.png

Let's now use :class:`auxjad.WindowLooper` to output loops of windows of the
material. Let's initiate this class with a window size of a 4/4 measure, and a
step forward of a semiquaver. Setting
:attr:`~auxjad.LeafLooper.after_rest` to the duration ``(1, 4)`` will add
crotchet rests in between consecutive outputs of this looper. Setting
:attr:`~auxjad.LeafLooper.after_rest_in_new_measure` to ``True`` ensure that
these rests (which work as separators of consecutive windows) are in a new
measure by themselves.

    >>> looper = auxjad.WindowLooper(container,
    ...                              window_size=(4, 4),
    ...                              step_size=(1, 16),
    ...                              after_rest=(1, 4),
    ...                              after_rest_in_new_measure=True,
    ...                              )

We can now use the :meth:`~auxjad.WindowLooper.output_n` to output several
measures of the looping process for us. In this case, let's output four
measures.

    >>> staff = abjad.Staff()
    >>> notes = looper.output_n(4)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 4/4
            <b bf''>4.
            \f
            c'8
            ~
            c'4
            ef''4
            \mf
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>4
            \f
            ~
            <b bf''>16
            c'8.
            ~
            c'8.
            ef''16
            \mf
            ~
            ef''8.
            c'16
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>4
            \f
            c'4
            ~
            c'8
            ef''4
            \mf
            c'8
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>8.
            \f
            c'16
            ~
            c'4
            ~
            c'16
            ef''8.
            \mf
            ~
            ef''16
            c'8.
            - \tenuto
            \time 1/4
            R1 * 1/4
        }

    ..  figure:: ../_images/example-3-looping-002erek662ml6.png

Let's now change the values of :attr:`~auxjad.WindowLooper.step_size` from a
semiquaver into a crotchet and output four more measures.

    >>> looper.step_size = (1, 4)
    >>> notes = looper.output_n(4)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 4/4
            <b bf''>4.
            \f
            c'8
            ~
            c'4
            ef''4
            \mf
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>4
            \f
            ~
            <b bf''>16
            c'8.
            ~
            c'8.
            ef''16
            \mf
            ~
            ef''8.
            c'16
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>4
            \f
            c'4
            ~
            c'8
            ef''4
            \mf
            c'8
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>8.
            \f
            c'16
            ~
            c'4
            ~
            c'16
            ef''8.
            \mf
            ~
            ef''16
            c'8.
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            c'4
            \f
            ~
            c'16
            ef''8.
            \mf
            ~
            ef''16
            c'8.
            - \tenuto
            ~
            c'8.
            <fs' g'>16
            \f
            \time 1/4
            R1 * 1/4
            \time 4/4
            c'16
            ef''8.
            \mf
            ~
            ef''16
            c'8.
            - \tenuto
            ~
            c'8.
            <fs' g'>16
            \f
            ~
            <fs' g'>8.
            a''16
            \p
            \time 1/4
            R1 * 1/4
            \time 4/4
            ef''16
            \mf
            c'8.
            - \tenuto
            ~
            c'8.
            <fs' g'>16
            \f
            ~
            <fs' g'>8.
            a''16
            \p
            ~
            a''4
            \time 1/4
            R1 * 1/4
            \time 4/4
            c'8.
            \mf
            - \tenuto
            <fs' g'>16
            \f
            ~
            <fs' g'>8.
            a''16
            \p
            ~
            a''4
            ~
            a''16
            <b bf''>8.
            \time 1/4
            R1 * 1/4
        }

    ..  figure:: ../_images/example-3-looping-qodelstkbvo.png

Let's now change both :attr:`~auxjad.WindowLooper.window_size` and
:attr:`~auxjad.WindowLooper.step_size` as well as remove the after rests, and
then output six more measures.

    >>> looper.window_size = (7, 8)
    >>> looper.step_size = (1, 16)
    >>> looper.after_rest = 0
    >>> notes = looper.output_n(6)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \time 4/4
            <b bf''>4.
            \f
            c'8
            ~
            c'4
            ef''4
            \mf
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>4
            \f
            ~
            <b bf''>16
            c'8.
            ~
            c'8.
            ef''16
            \mf
            ~
            ef''8.
            c'16
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>4
            \f
            c'4
            ~
            c'8
            ef''4
            \mf
            c'8
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            <b bf''>8.
            \f
            c'16
            ~
            c'4
            ~
            c'16
            ef''8.
            \mf
            ~
            ef''16
            c'8.
            - \tenuto
            \time 1/4
            R1 * 1/4
            \time 4/4
            c'4
            \f
            ~
            c'16
            ef''8.
            \mf
            ~
            ef''16
            c'8.
            - \tenuto
            ~
            c'8.
            <fs' g'>16
            \f
            \time 1/4
            R1 * 1/4
            \time 4/4
            c'16
            ef''8.
            \mf
            ~
            ef''16
            c'8.
            - \tenuto
            ~
            c'8.
            <fs' g'>16
            \f
            ~
            <fs' g'>8.
            a''16
            \p
            \time 1/4
            R1 * 1/4
            \time 4/4
            ef''16
            \mf
            c'8.
            - \tenuto
            ~
            c'8.
            <fs' g'>16
            \f
            ~
            <fs' g'>8.
            a''16
            \p
            ~
            a''4
            \time 1/4
            R1 * 1/4
            \time 4/4
            c'8.
            \mf
            - \tenuto
            <fs' g'>16
            \f
            ~
            <fs' g'>8.
            a''16
            \p
            ~
            a''4
            ~
            a''16
            <b bf''>8.
            \time 1/4
            R1 * 1/4
            \time 7/8
            c'8
            \mf
            - \tenuto
            <fs' g'>4
            \f
            a''4.
            \p
            <b bf''>8
            c'16
            \mf
            - \tenuto
            <fs' g'>16
            \f
            ~
            <fs' g'>8.
            a''16
            \p
            ~
            a''4
            ~
            a''16
            <b bf''>8.
            <fs' g'>4
            \f
            a''4.
            \p
            <b bf''>4
            <fs' g'>8.
            \f
            a''8.
            \p
            ~
            a''8.
            <b bf''>16
            ~
            <b bf''>4
            <fs' g'>8
            \f
            a''4
            \p
            ~
            a''8
            <b bf''>4.
            <fs' g'>16
            \f
            a''16
            \p
            ~
            a''4
            ~
            a''16
            <b bf''>4..
        }

    ..  figure:: ../_images/example-3-looping-snpku7bedo.png

Let's now add this staff to an |abjad.Score| and call the method
:meth:`~auxjad.Score.add_final_bar_line()` which Auxjad adds to |abjad.Score|.

    >>> score = abjad.Score([staff])
    >>> score.add_final_bar_line()

The final result is shown below.

    >>> abjad.show(score)

    ..  docs::

        \new Score
        <<
            \new Staff
            {
                \time 4/4
                <b bf''>4.
                \f
                c'8
                ~
                c'4
                ef''4
                \mf
                \time 1/4
                R1 * 1/4
                \time 4/4
                <b bf''>4
                \f
                ~
                <b bf''>16
                c'8.
                ~
                c'8.
                ef''16
                \mf
                ~
                ef''8.
                c'16
                - \tenuto
                \time 1/4
                R1 * 1/4
                \time 4/4
                <b bf''>4
                \f
                c'4
                ~
                c'8
                ef''4
                \mf
                c'8
                - \tenuto
                \time 1/4
                R1 * 1/4
                \time 4/4
                <b bf''>8.
                \f
                c'16
                ~
                c'4
                ~
                c'16
                ef''8.
                \mf
                ~
                ef''16
                c'8.
                - \tenuto
                \time 1/4
                R1 * 1/4
                \time 4/4
                c'4
                \f
                ~
                c'16
                ef''8.
                \mf
                ~
                ef''16
                c'8.
                - \tenuto
                ~
                c'8.
                <fs' g'>16
                \f
                \time 1/4
                R1 * 1/4
                \time 4/4
                c'16
                ef''8.
                \mf
                ~
                ef''16
                c'8.
                - \tenuto
                ~
                c'8.
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                \time 1/4
                R1 * 1/4
                \time 4/4
                ef''16
                \mf
                c'8.
                - \tenuto
                ~
                c'8.
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                ~
                a''4
                \time 1/4
                R1 * 1/4
                \time 4/4
                c'8.
                \mf
                - \tenuto
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                ~
                a''4
                ~
                a''16
                <b bf''>8.
                \time 1/4
                R1 * 1/4
                \time 7/8
                c'8
                \mf
                - \tenuto
                <fs' g'>4
                \f
                a''4.
                \p
                <b bf''>8
                c'16
                \mf
                - \tenuto
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                ~
                a''4
                ~
                a''16
                <b bf''>8.
                <fs' g'>4
                \f
                a''4.
                \p
                <b bf''>4
                <fs' g'>8.
                \f
                a''8.
                \p
                ~
                a''8.
                <b bf''>16
                ~
                <b bf''>4
                <fs' g'>8
                \f
                a''4
                \p
                ~
                a''8
                <b bf''>4.
                <fs' g'>16
                \f
                a''16
                \p
                ~
                a''4
                ~
                a''16
                <b bf''>4..
                \bar "|."
            }
        >>

    ..  figure:: ../_images/example-3-looping-16f4hdprg8k.png

.. include:: ../api/abjad-targets.rst
.. include:: ../api/auxjad-targets.rst
