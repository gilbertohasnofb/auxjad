import abjad

import auxjad


def test_Context_with_settings():
    assert auxjad.Context.with_settings is abjad.Context.with_settings


def test_Context_with_settings_Staff():
    staff = abjad.Staff([])
    staff.with_settings.append(r"\RemoveEmptyStaves")
    assert abjad.lilypond(staff) == abjad.String.normalize(r"""
        \new Staff
        \with
        {
            \RemoveEmptyStaves
        }
        {
        }
        """)


def test_Context_with_settings_Voice():
    voice = abjad.Voice([])
    voice.with_settings.append(r"\voiceOne")
    assert abjad.lilypond(voice) == abjad.String.normalize(r"""
        \new Voice
        \with
        {
            \voiceOne
        }
        {
        }
        """)


def test_Context_with_settings_StaffGroup():
    staff_group = abjad.StaffGroup([])
    staff_group.with_settings.append(r"\acceptsStaffGroup")
    assert abjad.lilypond(staff_group) == abjad.String.normalize(r"""
        \new StaffGroup
        \with
        {
            \acceptsStaffGroup
        }
        <<
        >>
        """)


def test_Context_with_settings_Score():
    score = abjad.Score([])
    score.with_settings.append(r"\EnableGregorianDivisiones")
    assert abjad.lilypond(score) == abjad.String.normalize(r"""
        \new Score
        \with
        {
            \EnableGregorianDivisiones
        }
        <<
        >>
        """)
