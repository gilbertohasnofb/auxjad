import random

import abjad
import pytest

import auxjad


def test_PitchRandomiser_01():
    random.seed(16284)
    container = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
    pitches = r"fs' gs' a' b' cs''"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    assert format(randomiser) == "PitchSegment(\"fs' gs' a' b' cs''\")"
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            a'4
            b'4
            cs''4
            fs'4
        }
        """)
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            b'4
            b'4
            b'4
            fs'4
        }
        """)
    notes = randomiser.current_window
    with pytest.raises(AttributeError):
        randomiser.current_window = abjad.Container(r"c''2 e''2")
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            b'4
            b'4
            b'4
            fs'4
        }
        """)


def test_PitchRandomiser_02():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches=r"a b cs' ds' e'",
                                        weights=[1.0, 2.0, 1.0, 1.5, 1.3],
                                        omit_time_signatures=True,
                                        process_on_first_call=True,
                                        use_tenney_selector=True,
                                        )
    assert randomiser.pitches == abjad.PitchSegment(r"a b cs' ds' e'")
    assert randomiser.weights == [1.0, 2.0, 1.0, 1.5, 1.3]
    assert randomiser.omit_time_signatures
    assert randomiser.process_on_first_call
    assert randomiser.use_tenney_selector
    randomiser.pitches = abjad.PitchSegment(r"c' d' e' f'")
    randomiser.weights = [1, 2, 5, 8]
    randomiser.omit_time_signatures = False
    randomiser.process_on_first_call = False
    randomiser.use_tenney_selector = False
    assert randomiser.pitches == abjad.PitchSegment(r"c' d' e' f'")
    assert randomiser.weights == [1, 2, 5, 8]
    assert not randomiser.omit_time_signatures
    assert not randomiser.process_on_first_call
    assert not randomiser.use_tenney_selector


def test_PitchRandomiser_03():
    random.seed(19387)
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    pitches = [6, 7, 8, 9, 10, 11]
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            bf'8.
            af'4
            r8
            r8.
            bf'16
            a'8.
        }
        """)


def test_PitchRandomiser_04():
    random.seed(87612)
    container = abjad.Container(r"<c' e' g'>8. d'4 r8 r8. e'16 <f' a'>8.")
    pitches = [6, 7, 8, 9, 10, 11]
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <fs' g' bf'>8.
            b'4
            r8
            r8.
            bf'16
            <fs' bf'>8.
        }
        """)


def test_PitchRandomiser_05():
    random.seed(31987)
    container = abjad.Container(r"<c' e' g' a'>2 <cs' ds' e' f' g' a' b'>2")
    pitches = [6, 7, 8]
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <fs' g' af'>2
            <fs' g' af'>2
        }
        """)


def test_PitchRandomiser_06():
    random.seed(87132)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        use_tenney_selector=True,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            fs'8
            a'8
            fs'8
            gs'8
            a'8
            b'8
            gs'8
            fs'8
        }
        """)


def test_PitchRandomiser_07():
    random.seed(67612)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        weights=[5.0, 2.0, 1.5, 1.0],
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            b'8
            fs'8
            gs'8
            gs'8
            gs'8
            fs'8
            fs'8
            a'8
        }
        """)


