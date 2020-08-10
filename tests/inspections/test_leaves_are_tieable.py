import abjad

import auxjad


def test_leaves_are_tieable_01():
    leaf1 = abjad.Note(r"c'4")
    leaf2 = abjad.Note(r"c'4")
    assert auxjad.leaves_are_tieable(leaf1, leaf2)


def test_leaves_are_tieable_02():
    leaf1 = abjad.Note(r"c'2.")
    leaf2 = abjad.Note(r"c'16")
    leaf3 = abjad.Note(r"f'''16")
    assert auxjad.leaves_are_tieable(leaf1, leaf2)
    assert not auxjad.leaves_are_tieable(leaf1, leaf3)
    assert not auxjad.leaves_are_tieable(leaf2, leaf3)


def test_leaves_are_tieable_03():
    chord1 = abjad.Chord(r"<c' e' g'>4")
    chord2 = abjad.Chord(r"<c' e' g'>16")
    chord3 = abjad.Chord(r"<f''' fs'''>16")
    assert auxjad.leaves_are_tieable(chord1, chord2)
    assert not auxjad.leaves_are_tieable(chord1, chord3)
    assert not auxjad.leaves_are_tieable(chord2, chord3)


def test_leaves_are_tieable_04():
    chord1 = abjad.Chord(r"<c' e' g'>4")
    chord2 = abjad.Chord(r"<c' e' g' bf'>4")
    assert not auxjad.leaves_are_tieable(chord1, chord2)


def test_leaves_are_tieable_05():
    container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
    assert auxjad.leaves_are_tieable(container[1], container[2])


def test_leaves_are_tieable_06():
    container = abjad.Container(r"r4 g'4 r2")
    assert not auxjad.leaves_are_tieable(container[0], container[2])


def test_leaves_are_tieable_07():
    staff1 = abjad.Staff(r"c'2 d'2 ~ d'8")
    staff2 = abjad.Staff(r"d'16 e'4")
    staff3 = abjad.Staff(r"f'''16 d'2")
    assert auxjad.leaves_are_tieable(staff1[:], staff2[:])
    assert not auxjad.leaves_are_tieable(staff1[:], staff3[:])
    assert not auxjad.leaves_are_tieable(staff2[:], staff3[:])


def test_leaves_are_tieable_08():
    leaf1 = abjad.Note(r"c'2.")
    leaf2 = abjad.Note(r"c'16")
    leaf3 = abjad.Note(r"f'''16")
    assert abjad.inspect(leaf1).leaves_are_tieable(leaf2)
    assert not abjad.inspect(leaf1).leaves_are_tieable(leaf3)
    assert not abjad.inspect(leaf2).leaves_are_tieable(leaf3)
