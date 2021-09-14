Random repetitions
==================

In this example, we will use some of |auxjad|_'s classes to generate random
repeated measures.

First, we start by importing both :mod:`abjad` and |auxjad|_.

    >>> import abjad
    >>> import auxjad

First, let's create a container with an arbitrary rhythm. The pitches do not
matter at this point since we will randomise them shortly.

    >>> container = abjad.Container(
    ...     r"c'4-- c'8.-- c'16( c'8)-. c'8-. c'8-. r8"
    ... )
    >>> abjad.show(container)

    ..  docs::

        {
            c'4
            - \tenuto
            c'8.
            - \tenuto
            c'16
            (
            c'8
            - \staccato
            )
            c'8
            - \staccato
            c'8
            - \staccato
            r8
        }

    ..  figure:: ../_images/example-4-random-repetitions-h990mzwoa7f.png

Next, let's initialise :class:`auxjad.PitchRandomiser` with this container as
well as a :obj:`list` representing pitches. This will be the source for the
random pitches selected by this randomiser.

    >>> pitch_list = ["c'", "cs'", "d'", "ef'", "e'"]
    >>> randomiser = auxjad.PitchRandomiser(container,
    ...                                     pitches=pitch_list,
    ...                                     )

Let's now output a first group of two measures with random pitches using the
method :meth:`auxjad.PitchRandomiser.output_n`.

    >>> notes = randomiser.output_n(2)
    >>> group_1 = abjad.Staff(notes)
    >>> abjad.show(group_1)

    ..  docs::

        \new Staff
        {
            d'4
            - \tenuto
            c'8.
            - \tenuto
            e'16
            (
            e'8
            - \staccato
            )
            cs'8
            - \staccato
            ef'8
            - \staccato
            r8
            cs'4
            - \tenuto
            ef'8.
            - \tenuto
            e'16
            (
            ef'8
            - \staccato
            )
            e'8
            - \staccato
            d'8
            - \staccato
            r8
        }

    ..  figure:: ../_images/example-4-random-repetitions-5s17pjm02j5.png

Let's now change the pitch :obj:`list` using the property
:attr:`~auxjad.PitchRandomiser.pitches` of the randomiser and create another
group of measures.

    >>> randomiser.pitches = ["a", "b", "bf'", "a''", "b''"]
    >>> notes = randomiser.output_n(2)
    >>> group_2 = abjad.Staff(notes)
    >>> abjad.show(group_2)

    ..  docs::

        \new Staff
        {
            a4
            - \tenuto
            a8.
            - \tenuto
            a16
            (
            b''8
            - \staccato
            )
            b''8
            - \staccato
            a''8
            - \staccato
            r8
            b''4
            - \tenuto
            b8.
            - \tenuto
            a16
            (
            a8
            - \staccato
            )
            bf'8
            - \staccato
            a8
            - \staccato
            r8
        }

    ..  figure:: ../_images/example-4-random-repetitions-xnmxj4w1d0s.png

Up to now, the pitches were being selected with equal weight (i.e. an uniform
distribution). Changing the :attr:`~auxjad.PitchRandomiser.weights` property to
a :obj:`list` of :obj:`int`'s or :obj:`float`'s allow us to give more weight to
certain pitches. It's important that this :obj:`list` has the same length as
the number of pitches in :attr:`~auxjad.PitchRandomiser.pitches`.

    >>> randomiser.weights = [6, 3, 2, 1, 1]

At this point, let's also change the input container for the randomiser:

    >>> container = abjad.Container(
    ...     r"\time 3/4 c'4--( ~ "
    ...     r"\times 4/5 {c'16 c'16-. c'16-. c'16-. c'16-.)} "
    ...     r"r8 c'8->"
    ... )
    >>> abjad.show(container)

    ..  docs::

        {
            \time 3/4
            c'4
            - \tenuto
            (
            ~
            \times 4/5
            {
                c'16
                c'16
                - \staccato
                c'16
                - \staccato
                c'16
                - \staccato
                c'16
                - \staccato
                )
            }
            r8
            c'8
            - \accent
        }

    ..  figure:: ../_images/example-4-random-repetitions-KVefBW5cfu.png

Now, with the new contents of the randomiser, let's output two more measures as
the third and final group of measures.

    >>> randomiser.contents = container
    >>> notes = randomiser.output_n(2)
    >>> group_3 = abjad.Staff(notes)
    >>> abjad.show(group_3)

    ..  docs::

        \new Staff
        {
            \time 3/4
            b4
            - \tenuto
            (
            ~
            \times 4/5
            {
                b16
                b16
                - \staccato
                a''16
                - \staccato
                b16
                - \staccato
                a''16
                - \staccato
                )
            }
            r8
            b''8
            - \accent
            bf'4
            - \tenuto
            (
            ~
            \times 4/5
            {
                bf'16
                a16
                - \staccato
                b16
                - \staccato
                a16
                - \staccato
                b16
                - \staccato
                )
            }
            r8
            b8
            - \accent
        }

    ..  figure:: ../_images/example-4-random-repetitions-dF9FpK16kE.png