def test_PitchRandomiser_08():
    random.seed(81223)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        weights=[5.0, 2.0, 1.5, 1.0],
                                        use_tenney_selector=True,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            fs'8
            gs'8
            a'8
            fs'8
            gs'8
            a'8
            gs'8
            b'8
        }
        """)


def test_PitchRandomiser_09():
    random.seed(91445)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        weights=[100.0, 1.0, 1.0, 1.0],
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            fs'8
            fs'8
            fs'8
            fs'8
            fs'8
            fs'8
            fs'8
            fs'8
        }
        """)
    randomiser.weights = None
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            fs'8
            fs'8
            b'8
            gs'8
            gs'8
            a'8
            fs'8
            b'8
        }
        """)


def test_PitchRandomiser_10():
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        weights=[100.0, 1.0, 1.0, 1.0],
                                        )
    randomiser.pitches = r"c'' d'' e'' f''"
    assert randomiser.pitches == abjad.PitchSegment(r"c'' d'' e'' f''")
    assert randomiser.weights == [100.0, 1.0, 1.0, 1.0]


def test_PitchRandomiser_11():
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        weights=[100.0, 1.0, 1.0, 1.0],
                                        )
    randomiser.pitches = r"c'' d'' e'' f'' g'' a'' b''"
    assert randomiser.pitches == abjad.PitchSegment(
        r"c'' d'' e'' f'' g'' a'' b''"
    )
    assert randomiser.weights is None


def test_PitchRandomiser_12():
    random.seed(95877)
    container = abjad.Container(r"c'4 ~ c'16 r8. d'4 e'8. r16")
    pitches = [6, 7, 8, 9, 10]
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    notes = randomiser.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            a'4
            ~
            a'16
            r8.
            g'4
            fs'8.
            r16
            g'4
            ~
            g'16
            r8.
            g'4
            fs'8.
            r16
            bf'4
            ~
            bf'16
            r8.
            a'4
            af'8.
            r16
        }
        """)


def test_PitchRandomiser_13():
    random.seed(88112)
    container = abjad.Container(
        r"c'4\p\< ~ c'8. d'16-.\f e'4--\pp f'8.( g'16)"
    )
    pitches = [6, 7, 8, 9, 10, 11, 12]
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            a'4
            \p
            \<
            ~
            a'8.
            c''16
            \f
            - \staccato
            af'4
            \pp
            - \tenuto
            a'8.
            (
            bf'16
            )
        }
        """)


def test_PitchRandomiser_14():
    random.seed(97112)
    container = abjad.Container(r"\time 3/4 c'4 d'2 \time 2/4 e'8 f'8 g'8 a'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            a'4
            fs'2
            \time 2/4
            gs'8
            gs'8
            a'8
            gs'8
        }
        """)


def test_PitchRandomiser_15():
    random.seed(97112)
    container = abjad.Container(r"\time 3/4 c'4 d'2 \time 2/4 e'8 f'8 g'8 a'8")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        omit_time_signatures=True,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            a'4
            fs'2
            gs'8
            gs'8
            a'8
            gs'8
        }
        """)


def test_PitchRandomiser_16():
    random.seed(45017)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        process_on_first_call=False,
                                        )
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = randomiser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            b'4
            fs'4
            gs'4
            fs'4
        }
        """)


def test_PitchRandomiser_17():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    pitches = r"fs' gs' a' b'"
    weights = None
    assert auxjad.PitchRandomiser(container, pitches, weights=weights)
    weights = [1, 1, 5, 2]
    assert auxjad.PitchRandomiser(container, pitches, weights=weights)
    weights = [1, 1, 5, 2, 3, 4, 8]
    with pytest.raises(ValueError):
        assert auxjad.PitchRandomiser(container, pitches, weights=weights)


def test_PitchRandomiser_18():
    random.seed(91773)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
    pitches = r"fs' gs' a' b' cs''"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    staff = abjad.Staff()
    for window in randomiser:
        staff.append(window)
        if abjad.inspect(staff).duration() == abjad.Duration((9, 4)):
            break
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            a'4
            b'4
            gs'4
            \time 3/4
            fs'4
            a'4
            b'4
            \time 3/4
            a'4
            gs'4
            cs''4
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            a'4
            b'4
            gs'4
            fs'4
            a'4
            b'4
            a'4
            gs'4
            cs''4
        }
        """)


def test_PitchRandomiser_19():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    pitches = r"fs' gs' a' b'"
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    assert len(randomiser) == 4
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    pitches = [6, 7, 8, 9, 10, 11, 12]
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches,
                                        )
    assert len(randomiser) == 7
