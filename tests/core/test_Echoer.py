import random

import abjad
import pytest

import auxjad


def test_Echoer_01():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    assert abjad.lilypond(echoer) == abjad.String.normalize(
        r"""
        {
            %%% \time 4/4 %%%
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
        }
        """
    )
    notes = echoer.current_window
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
        }
        """
    )


def test_Echoer_02():
    container = abjad.Container(r"c'4\p d'4 e' f'")
    echoer = auxjad.Echoer(container)
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            d'4
            e'4
            f'4
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \pp
            d'4
            e'4
            f'4
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \ppp
            d'4
            e'4
            f'4
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
        }
        """
    )
    with pytest.raises(RuntimeError):
        notes = echoer()  # noqa: F841


def test_Echoer_03():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container,
                           min_dynamic='p',
                           max_steps=2,
                           repetition_chance=0.7,
                           disable_rewrite_meter=True,
                           omit_time_signatures=True,
                           use_multimeasure_rests=False,
                           boundary_depth=0,
                           maximum_dot_count=1,
                           rewrite_tuplets=False,
                           process_on_first_call=True,
                           include_empty_measures=False,
                           )
    assert echoer.min_dynamic == 'p'
    assert echoer.max_steps == 2
    assert echoer.repetition_chance == 0.7
    assert echoer.disable_rewrite_meter
    assert echoer.omit_time_signatures
    assert not echoer.use_multimeasure_rests
    assert echoer.boundary_depth == 0
    assert echoer.maximum_dot_count == 1
    assert not echoer.rewrite_tuplets
    assert echoer.process_on_first_call
    assert not echoer.include_empty_measures
    echoer.min_dynamic = 'mp'
    echoer.max_steps = 1
    echoer.repetition_chance = 0.23
    echoer.disable_rewrite_meter = False
    echoer.omit_time_signatures = False
    echoer.use_multimeasure_rests = True
    echoer.boundary_depth = 1
    echoer.maximum_dot_count = 2
    echoer.rewrite_tuplets = True
    echoer.process_on_first_call = False
    echoer.include_empty_measures = True
    assert echoer.min_dynamic == 'mp'
    assert echoer.max_steps == 1
    assert echoer.repetition_chance == 0.23
    assert not echoer.disable_rewrite_meter
    assert not echoer.omit_time_signatures
    assert echoer.use_multimeasure_rests
    assert echoer.boundary_depth == 1
    assert echoer.maximum_dot_count == 2
    assert echoer.rewrite_tuplets
    assert not echoer.process_on_first_call
    assert echoer.include_empty_measures


def test_Echoer_04():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    notes = echoer.output_all()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
            c'4
            \pp
            d'4
            \ppp
            r2
            c'4
            r2.
            R1
        }
        """
    )


def test_Echoer_05():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container,
                           min_dynamic='p',
                           )
    notes = echoer.output_all()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
            c'4
            \mp
            d'4
            \p
            r2
            c'4
            r2.
            R1
        }
        """
    )
    container = abjad.Container(r"c'4\f d'4 e'4 f'4")
    echoer = auxjad.Echoer(container,
                           min_dynamic='mp',
                           )
    notes = echoer.output_all()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \f
            d'4
            e'4
            f'4
            c'4
            \mf
            d'4
            e'4
            f'4
            c'4
            \mp
            d'4
            e'4
            f'4
            R1
        }
        """
    )


def test_Echoer_06():
    container = abjad.Container(
        r"c'4\p ~ c'16 r8. r8. <d' e'>16\mp ~ <d' e'>4"
    )
    echoer = auxjad.Echoer(container)
    notes = echoer.output_all()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            ~
            c'16
            r8.
            r8.
            <d' e'>16
            \mp
            ~
            <d' e'>4
            c'4
            \pp
            ~
            c'16
            r8.
            r8.
            <d' e'>16
            \p
            ~
            <d' e'>4
            c'4
            \ppp
            ~
            c'16
            r8.
            r8.
            <d' e'>16
            \pp
            ~
            <d' e'>4
            r2
            r8.
            <d' e'>16
            \ppp
            ~
            <d' e'>4
            R1
        }
        """
    )


def test_Echoer_07():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    notes = echoer.__next__()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
        }
        """
    )
    notes = echoer.__next__()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
        }
        """
    )
    notes = echoer.__next__()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
        }
        """
    )
    echoer.min_dynamic = 'pp'
    notes = echoer.__next__()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \pp
            r2.
        }
        """
    )
    notes = echoer.__next__()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
        }
        """
    )


def test_Echoer_08():
    container = abjad.Container(r"\times 2/3 {c'8\ppp d'8\mp e'8} d'2.\pp")
    echoer = auxjad.Echoer(container)
    notes = echoer.output_all()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3
            {
                \time 4/4
                c'8
                \ppp
                d'8
                \mp
                e'8
            }
            d'2.
            \pp
            \times 2/3
            {
                r8
                d'8
                \p
                e'8
            }
            d'2.
            \ppp
            \times 2/3
            {
                r8
                d'8
                \pp
                e'8
            }
            r2.
            \times 2/3
            {
                r8
                d'8
                \ppp
                e'8
            }
            r2.
            R1
        }
        """
    )


