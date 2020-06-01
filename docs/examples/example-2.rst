Example 2
---------

In this second example, we will use some of ``auxjad``'s' classes to generate
a container of randomly selected material, and then use this material as input
for the looping and shuffling classes.

First, we start by importing both ``abjad`` and ``auxjad``.

    >>> import abjad
    >>> import auxjad

Let's start by deciding what random selectors will be responsible for
generating each parameter of our basic material. Let's use
``auxjad.TenneySelector`` for pitches, which is an implementation of Tenney's
Dissonant Counterpoint Algorithm; at each call, this algorithm prioritises
elements that haven't been select for the longest time. For the durations,
dynamics, and articulations, the example will use
``auxjad.CartographySelector``. Each element input into this type of selector
has a probability of being selected which is dependent on its index. By
default, the probability of consecutive elements decay with a rate of 0.75. For
more information on both of these classes, check the ``auxjad`` API page (link
in the left panel).

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

With these lists of pitches, durations, dynamics, and articulations, we can now
use ``auxjad.LeafDynMaker`` to create the individual abjad leaves for us.

    >>> leaf_dyn_maker = auxjad.LeafDynMaker()
    >>> notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    >>> container = abjad.Staff(notes)

Let's now add a time signature of the length of the container.

    >>> container_length = abjad.inspect(container).duration()
    >>> abjad.attach(abjad.TimeSignature(container_length), container[0])
    >>> abjad.f(container)
    \new Staff
    {
        \time 13/4
        c'2
        \mp
        - \tenuto
        ~
        c'8
        af'4.
        \mp
        bf'4.
        \mf
        - \tenuto
        c'4.
        \mp
        d'4.
        \mf
        - \accent
        ef'4
        \p
        - \accent
        af'2
        \mp
        ~
        af'8
        c'4
        \mp
        - \accent
    }

.. figure:: ../_images/image-example-2-1.png

Let's now use ``auxjad.LoopByWindow`` to output loops of windows of the material.
By default, this class uses a window size of a 4/4 measure, and each step
forward has the size of a sixteenth-note. These parameters are all adjustable,
please refer to this library's API for more information.

    >>> looper = auxjad.LoopByWindow(container)
    >>> staff = abjad.Staff()
    >>> for _ in range(3):
    >>>     music = looper()
    >>>     staff.append(music)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 4/4
        c'2
        \mp
        - \tenuto
        ~
        c'8
        af'4.
        \mp
        c'2
        \mp
        - \tenuto
        ~
        c'16
        af'8.
        \mp
        ~
        af'8.
        bf'16
        \mf
        - \tenuto
        c'2
        \mp
        - \tenuto
        af'4.
        \mp
        bf'8
        \mf
        - \tenuto
    }

.. figure:: ../_images/image-example-2-2.png

Let's now grab the last window output by the looper object above and use it as
input for ``auxjad.Shuffler``. This will randomly shuffles the leaves of
the input container.

    >>> container = abjad.Container(looper.current_window)
    >>> shuffler = auxjad.Shuffler(container, omit_time_signatures=True)
    >>> for _ in range(3):
    >>>     music = shuffler()
    >>>     staff.append(music)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 4/4
        c'2
        \mp
        - \tenuto
        ~
        c'8
        af'4.
        \mp
        c'2
        \mp
        - \tenuto
        ~
        c'16
        af'8.
        \mp
        ~
        af'8.
        bf'16
        \mf
        - \tenuto
        c'2
        \mp
        - \tenuto
        af'4.
        \mp
        bf'8
        \mf
        - \tenuto
        bf'8
        \mf
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'4.
        \mp
        c'2
        \mp
        - \tenuto
        bf'8
        \mf
        - \tenuto
        af'4.
        \mp
        bf'8
        \mf
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'4.
        \mp
    }

.. figure:: ../_images/image-example-2-3.png

Let's use the last output of the shuffler above and feed it into a new looper.
This time we will use a window of size 3/4.

    >>> container = abjad.Container(shuffler.current_container)
    >>> looper = auxjad.LoopByWindow(container,
    ...                            window_size=(3, 4),
    ...                            )
    >>> for _ in range(3):
    >>>     music = looper()
    >>>     staff.append(music)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 4/4
        c'2
        \mp
        - \tenuto
        ~
        c'8
        af'4.
        \mp
        c'2
        \mp
        - \tenuto
        ~
        c'16
        af'8.
        \mp
        ~
        af'8.
        bf'16
        \mf
        - \tenuto
        c'2
        \mp
        - \tenuto
        af'4.
        \mp
        bf'8
        \mf
        - \tenuto
        bf'8
        \mf
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'4.
        \mp
        c'2
        \mp
        - \tenuto
        bf'8
        \mf
        - \tenuto
        af'4.
        \mp
        bf'8
        \mf
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'4.
        \mp
        \time 3/4
        bf'8
        \mf
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'8
        \mp
        bf'16
        \mf
        - \tenuto
        c'8.
        \mp
        - \tenuto
        ~
        c'4
        ~
        c'16
        af'8.
        \mp
        c'2
        \mp
        - \tenuto
        af'4
        \mp
    }

.. figure:: ../_images/image-example-2-4.png

At this point, let's use ``auxjad.remove_repeated_dynamics`` to remove all
repeated dyanmics. The final result is shown below.

    >>> auxjad.remove_repeated_dynamics(staff)
    >>> abjad.f(staff)
    \new Staff
    {
        \time 4/4
        c'2
        \mp
        - \tenuto
        ~
        c'8
        af'4.
        c'2
        - \tenuto
        ~
        c'16
        af'8.
        ~
        af'8.
        bf'16
        \mf
        - \tenuto
        c'2
        \mp
        - \tenuto
        af'4.
        bf'8
        \mf
        - \tenuto
        bf'8
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'4.
        c'2
        - \tenuto
        bf'8
        \mf
        - \tenuto
        af'4.
        \mp
        bf'8
        \mf
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'4.
        \time 3/4
        bf'8
        \mf
        - \tenuto
        c'8
        \mp
        - \tenuto
        ~
        c'4.
        af'8
        bf'16
        \mf
        - \tenuto
        c'8.
        \mp
        - \tenuto
        ~
        c'4
        ~
        c'16
        af'8.
        c'2
        - \tenuto
        af'4
    }

.. figure:: ../_images/image-example-2-5.png
