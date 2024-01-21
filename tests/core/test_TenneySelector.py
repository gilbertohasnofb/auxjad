import random

import pytest

import auxjad


def test_TenneySelector__init__():
    r"""Confirm correct initialisation of attributes."""
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    assert selector.contents == ['A', 'B', 'C', 'D', 'E', 'F']
    assert format(selector) == "['A', 'B', 'C', 'D', 'E', 'F']"
    assert selector.curvature == 1.0
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.counter == [1, 1, 1, 1, 1, 1]
    assert selector.previous_index is None
    assert selector.previous_result is None


def test_TenneySelector__call__():
    r"""Confirm correct behaviour when calling instance."""
    random.seed(43714)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'BDAFCBEFCDFDBAEDFCABDEABCDEBFE'
    assert selector.previous_index == 4
    assert selector.previous_result == 'E'
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [7.0, 2.0, 5.0, 4.0, 0.0, 1.0]


def test_TenneySelector_previous_index_and_previous_result_read_only():
    r"""Confirm attributes previous_index and previous_result are both read
    only.
    """
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    with pytest.raises(AttributeError):
        selector.previous_index = 3
    with pytest.raises(AttributeError):
        selector.previous_result = 'C'


def test_TenneySelector_concave_curvature():
    r"""Test concave curvature (0 < curvature < 1.0)."""
    random.seed(37248)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'],
                                     curvature=0.001,
                                     )
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'CDCBFECBCEBCFCEDFACDBADCADCDFE'
    assert selector.probabilities == pytest.approx(
        [1.0016107, 1.0021996, 1.0010992, 1.0006934, 0.0, 1.0]
    )


def test_TenneySelector_convex_curvature():
    r"""Test convex curvature (> 1.0)."""
    random.seed(76231)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'],
                                     curvature=15.2,
                                     )
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'DFAECBDFAECBDFAECBDFAECBDFAECB'
    assert selector.probabilities == pytest.approx(
        [17874877.4, 0.0, 1.0, 42106007735.0, 37640.548, 1416810830.9]
    )


def test_TenneySelector_non_default_weights():
    r"""Confirm values of weights and probabilities after a number of calls for
    non-default initial weights.
    """
    random.seed(14625)
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'FBEFECFDEADFEDFEDBFECDAFCEDCFE'
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [7.0, 12.0, 10.0, 15.0, 0.0, 20.0]


def test_TenneySelector__len__():
    r"""Confirm __len__ returns the correct length of contents and weights."""
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    assert len(selector) == 6
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def test_TenneySelector_weights_after_change_of_contents():
    r"""Confirm weights have the same length of contents if contents change
    after instantiation with a new length.
    """
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    selector.contents = ['A', 'B', 'C']
    assert len(selector) == 3
    assert selector.contents == ['A', 'B', 'C']
    assert selector.weights == [1.0, 1.0, 1.0]
    assert selector.probabilities == [1.0, 1.0, 1.0]


def test_TenneySelector__getitem__():
    r"""Confirm __getitem__ returns elements from a given index or index range.
    """
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    assert selector[1] == 'B'
    assert selector[1:4] == ['B', 'C', 'D']
    assert selector[:] == ['A', 'B', 'C', 'D', 'E', 'F']


def test_TenneySelector__delitem__():
    r"""Confirm __delitem__ deletes elements from a given index or index range.
    """
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    del selector[0]
    assert selector.contents == ['B', 'C', 'D', 'E', 'F']
    del selector[2:4]
    assert selector.contents == ['B', 'C', 'F']


def test_TenneySelector__setitem__():
    r"""Confirm __setitem__ can set items in specific index or index ranges.
    """
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    selector[2] = 'X'
    assert selector.contents == ['A', 'B', 'X', 'D', 'E', 'F']
    selector[5:7] = ['foo', 'bar']
    assert selector.contents == ['A', 'B', 'X', 'D', 'E', 'foo', 'bar']


