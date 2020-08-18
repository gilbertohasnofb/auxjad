import abjad

import auxjad


def test_example_of_usage_01():
    material = abjad.Staff(r"\time 12/8 c8 c c r c c r c r c c r",
                           lilypond_type="RhythmicStaff",
                           )
    phaser = auxjad.Phaser(material,
                           step_size=abjad.Duration((1, 8)),
                           )
    notes = phaser.output_all()
    phased_staff = abjad.Staff(notes,
                               lilypond_type="RhythmicStaff",
                               )
    repeater = auxjad.Repeater(material)
    notes = repeater(13)
    constant_staff = abjad.Staff(notes,
                                 lilypond_type="RhythmicStaff",
                                 )
    score = abjad.Score([constant_staff, phased_staff])
    measures = abjad.select(constant_staff[:]).group_by_measure()
    for measure in measures[:-1]:
        abjad.attach(abjad.BarLine(':..:'), measure[-1])
    abjad.attach(abjad.BarLine(':|.'), constant_staff[-1])
    assert format(score) == abjad.String.normalize(
        r"""
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
        """)
