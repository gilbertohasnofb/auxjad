Steve Reich's *Clapping Music*
==============================

In this example, we will use some of |auxjad|_'s classes and functions to
generate the score of Steve Reich's *Clapping Music*.

First, we start by importing both :mod:`abjad` and |auxjad|_.

    >>> import abjad
    >>> import auxjad

Let's now input the basic material that will be used to generate this
composition. The original score is notated using a rhythmic staff, so we can
initialise |abjad.Staff| with the property
:attr:`lilypond_type <abjad.core.Staff.Staff.lilypond_type>` set to
``"RhythmicStaff"``.

    >>> material = abjad.Staff(r"\time 12/8 c8 c c r c c r c r c c r",
    ...                        lilypond_type="RhythmicStaff",
    ...                        )
    >>> abjad.show(material)

..  docs::

    \new RhythmicStaff
    {
        \time 12/8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
    }

..  figure:: ../_images/example-1-clapping-music-46ql3n3hznt.png

Next, we create an instance of :class:`auxjad.Phaser` which will be used to
create the phasing process of the initial material. We initialise it with
``material`` as well as a :attr:`~auxjad.Phaser.step_size` of the length of a
quaver.

    >>> phaser = auxjad.Phaser(material,
    ...                        step_size=abjad.Duration((1, 8)),
    ...                        )

Since Reich's composition phases the material until it is back at its initial
position, we can use the method :meth:`~auxjad.Phaser.output_all` to generate
all thirtee measures of the bottom staff.

    >>> notes = phaser.output_all()
    >>> phased_staff = abjad.Staff(notes,
    ...                            lilypond_type="RhythmicStaff",
    ...                            )
    >>> abjad.show(phased_staff)

..  docs::

    \new RhythmicStaff
    {
        \time 12/8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
    }

..  figure:: ../_images/example-1-clapping-music-gosdyid8m5c.png

The upper staff of the composition consists of thirteen measures of the
material being repeated. We can thus use the class :func:`auxjad.Repeater()` to
generate these repetitions and take care of removing the time signatures of the
repeated measures.

    >>> repeater = auxjad.Repeater(material)
    >>> notes = repeater(13)
    >>> constant_staff = abjad.Staff(notes,
    ...                              lilypond_type="RhythmicStaff",
    ...                              )
    >>> abjad.show(constant_staff)

..  docs::

    \new RhythmicStaff
    {
        \time 12/8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
        c8
        c8
        c8
        r8
        c8
        c8
        r8
        c8
        r8
        c8
        c8
        r8
    }

..  figure:: ../_images/example-1-clapping-music-vdcucelr7bc.png

With both staves created, we can now add them to a single score.

    >>> score = abjad.Score([constant_staff, phased_staff])
    >>> abjad.show(score)

..  docs::

    \new Score
    <<
        \new RhythmicStaff
        {
            \time 12/8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
        }
        \new RhythmicStaff
        {
            \time 12/8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
        }
    >>

..  figure:: ../_images/example-1-clapping-music-36foxn3jk9.png

We now group the leaves of the upper staff by measures and add a double
repetition bar line to the last leaf of each measure. The very last leaf of the
score should have a single end repetition bar line.

    >>> measures = abjad.select(constant_staff[:]).group_by_measure()
    >>> for measure in measures[:-1]:
    ...     abjad.attach(abjad.BarLine(':..:'), measure[-1])
    >>> abjad.attach(abjad.BarLine(':|.'), constant_staff[-1])
    >>> abjad.show(score)

..  docs::

    \new Score
    <<
        \new RhythmicStaff
        {
            \time 12/8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":..:"
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            \bar ":|."
        }
        \new RhythmicStaff
        {
            \time 12/8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            r8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            c8
            c8
            c8
            r8
            c8
            c8
            r8
            c8
            r8
            c8
            c8
            r8
        }
    >>

..  figure:: ../_images/example-1-clapping-music-k6vxi0vtu6o.png

.. include:: ../api/abjad-targets.rst
.. include:: ../api/auxjad-targets.rst
