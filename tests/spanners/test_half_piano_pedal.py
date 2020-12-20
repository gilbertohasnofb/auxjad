import abjad

import auxjad


def test_half_piano_pedal_01():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.half_piano_pedal(staff[:])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    (markup #:larger "½"
                            #:musicglyph "pedal.Ped")))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """)


def test_half_piano_pedal_02():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.half_piano_pedal(staff[:],
                            until_the_end=True,
                            )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    (markup #:larger "½"
                            #:musicglyph "pedal.Ped"
                            #:raise -0.3 "→")))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """)


def test_half_piano_pedal_03():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.half_piano_pedal(staff[:],
                            omit_raise_pedal_glyph=True,
                            )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    (markup #:larger "½"
                            #:musicglyph "pedal.Ped")))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """)


def test_half_piano_pedal_04():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.half_piano_pedal(staff[:],
                            until_the_end=True,
                            omit_raise_pedal_glyph=True,
                            )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    (markup #:larger "½"
                            #:musicglyph "pedal.Ped"
                            #:raise -0.3 "→")))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """)


def test_half_piano_pedal_05():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.half_piano_pedal(staff[:])
    abjad.setting(staff).pedal_sustain_style = "#'mixed"
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            pedalSustainStyle = #'mixed
        }
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    (markup #:larger "½"
                            #:musicglyph "pedal.Ped")))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """)


def test_half_piano_pedal_06():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.half_piano_pedal(staff[:],
                            until_the_end=True,
                            )
    abjad.setting(staff).pedal_sustain_style = "#'mixed"
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            pedalSustainStyle = #'mixed
        }
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    (markup #:larger "½"
                            #:musicglyph "pedal.Ped"
                            #:raise -0.3 "→")))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """)


def test_half_piano_pedal_07():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    abjad.half_piano_pedal(staff[:],
                           until_the_end=True,
                           omit_raise_pedal_glyph=True,
                           )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    (markup #:larger "½"
                            #:musicglyph "pedal.Ped"
                            #:raise -0.3 "→")))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """)