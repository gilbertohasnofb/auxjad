import abjad

import auxjad


def test_piano_pedal_01():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_02():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       until_the_end=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_03():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       omit_raise_pedal_glyph=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_04():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       until_the_end=True,
                       omit_raise_pedal_glyph=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_05():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:])
    abjad.setting(staff).pedal_sustain_style = "#'mixed"
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            pedalSustainStyle = #'mixed
        }
        {
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_06():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       until_the_end=True,
                       )
    abjad.setting(staff).pedal_sustain_style = "#'mixed"
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            pedalSustainStyle = #'mixed
        }
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_07():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       until_the_end=True,
                       omit_raise_pedal_glyph=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_08():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       half_pedal=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_09():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       half_pedal=True,
                       until_the_end=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_10():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       half_pedal=True,
                       omit_raise_pedal_glyph=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_11():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       half_pedal=True,
                       until_the_end=True,
                       omit_raise_pedal_glyph=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_12():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       half_pedal=True,
                       )
    abjad.setting(staff).pedal_sustain_style = "#'mixed"
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            pedalSustainStyle = #'mixed
        }
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_13():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       half_pedal=True,
                       until_the_end=True,
                       )
    abjad.setting(staff).pedal_sustain_style = "#'mixed"
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            pedalSustainStyle = #'mixed
        }
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_14():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    auxjad.piano_pedal(staff[:],
                       half_pedal=True,
                       until_the_end=True,
                       omit_raise_pedal_glyph=True,
                       )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            c'4
            \sustainOn
            d'4
            e'4
            \once \override Staff.SustainPedal.stencil = ##f
            f'4
            \sustainOff
        }
        """
    )


def test_piano_pedal_15():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    abjad.piano_pedal(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \sustainOn
            d'4
            e'4
            f'4
            \sustainOff
        }
        """
    )
