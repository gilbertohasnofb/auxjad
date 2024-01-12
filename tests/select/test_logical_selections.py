import abjad

import auxjad


def test_logical_selections_01():
    container = abjad.Container(r"c'4 ~ c'16 r8. r4.. d'16 ~ d'4")
    logical_selections = auxjad.select.logical_selections(container)
    expected_results = [
        r"c'4 ~ c'16",
        r"r8. r4..",
        r"d'16 ~ d'4",
    ]
    for logical_selection, expected_result in zip(logical_selections,
                                                  expected_results,
                                                  ):
        selections = [logical_selection.leaves(),
                      abjad.Container(expected_result)[:],
                      ]
        assert auxjad.get.selections_are_identical(selections)


def test_logical_selections_02():
    container = abjad.Container(
        r"c'4 ~ c'16 r8. r2 r4.. d'16 r8 <e' f'>8"
    )
    logical_selections = auxjad.select.logical_selections(container)
    expected_results = [
        r"c'4 ~ c'16",
        r"r8. r2 r4..",
        r"d'16",
        r"r8",
        r"<e' f'>8",
    ]
    for logical_selection, expected_result in zip(logical_selections,
                                                  expected_results,
                                                  ):
        selections = [logical_selection.leaves(),
                      abjad.Container(expected_result)[:],
                      ]
        assert auxjad.get.selections_are_identical(selections)


def test_logical_selections_03():
    container = abjad.Container(r"c'2. ~ c'16 r8. R1 r4.. d'16 ~ d'2.")
    logical_selections = auxjad.select.logical_selections(container)
    expected_results = [
        r"c'2. ~ c'16",
        r"r8. R1 r4..",
        r"d'16 ~ d'2.",
    ]
    for logical_selection, expected_result in zip(logical_selections,
                                                  expected_results,
                                                  ):
        selections = [logical_selection.leaves(),
                      abjad.Container(expected_result)[:],
                      ]
        assert auxjad.get.selections_are_identical(selections)


def test_logical_selections_04():
    container = abjad.Container(r"c'2. ~ c'16 r8. R1 r4.. d'16 ~ d'2.")
    logical_selections = auxjad.select.logical_selections(
        container,
        include_multimeasure_rests=False,
    )
    expected_results = [
        r"c'2. ~ c'16",
        r"r8.",
        r"R1",
        r"r4..",
        r"d'16 ~ d'2.",
    ]
    for logical_selection, expected_result in zip(logical_selections,
                                                  expected_results,
                                                  ):
        selections = [logical_selection.leaves(),
                      abjad.Container(expected_result)[:],
                      ]
        assert auxjad.get.selections_are_identical(selections)
