import abjad
import pytest

import auxjad


def test_time_signature_list_01():
    container = abjad.Container(r"\time 3/4 c'2. \time 4/4 d'1")
    time_signatures = auxjad.get.time_signature_list(container)
    assert time_signatures == [abjad.TimeSignature((3, 4)),
                               abjad.TimeSignature((4, 4)),
                               ]


def test_time_signature_list_02():
    container = abjad.Container(r"\time 3/4 c'2. d'2. e'2.")
    time_signatures = auxjad.get.time_signature_list(container)
    assert time_signatures == [abjad.TimeSignature((3, 4)),
                               None,
                               None,
                               ]


def test_time_signature_list_03():
    container = abjad.Container(r"\time 5/8 c'4 ~ c'16 \time 3/8 d'4. e'4.")
    time_signatures = auxjad.get.time_signature_list(container)
    assert time_signatures == [abjad.TimeSignature((5, 8)),
                               abjad.TimeSignature((3, 8)),
                               None,
                               ]
    time_signatures = auxjad.get.time_signature_list(
        container,
        do_not_use_none=True,
    )
    assert time_signatures == [abjad.TimeSignature((5, 8)),
                               abjad.TimeSignature((3, 8)),
                               abjad.TimeSignature((3, 8)),
                               ]


def test_time_signature_list_04():
    container = abjad.Container(r"\time 3/4 c'2. d'2. \time 3/4 e'2. f'2.")
    time_signatures = auxjad.get.time_signature_list(container)
    assert time_signatures == [abjad.TimeSignature((3, 4)),
                               None,
                               abjad.TimeSignature((3, 4)),
                               None,
                               ]
    time_signatures = auxjad.get.time_signature_list(
        container,
        omit_repeated=True,
    )
    assert time_signatures == [abjad.TimeSignature((3, 4)),
                               None,
                               None,
                               None,
                               ]


def test_time_signature_list_05():
    container = abjad.Container(
        r"\time 3/4 c'2. d'2. \time 3/4 e'2. f'2."
    )
    with pytest.raises(ValueError):
        auxjad.get.time_signature_list(container,
                                       do_not_use_none=True,
                                       omit_repeated=True,
                                       )


def test_time_signature_list_06():
    container = abjad.Container(r"c'1 d'1 e'1 f'1")
    time_signatures = auxjad.get.time_signature_list(container)
    assert time_signatures == [abjad.TimeSignature((4, 4)),
                               None,
                               None,
                               None,
                               ]
    time_signatures = auxjad.get.time_signature_list(
        container,
        implicit_common_time=False,
    )
    assert time_signatures == [None,
                               None,
                               None,
                               None,
                               ]


def test_time_signature_list_07():
    container = abjad.Container(r"\time 4/4 c'1 d'1 e'1 f'1")
    time_signatures = auxjad.get.time_signature_list(
        container,
        do_not_use_none=True,
        implicit_common_time=False,
    )
    assert time_signatures == [abjad.TimeSignature((4, 4)),
                               abjad.TimeSignature((4, 4)),
                               abjad.TimeSignature((4, 4)),
                               abjad.TimeSignature((4, 4)),
                               ]
    container = abjad.Container(r"c'1 d'1 e'1 f'1")
    with pytest.raises(ValueError):
        auxjad.get.time_signature_list(container,
                                       do_not_use_none=True,
                                       implicit_common_time=False,
                                       )