def test_Echoer_09():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    notes = echoer.output_n(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
        }
        """
    )


def test_Echoer_10():
    container = abjad.Container(
        r"\time 3/8 c'4.\pp \time 2/4 d'2\ff \time 3/8 e'4.\mp"
    )
    echoer = auxjad.Echoer(container)
    notes = echoer.output_n(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4.
            \pp
            \time 2/4
            d'2
            \ff
            \time 3/8
            e'4.
            \mp
            c'4.
            \ppp
            \time 2/4
            d'2
            \f
            \time 3/8
            e'4.
            \p
            R1 * 3/8
            \time 2/4
            d'2
            \mf
            \time 3/8
            e'4.
            \pp
        }
        """
    )


def test_Echoer_11():
    random.seed(95537)
    container = abjad.Container(r"c'2\fff d'2\mf")
    echoer = auxjad.Echoer(container,
                           max_steps=3,
                           )
    notes = echoer.output_n(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'2
            \fff
            d'2
            \mf
            c'2
            \f
            d'2
            \p
            c'2
            \mf
            d'2
            \pp
        }
        """
    )


def test_Echoer_12():
    container = abjad.Container(r"c'4\p ~ c'16 d'8.\mp ~ d'2")
    echoer = auxjad.Echoer(container,
                           disable_rewrite_meter=True,
                           use_multimeasure_rests=False,
                           )
    notes = echoer.output_all()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            ~
            c'16
            d'8.
            \mp
            ~
            d'2
            c'4
            \pp
            ~
            c'16
            d'8.
            \p
            ~
            d'2
            c'4
            \ppp
            ~
            c'16
            d'8.
            \pp
            ~
            d'2
            r4
            r16
            d'8.
            \ppp
            ~
            d'2
            r4
            r16
            r8.
            r2
        }
        """
    )


def test_Echoer_13():
    container = abjad.Container(
        r"\time 2/4 c'4\mf d'4 \time 3/4 e'4\p f'4 g'4"
    )
    echoer = auxjad.Echoer(container,
                           omit_time_signatures=True,
                           )
    notes = echoer.output_n(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \mf
            d'4
            e'4
            \p
            f'4
            g'4
            c'4
            \mp
            d'4
            e'4
            \pp
            f'4
            g'4
            c'4
            \p
            d'4
            e'4
            \ppp
            f'4
            g'4
        }
        """
    )


def test_Echoer_14():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container,
                           process_on_first_call=True,
                           )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
        }
        """
    )


def test_Echoer_15():
    container = abjad.Container(
        r"\time 3/4 c'8.->\mf d'16 ~ d'4 e'8..--\p f'32-.\f"
    )
    echoer = auxjad.Echoer(container)
    notes = echoer.output_all()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'8.
            \mf
            - \accent
            d'16
            ~
            d'4
            e'8..
            \p
            - \tenuto
            f'32
            \f
            - \staccato
            c'8.
            \mp
            - \accent
            d'16
            ~
            d'4
            e'8..
            \pp
            - \tenuto
            f'32
            \mf
            - \staccato
            c'8.
            \p
            - \accent
            d'16
            ~
            d'4
            e'8..
            \ppp
            - \tenuto
            f'32
            \mp
            - \staccato
            c'8.
            \pp
            - \accent
            d'16
            ~
            d'4
            r8..
            f'32
            \p
            - \staccato
            c'8.
            \ppp
            - \accent
            d'16
            ~
            d'4
            r8..
            f'32
            \pp
            - \staccato
            r2
            r8..
            f'32
            \ppp
            - \staccato
            R1 * 3/4
        }
        """
    )


def test_Echoer_16():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    assert len(echoer) == 4
    container = abjad.Container(r"c'4\mf ~ c'8 d'8\mp e'4\p ~ e'8 f'8\pp")
    echoer = auxjad.Echoer(container)
    assert len(echoer) == 4
    container = abjad.Container(
        r"c'4\mf ~ c'16 r16 d'8\mp e'4\p ~ e'8 f'16\pp r16"
    )
    echoer = auxjad.Echoer(container)
    assert len(echoer) == 4
    container = abjad.Container(r"<c' e' g'>2\f <d' f'>2\p")
    echoer = auxjad.Echoer(container)
    assert len(echoer) == 2
    container = abjad.Container(r"<c' e' g'>4\f ~ <c' e' g'>16 r8. <d' f'>2\p")
    echoer = auxjad.Echoer(container)
    assert len(echoer) == 2
    container = abjad.Container(r"<c' e' g'>4\f d'4\mf <e' g' b'>4\p r4")
    echoer = auxjad.Echoer(container)
    assert len(echoer) == 3


def test_Echoer_17():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
        }
        """
    )
    echoer.contents = abjad.Container(r"c'16\f d'16 e'16 f'16 g'2.\p")
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'16
            \f
            d'16
            e'16
            f'16
            g'2.
            \p
        }
        """
    )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'16
            \mf
            d'16
            e'16
            f'16
            g'2.
            \pp
        }
        """
    )


