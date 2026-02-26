import abjad

import auxjad


def test_Context_context_commands():
    assert auxjad.Context.context_commands is abjad.Context.context_commands


def test_Context_context_commands_Staff():
    staff = abjad.Staff([])
    staff.context_commands.append(r"\RemoveEmptyStaves")
    assert abjad.lilypond(staff) == abjad.String.normalize(r"""
        \new Staff
        \with
        {
            \RemoveEmptyStaves
        }
        {
        }
        """)


def test_Context_context_commands_Voice():
    voice = abjad.Voice([])
    voice.context_commands.append(r"\voiceOne")
    assert abjad.lilypond(voice) == abjad.String.normalize(r"""
        \new Voice
        \with
        {
            \voiceOne
        }
        {
        }
        """)


def test_Context_context_commands_StaffGroup():
    staff_group = abjad.StaffGroup([])
    staff_group.context_commands.append(r"\RemoveEmptyStaves")
    assert abjad.lilypond(staff_group) == abjad.String.normalize(r"""
        \new StaffGroup
        \with
        {
            \RemoveEmptyStaves
        }
        <<
        >>
        """)


def test_Context_context_commands_Score():
    score = abjad.Score([])
    score.context_commands.append(r"\RemoveEmptyStaves")
    assert abjad.lilypond(score) == abjad.String.normalize(r"""
        \new Score
        \with
        {
            \RemoveEmptyStaves
        }
        <<
        >>
        """)
