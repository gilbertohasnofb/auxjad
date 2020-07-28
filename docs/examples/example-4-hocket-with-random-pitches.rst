Hocket with random pitches
==========================

In this example, we will use some of |auxjad|_'s classes to generate a hocket
with random pitches.

First, we start by importing both :mod:`abjad` and |auxjad|_.

    >>> import abjad
    >>> import auxjad

First, let's create a container with an arbitrary rhythm. The pitches do not
matter at this point since we will randomise them shortly.

    >>> container = abjad.Container(r"c'4 ~ c'16 r8 c'16 c'4 c'16 r8.")
    >>> abjad.f(container)
    {
        c'4
        ~
        c'16
        r8
        c'16
        c'4
        c'16
        r8.
    }

.. figure:: ../_images/image-example-4-hocket-with-random-pitches-1.png

Next, let's initialise :class:`auxjad.PitchRandomiser` with this container as
well as a :obj:`list` representing pitches. This will be the source for the
random pitches selected by this randomiser.

    >>> randomiser = auxjad.PitchRandomiser(container,
    ...                                     pitches=[0, 1, 2, 3, 4, 5, 6],
    ...                                     )

We can now output three measures with random pitches using the method
:meth:`auxjad.PitchRandomiser.output_n`.

    >>> staff = abjad.Staff()
    >>> notes = randomiser.output_n(3)
    >>> staff.append(notes)
    >>> abjad.f(container)
    \new Staff
    {
        f'4
        ~
        f'16
        r8
        fs'16
        d'4
        cs'16
        r8.
        fs'4
        ~
        fs'16
        r8
        cs'16
        ef'4
        e'16
        r8.
        c'4
        ~
        c'16
        r8
        ef'16
        c'4
        cs'16
        r8.
    }

.. figure:: ../_images/image-example-4-hocket-with-random-pitches-2.png

Let's now change the pitch :obj:`list` using the property
:attr:`~auxjad.PitchRandomiser.pitches` of the randomiser.

    >>> randomiser.pitches = [13, 14, 16, 17, 21]

Generating three more measures results in:

    >>> notes = randomiser.output_n(3)
    >>> staff.append(notes)
    >>> abjad.f(container)
    \new Staff
    {
        f'4
        ~
        f'16
        r8
        fs'16
        d'4
        cs'16
        r8.
        fs'4
        ~
        fs'16
        r8
        cs'16
        ef'4
        e'16
        r8.
        c'4
        ~
        c'16
        r8
        ef'16
        c'4
        cs'16
        r8.
        f''4
        ~
        f''16
        r8
        f''16
        cs''4
        f''16
        r8.
        f''4
        ~
        f''16
        r8
        a''16
        e''4
        f''16
        r8.
        a''4
        ~
        a''16
        r8
        cs''16
        e''4
        f''16
        r8.
    }

.. figure:: ../_images/image-example-4-hocket-with-random-pitches-3.png

Up to now, the pitches were being selected with equal weight (i.e. an uniform
distribution). Changing the :attr:`~auxjad.PitchRandomiser.weights` property to
a :obj:`list` of :obj:`int`'s or :obj:`float`'s allow us to give more weight to
certain pitches. It's important that this :obj:`list` has the same length as
the number of pitches in :attr:`~auxjad.PitchRandomiser.pitches`.

    >>> randomiser.weights = [6, 3, 2, 1, 1]

    Generating three more measures results in:

        >>> notes = randomiser.output_n(3)
        >>> staff.append(notes)
        >>> abjad.f(container)
        \new Staff
        {
            f'4
            ~
            f'16
            r8
            fs'16
            d'4
            cs'16
            r8.
            fs'4
            ~
            fs'16
            r8
            cs'16
            ef'4
            e'16
            r8.
            c'4
            ~
            c'16
            r8
            ef'16
            c'4
            cs'16
            r8.
            f''4
            ~
            f''16
            r8
            f''16
            cs''4
            f''16
            r8.
            f''4
            ~
            f''16
            r8
            a''16
            e''4
            f''16
            r8.
            a''4
            ~
            a''16
            r8
            cs''16
            e''4
            f''16
            r8.
            cs''4
            ~
            cs''16
            r8
            d''16
            d''4
            d''16
            r8.
            d''4
            ~
            d''16
            r8
            cs''16
            d''4
            a''16
            r8.
            d''4
            ~
            d''16
            r8
            cs''16
            d''4
            cs''16
            r8.
        }

.. figure:: ../_images/image-example-4-hocket-with-random-pitches-4.png

Let's now feed this staff of music into :class:`auxjad.Hocketer`. This class
will distribute each note to a different voice, each given their own staff. See
its documentation for more information. For a basic usage with three voices, we
simply initialise :class:`auxjad.Hocketer` with the staff we previously created
as well as the desired number of voices.

    >>> hocketer = auxjad.Hocketer(staff,
    ...                            n_voices=3,
    ...                            )

To create the final score, we can simply assign its return value to an
|abjad.Score|.

    >>> music = hocketer()
    >>> score = abjad.Score(music)
    >>> abjad.f(score)
    \new Score
    <<
        \new Staff
        {
            f'4
            ~
            f'16
            r4..
            cs'16
            r8.
            R1
            R1
            f''4
            ~
            f''16
            r16
            r16
            f''16
            r2
            R1
            a''4
            ~
            a''16
            r8.
            e''4
            r4
            r2.
            d''16
            r8.
            r4..
            cs''16
            r2
            r4..
            cs''16
            r4
            cs''16
            r8.
        }
        \new Staff
        {
            r2
            d'4
            r4
            fs'4
            ~
            fs'16
            r8.
            r2
            c'4
            ~
            c'16
            r16
            r16
            ef'16
            r4
            cs'16
            r8.
            r2.
            f''16
            r8.
            f''4
            ~
            f''16
            r16
            r16
            a''16
            e''4
            f''16
            r8.
            r4..
            cs''16
            r2
            r4..
            d''16
            r2
            d''4
            ~
            d''16
            r4..
            a''16
            r8.
            R1
        }
        \new Staff
        {
            r4..
            fs'16
            r2
            r4..
            cs'16
            ef'4
            e'16
            r8.
            r2
            c'4
            r4
            r2
            cs''4
            r4
            R1
            r2.
            f''16
            r8.
            cs''4
            ~
            cs''16
            r8.
            d''4
            r4
            r2
            d''4
            r4
            d''4
            ~
            d''16
            r8.
            d''4
            r4
        }
    >>

.. figure:: ../_images/image-example-4-hocket-with-random-pitches-5.png

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: ../api/index.html

.. include:: ../api/abjad-targets.rst