We can now use :class:`auxjad.Repeater` to create a staff made out of multiple
repetitions of these three groups. When the repeater type is set to to
``'volta'`` using the attribute :attr:`~auxjad.LeafLooper.repeat_type`, it will
output measures with repetition bar lines and with a written indication for the
number of repeats. Let's start with the first group and repeat it 3x.

    >>> staff = abjad.Staff()
    >>> repeater = auxjad.Repeater(group_1,
    ...                            repeat_type='volta',
    ...                            )
    >>> notes = repeater(3)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \repeat volta 3
            {
                d'4
                - \tenuto
                c'8.
                - \tenuto
                e'16
                (
                e'8
                - \staccato
                )
                cs'8
                - \staccato
                ef'8
                - \staccato
                r8
                cs'4
                - \tenuto
                ef'8.
                - \tenuto
                e'16
                (
                ef'8
                - \staccato
                )
                e'8
                - \staccato
                d'8
                - \staccato
                r8
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "3×"}
            }
        }

    ..  figure:: ../_images/example-4-random-repetitions-7vipmn3n2ts.png

Let's now do the same with the second group, repeating it 5x and appending it
to our staff.

    >>> repeater.contents = group_2
    >>> notes = repeater(5)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \repeat volta 3
            {
                d'4
                - \tenuto
                c'8.
                - \tenuto
                e'16
                (
                e'8
                - \staccato
                )
                cs'8
                - \staccato
                ef'8
                - \staccato
                r8
                cs'4
                - \tenuto
                ef'8.
                - \tenuto
                e'16
                (
                ef'8
                - \staccato
                )
                e'8
                - \staccato
                d'8
                - \staccato
                r8
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "3×"}
            }
            \repeat volta 5
            {
                a4
                - \tenuto
                a8.
                - \tenuto
                a16
                (
                b''8
                - \staccato
                )
                b''8
                - \staccato
                a''8
                - \staccato
                r8
                b''4
                - \tenuto
                b8.
                - \tenuto
                a16
                (
                a8
                - \staccato
                )
                bf'8
                - \staccato
                a8
                - \staccato
                r8
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "5×"}
            }
        }

    ..  figure:: ../_images/example-4-random-repetitions-CPWBSKlHBd.png

Finally, let's do the same with the third group and repeat it 4x. This will be
our final score.

    >>> repeater.contents = group_3
    >>> notes = repeater(4)
    >>> staff.append(notes)
    >>> abjad.show(staff)

    ..  docs::

        \new Staff
        {
            \repeat volta 3
            {
                d'4
                - \tenuto
                c'8.
                - \tenuto
                e'16
                (
                e'8
                - \staccato
                )
                cs'8
                - \staccato
                ef'8
                - \staccato
                r8
                cs'4
                - \tenuto
                ef'8.
                - \tenuto
                e'16
                (
                ef'8
                - \staccato
                )
                e'8
                - \staccato
                d'8
                - \staccato
                r8
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "3×"}
            }
            \repeat volta 5
            {
                a4
                - \tenuto
                a8.
                - \tenuto
                a16
                (
                b''8
                - \staccato
                )
                b''8
                - \staccato
                a''8
                - \staccato
                r8
                b''4
                - \tenuto
                b8.
                - \tenuto
                a16
                (
                a8
                - \staccato
                )
                bf'8
                - \staccato
                a8
                - \staccato
                r8
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "5×"}
            }
            \repeat volta 4
            {
                \time 3/4
                b4
                - \tenuto
                (
                ~
                \times 4/5
                {
                    b16
                    b16
                    - \staccato
                    a''16
                    - \staccato
                    b16
                    - \staccato
                    a''16
                    - \staccato
                    )
                }
                r8
                b''8
                - \accent
                bf'4
                - \tenuto
                (
                ~
                \times 4/5
                {
                    bf'16
                    a16
                    - \staccato
                    b16
                    - \staccato
                    a16
                    - \staccato
                    b16
                    - \staccato
                    )
                }
                r8
                b8
                - \accent
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "4×"}
            }
        }

    ..  figure:: ../_images/example-4-random-repetitions-3A9Bt4Xifq.png

.. include:: ../api/abjad-targets.rst
.. include:: ../api/auxjad-targets.rst