def test_TenneySelector__delitem__handles_weights_probabilities_and_counter():
    r"""Confirm __delitem__ correctly handles weights, probabilities, and
    counter lists due to change in length.
    """
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.counter == [1, 1, 1, 1, 1, 1]
    del selector[0]
    assert selector.contents == ['B', 'C', 'D', 'E', 'F']
    assert selector.weights == [1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.counter == [1, 1, 1, 1, 1]
    del selector[2:4]
    assert selector.contents == ['B', 'C', 'F']
    assert selector.weights == [1.0, 5.0, 20.0]
    assert selector.probabilities == [1.0, 5.0, 20.0]
    assert selector.counter == [1, 1, 1]


def test_TenneySelector__setitem__handles_weights_probabilities_and_counter():
    r"""Confirm __setitem__ can set items in specific index or index ranges.
    """
    random.seed(51955)
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    selector()
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [2.0, 2.0, 10.0, 10.0, 0.0, 40.0]
    assert selector.counter == [2, 2, 2, 2, 0, 2]
    selector[2] = 'X'
    assert selector.contents == ['A', 'B', 'X', 'D', 'E', 'F']
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [2.0, 2.0, 10.0, 10.0, 0.0, 40.0]
    assert selector.counter == [2, 2, 2, 2, 0, 2]
    selector[5:7] = ['foo', 'bar']
    assert selector.contents == ['A', 'B', 'X', 'D', 'E', 'foo', 'bar']
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.counter == [1, 1, 1, 1, 1, 1, 1]


def test_TenneySelector_slicing_example_from_docs():
    r"""Confirm example of slicing from documentation returns expected values.
    """
    random.seed(21169)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(30):
        selector()
    assert selector.probabilities == [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]
    assert selector[2] == 'C'
    assert selector[1:4] == ['B', 'C', 'D']
    selector[2] = 'X'
    assert selector.contents == ['A', 'B', 'X', 'D', 'E', 'F']
    selector[:] = ['A', 'B', 'X', 'D', 'foo', 'bar']
    assert selector.contents == ['A', 'B', 'X', 'D', 'foo', 'bar']
    assert selector.probabilities == [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]
    del selector[0:2]
    assert selector.contents == ['X', 'D', 'foo', 'bar']
    assert selector.probabilities == [1.0, 7.0, 5.0, 0.0]
    assert 'X' in selector
    assert 'A' not in selector


def test_TenneySelector_weights_after_change_of_contents_after__call__():
    r"""Confirm weights, probabilities, and counter behave as expected when
    there's a change of contents after __call__ has been invoked (i.e.
    probabilities and counter won't be default).
    """
    random.seed(54267)
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    for _ in range(30):
        selector()
    assert len(selector) == 6
    assert selector.contents == ['A', 'B', 'C', 'D', 'E', 'F']
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [8.0, 2.0, 5.0, 15.0, 50.0, 0.0]
    assert selector.counter == [8, 2, 1, 3, 5, 0]
    selector.contents = [2, 4, 6, 8]
    assert len(selector) == 4
    assert selector.contents == [2, 4, 6, 8]
    assert selector.weights == [1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0]
    assert selector.counter == [1, 1, 1, 1]
    selector.weights = [1.2, 3.0, 2.5, 1.3]
    assert selector.weights == [1.2, 3.0, 2.5, 1.3]
    assert selector.probabilities == [1.2, 3.0, 2.5, 1.3]
    assert selector.counter == [1, 1, 1, 1]


def test_TenneySelector_curvature_property():
    r"""Confirm curvature setter."""
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    assert selector.curvature == 1.0
    selector.curvature = 0.25
    assert selector.curvature == 0.25


def test_TenneySelector_reset_probabilities():
    r"""Confirm reset_probabilities() returns uniform distribution."""
    random.seed(99651)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(30):
        selector()
    assert selector.probabilities == [4.0, 3.0, 1.0, 0.0, 5.0, 2.0]
    selector.reset_probabilities()
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def test_TenneySelector__next__():
    r"""Confirm __next__ behaves identical to __call__."""
    random.seed(12387)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    result = ''
    result += selector.__next__()
    result += selector.__next__()
    result += selector.__next__()
    result += next(selector)
    result += next(selector)
    result += next(selector)
    assert result == 'DBDFAE'


def test_TenneySelector_using_None_weights_for_uniform_weights():
    r"""Confirm weights setter returns uniform weights if input is None."""
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    selector.weights = None
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