def test_Echoer_18():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    with pytest.raises(RuntimeError):
        echoer = auxjad.Echoer(container)  # noqa: F841


def test_Echoer_19():
    container = abjad.Container(r"c'4\fp d'4\sfz e'4\spp f'4\rfz")
    echoer = auxjad.Echoer(container)
    notes = echoer.output_n(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \fp
            d'4
            \sfz
            e'4
            \spp
            f'4
            \rfz
            c'4
            \pp
            d'4
            \mf
            e'4
            \ppp
            f'4
            \mf
            c'4
            \ppp
            d'4
            \mp
            r4
            f'4
        }
        """
    )


def test_Echoer_20():
    container = abjad.Container(r"c'4.\mf d'8 e'2")
    echoer = auxjad.Echoer(container)
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            \mf
            d'8
            e'2
        }
        """
    )
    echoer = auxjad.Echoer(container,
                           boundary_depth=1,
                           )
    notes = echoer()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            ~
            c'8
            d'8
            e'2
        }
        """
    )


def test_Echoer_21():
    container = abjad.Container(r"c'2\fffff d'\ppp")
    echoer = auxjad.Echoer(container, min_dynamic='ppppp')
    notes = echoer.output_n(4)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'2
            \fffff
            d'2
            \ppp
            c'2
            \ffff
            d'2
            \pppp
            c'2
            \fff
            d'2
            \ppppp
            c'2
            \ff
            r2
        }
        """
    )


def test_Echoer_22():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    staff = abjad.Staff()
    for window in echoer:
        staff.append(window)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
            \time 4/4
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
            \time 4/4
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
            \time 4/4
            c'4
            \pp
            d'4
            \ppp
            r2
            \time 4/4
            c'4
            \ppp
            r2.
            \time 4/4
            R1
        }
        """
    )
    auxjad.mutate.remove_repeated_time_signatures(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
            c'4
            \pp
            d'4
            \ppp
            r2
            c'4
            \ppp
            r2.
            R1
        }
        """
    )


