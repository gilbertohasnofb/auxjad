import abjad

import auxjad


def test_leaves_are_tieable_01():
    leaf1 = abjad.Note(r"c'4")
    leaf2 = abjad.Note(r"c'4")
    assert auxjad.get.leaves_are_tieable([leaf1, leaf2])


def test_leaves_are_tieable_02():
    leaf1 = abjad.Note(r"c'2.")
    leaf2 = abjad.Note(r"c'16")
    leaf3 = abjad.Note(r"f'''16")
    leaf4 = abjad.Note(r"r2.")
    assert auxjad.get.leaves_are_tieable([leaf1, leaf2])
    assert not auxjad.get.leaves_are_tieable([leaf1, leaf3])
    assert not auxjad.get.leaves_are_tieable([leaf2, leaf3])
    assert not auxjad.get.leaves_are_tieable([leaf3, leaf4])


def test_leaves_are_tieable_03():
    chord1 = abjad.Chord(r"<c' e' g'>4")
    chord2 = abjad.Chord(r"<c' e' g'>16")
    chord3 = abjad.Chord(r"<f''' fs'''>16")
    assert auxjad.get.leaves_are_tieable([chord1, chord2])
    assert not auxjad.get.leaves_are_tieable([chord1, chord3])
    assert not auxjad.get.leaves_are_tieable([chord2, chord3])


def test_leaves_are_tieable_04():
    chord1 = abjad.Chord(r"<c' e' g'>4")
    chord2 = abjad.Chord(r"<c' e' g' bf'>4")
    note = abjad.Note(r"c'4")
    assert auxjad.get.leaves_are_tieable([chord1, chord2])
    assert auxjad.get.leaves_are_tieable([chord2, note])


def test_leaves_are_tieable_05():
    container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
    assert auxjad.get.leaves_are_tieable([container[1], container[2]])


def test_leaves_are_tieable_06():
    leaf = abjad.Note(r"c'4")
    rest = abjad.Rest(r"r4")
    assert not auxjad.get.leaves_are_tieable([leaf, rest])


def test_leaves_are_tieable_07():
    staff = abjad.Staff(r"c'4 d'4 e'2 e'1")
    assert not auxjad.get.leaves_are_tieable(staff[:2])
    assert not auxjad.get.leaves_are_tieable(staff[1:3])
    assert auxjad.get.leaves_are_tieable(staff[2:4])


def test_leaves_are_tieable_08():
    staff = abjad.Staff(r"c'2 c'4. c'8")
    assert auxjad.get.leaves_are_tieable(staff[:])
    staff = abjad.Staff(r"c'2 c'4. d'8")
    assert not auxjad.get.leaves_are_tieable(staff[:])


def test_leaves_are_tieable_09():
    leaf1 = abjad.Note(r"c'4")
    leaf2 = abjad.Note(r"c'4")
    leaf3 = abjad.Note(r"c'2.")
    assert auxjad.get.leaves_are_tieable([leaf1, leaf2, leaf3])


def test_leaves_are_tieable_10():
    leaf = abjad.Note(r"c'2.")
    staff = abjad.Staff(r"c'4 ~ c'16")
    logical_tie = abjad.select(staff).logical_tie(0)
    assert auxjad.get.leaves_are_tieable([leaf, logical_tie])


def test_leaves_are_tieable_11():
    leaf1 = abjad.Note(r"c'2.")
    leaf2 = abjad.Note(r"c'16")
    leaf3 = abjad.Note(r"f'''16")
    assert abjad.get.leaves_are_tieable([leaf1, leaf2])
    assert not abjad.get.leaves_are_tieable([leaf1, leaf3])
    assert not abjad.get.leaves_are_tieable([leaf2, leaf3])


def test_leaves_are_tieable_12():
    leaf1 = abjad.Note(r"c'4")
    leaf2 = abjad.Chord(r"<c' e'>4")
    leaf3 = abjad.Note(r"c'2")
    assert auxjad.get.leaves_are_tieable([leaf1, leaf2])
    assert not auxjad.get.leaves_are_tieable([leaf1, leaf2],
                                             only_identical_pitches=True,
                                             )
    assert auxjad.get.leaves_are_tieable([leaf2, leaf3])
    assert not auxjad.get.leaves_are_tieable([leaf2, leaf3],
                                             only_identical_pitches=True,
                                             )


def test_leaves_are_tieable_13():
    chord1 = abjad.Chord(r"<c' e' g'>4")
    chord2 = abjad.Chord(r"<c' e' g' bf'>4")
    chord3 = abjad.Chord(r"<c' e' fs'>4")
    assert auxjad.get.leaves_are_tieable([chord1, chord2])
    assert not auxjad.get.leaves_are_tieable([chord1, chord2],
                                             only_identical_pitches=True,
                                             )
    assert auxjad.get.leaves_are_tieable([chord2, chord3])
    assert not auxjad.get.leaves_are_tieable([chord2, chord3],
                                             only_identical_pitches=True,
                                             )


def test_leaves_are_tieable_14():
    staff = abjad.Staff(r"c'2 c'4. <c' e'>8")
    assert auxjad.get.leaves_are_tieable(staff[:])
    assert not auxjad.get.leaves_are_tieable(staff[:],
                                             only_identical_pitches=True,
                                             )
