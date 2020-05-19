import abjad
import auxjad


def test_leaves_are_tieable_01():
    note1 = abjad.Note(r"c'4")
    note2 = abjad.Note(r"c'4")
    assert auxjad.leaves_are_tieable(note1, note2)


def test_leaves_are_tieable_02():
    note1 = abjad.Note(r"c'2.")
    note2 = abjad.Note(r"c'16")
    note3 = abjad.Note(r"f'''16")
    assert auxjad.leaves_are_tieable(note1, note2)
    assert not auxjad.leaves_are_tieable(note1, note3)
    assert not auxjad.leaves_are_tieable(note2, note3)


def test_leaves_are_tieable_03():
    chord1 = abjad.Chord(r"<c' e' g'>4")
    chord2 = abjad.Chord(r"<c' e' g'>16")
    chord3 = abjad.Chord(r"<f''' fs'''>16")
    assert auxjad.leaves_are_tieable(chord1, chord2)
    assert not auxjad.leaves_are_tieable(chord1, chord3)
    assert not auxjad.leaves_are_tieable(chord2, chord3)


def test_leaves_are_tieable_04():
    container = abjad.Container(r"r4 <c' e'>4 <c' e'>2")
    assert auxjad.leaves_are_tieable(container[1], container[2])


def test_leaves_are_tieable_05():
    container = abjad.Container(r"r4 g'4 r2")
    assert not auxjad.leaves_are_tieable(container[0], container[2])