def test_Echoer_23():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container)
    assert isinstance(echoer(), abjad.Selection)
    tuplet = abjad.Tuplet('3:2', r"c'2\mf d'2\mp e'2\p")
    echoer = auxjad.Echoer(tuplet)
    assert isinstance(echoer(), abjad.Selection)
    voice = abjad.Voice(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(voice)
    assert isinstance(echoer(), abjad.Selection)
    staff = abjad.Staff(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(staff)
    assert isinstance(echoer(), abjad.Selection)
    score = abjad.Score([abjad.Staff(r"c'4\mf d'4\mp e'\p f'\pp")])
    echoer = auxjad.Echoer(score)
    assert isinstance(echoer(), abjad.Selection)
    voice = abjad.Voice(r"c'4\mf d'4\mp e'\p f'\pp")
    staff = abjad.Staff([voice])
    echoer = auxjad.Echoer(staff)
    assert isinstance(echoer(), abjad.Selection)
    staff = abjad.Staff(r"c'4\mf d'4\mp e'\p f'\pp")
    score = abjad.Score([staff])
    echoer = auxjad.Echoer(score)
    assert isinstance(echoer(), abjad.Selection)

    voice1 = abjad.Voice(r"c'4\mf d'4\mp e'\p f'\pp")
    voice2 = abjad.Voice(r"g2\ff f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        echoer = auxjad.Echoer(staff)  # noqa: F841

    staff1 = abjad.Staff(r"c'4\mf d'4\mp e'\p f'\pp")
    staff2 = abjad.Staff(r"g2\ff f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        echoer = auxjad.Echoer(score)  # noqa: F841


def test_Echoer_24():
    container = abjad.Container(
        r"\times 2/3 {c'2(\p\< d'2 e'2\ff} f'4\mf\> g'2 a'4\mp)"
    )
    echoer = auxjad.Echoer(container)
    notes = echoer.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3
            {
                \time 4/4
                c'2
                \p
                \<
                (
                d'2
                e'2
                \ff
            }
            f'4
            \mf
            \>
            g'2
            a'4
            \mp
            )
            \times 2/3
            {
                c'2
                \pp
                \<
                (
                d'2
                e'2
                \f
            }
            f'4
            \mp
            \>
            g'2
            a'4
            \p
            )
            \times 2/3
            {
                c'2
                \ppp
                \<
                (
                d'2
                e'2
                \mf
            }
            f'4
            \p
            \>
            g'2
            a'4
            \pp
            )
            \times 2/3
            {
                r1
                e'2
                \mp
                (
            }
            f'4
            \pp
            \>
            g'2
            a'4
            \ppp
            )
            \times 2/3
            {
                r1
                e'2
                \p
                (
            }
            f'4
            \ppp
            \>
            g'2
            )
            r4
            \!
        }
        """
    )


def test_Echoer_25():
    container = abjad.Container([
        auxjad.ArtificialHarmonic(r"<c' f'>2"),
        abjad.Chord(r"<c' f'>2"),
    ])
    abjad.attach(abjad.Dynamic('pp'), container[0])
    abjad.attach(abjad.Dynamic('mp'), container[1])
    echoer = auxjad.Echoer(container)
    staff = abjad.Staff(echoer.output_all())
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            <
                c'
                \tweak style #'harmonic
                f'
            >2
            \pp
            <c' f'>2
            \mp
            <
                c'
                \tweak style #'harmonic
                f'
            >2
            \ppp
            <c' f'>2
            \p
            r2
            <c' f'>2
            \pp
            r2
            <c' f'>2
            \ppp
            R1
        }
        """
    )


def test_Echoer_26():
    container = abjad.Container(r"c'4\p d'4 e' f'")
    echoer = auxjad.Echoer(container,
                           include_empty_measures=True,
                           )
    staff = abjad.Staff(echoer.output_all())
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            d'4
            e'4
            f'4
            c'4
            \pp
            d'4
            e'4
            f'4
            c'4
            \ppp
            d'4
            e'4
            f'4
            R1
        }
        """
    )
    container = abjad.Container(r"c'4\p d'4 e' f'")
    echoer = auxjad.Echoer(container,
                           include_empty_measures=False,
                           )
    staff = abjad.Staff(echoer.output_all())
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            d'4
            e'4
            f'4
            c'4
            \pp
            d'4
            e'4
            f'4
            c'4
            \ppp
            d'4
            e'4
            f'4
        }
        """
    )


def test_Echoer_27():
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container,
                           include_empty_measures=True,
                           )
    staff = abjad.Staff(echoer.output_all())
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
            c'4
            \pp
            d'4
            \ppp
            r2
            c'4
            r2.
            R1
        }
        """
    )
    container = abjad.Container(r"c'4\mf d'4\mp e'\p f'\pp")
    echoer = auxjad.Echoer(container,
                           include_empty_measures=False,
                           )
    staff = abjad.Staff(echoer.output_all())
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \mf
            d'4
            \mp
            e'4
            \p
            f'4
            \pp
            c'4
            \mp
            d'4
            \p
            e'4
            \pp
            f'4
            \ppp
            c'4
            \p
            d'4
            \pp
            e'4
            \ppp
            r4
            c'4
            \pp
            d'4
            \ppp
            r2
            c'4
            r2.
        }
        """
    )


def test_Echoer_28():
    container = abjad.Container(r"c'4\p d'4 e' f'")
    echoer = auxjad.Echoer(container,
                           process_on_first_call=False,
                           )
    staff = abjad.Staff(echoer.output_all())
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            d'4
            e'4
            f'4
            c'4
            \pp
            d'4
            e'4
            f'4
            c'4
            \ppp
            d'4
            e'4
            f'4
            R1
        }
        """
    )
    container = abjad.Container(r"c'4\p d'4 e' f'")
    echoer = auxjad.Echoer(container,
                           process_on_first_call=True,
                           )
    staff = abjad.Staff(echoer.output_all())
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \pp
            d'4
            e'4
            f'4
            c'4
            \ppp
            d'4
            e'4
            f'4
            R1
        }
        """
    )


def test_Echoer_29():
    random.seed(82361)
    container = abjad.Container(r"c'4.\f d'8\p e'4..\mf f'16\mp")
    echoer = auxjad.Echoer(container,
                           repetition_chance=0.5,
                           )
    notes = echoer.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            \f
            d'8
            \p
            e'4..
            \mf
            f'16
            \mp
            c'4.
            \f
            d'8
            \p
            e'4..
            \mf
            f'16
            \mp
            c'4.
            \mf
            d'8
            \pp
            e'4..
            \mp
            f'16
            \p
            c'4.
            \mp
            d'8
            \ppp
            e'4..
            \p
            f'16
            \pp
            c'4.
            \mp
            d'8
            \ppp
            e'4..
            \p
            f'16
            \pp
        }
        """
    )
