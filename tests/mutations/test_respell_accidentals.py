import abjad

import auxjad


def test_respell_accidentals_01():
    staff = abjad.Staff(r"c'4 r4 <ef' e'>4 g'4 <c' cs'>4 r2.")
    auxjad.mutate(staff[:]).respell_accidentals()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r4
            <ds' e'>4
            g'4
            <c' df'>4
            r2.
        }
        """)


def test_respell_accidentals_02():
    staff = abjad.Staff()
    for pitch in range(12):
        staff.append(abjad.Chord([pitch, pitch + 1], (1, 16)))
    auxjad.mutate(staff[:]).respell_accidentals()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' df'>16
            <cs' d'>16
            <d' ef'>16
            <ds' e'>16
            <e' f'>16
            <f' gf'>16
            <fs' g'>16
            <g' af'>16
            <gs' a'>16
            <a' bf'>16
            <as' b'>16
            <b' c''>16
        }
        """)


def test_respell_accidentals_03():
    staff = abjad.Staff(r"<a c' cs' f'>1")
    auxjad.mutate(staff[:]).respell_accidentals()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <a c' df' f'>1
        }
        """)


def test_respell_accidentals_04():
    staff = abjad.Staff(r"<e' cs' g' ef'>1")
    auxjad.mutate(staff[:]).respell_accidentals()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <cs' ds' e' g'>1
        }
        """)


def test_respell_accidentals_05():
    staff = abjad.Staff(r"<c' cs''>1")
    auxjad.mutate(staff[:]).respell_accidentals()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' cs''>1
        }
        """)
    auxjad.mutate(staff[:]).respell_accidentals(include_multiples=True)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' df''>1
        }
        """)


def test_respell_accidentals_06():
    staff = abjad.Staff(r"<c' cs' cs''>1")
    auxjad.mutate(staff[:]).respell_accidentals()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' df' cs''>1
        }
        """)
    staff = abjad.Staff(r"<c' cs' cs''>1")
    auxjad.mutate(staff[:]).respell_accidentals(respell_by_pitch_class=True)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' df' df''>1
        }
        """)


def test_respell_accidentals_07():
    staff = abjad.Staff(r"c'4 r4 <ef' e'>4 g'4 <c' cs'>4 r2.")
    abjad.mutate(staff[:]).respell_accidentals()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r4
            <ds' e'>4
            g'4
            <c' df'>4
            r2.
        }
        """)
