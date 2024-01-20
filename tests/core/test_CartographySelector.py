import random

import pytest

import auxjad


def test_CartographySelector__init__():
    r"""Confirm correct initialisation of attributes.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    assert selector.contents == [0, 1, 2, 3, 4]
    assert format(selector) == '[0, 1, 2, 3, 4]'
    assert selector.weights == pytest.approx(
        [1.0, 0.75, 0.5625, 0.421875, 0.31640625],
    )
    assert selector.previous_index is None
    assert selector.previous_result is None
    with pytest.raises(AttributeError):
        selector.previous_index = 3
        selector.previous_result = 7


def test_CartographySelector__call__():
    r"""Confirm correct behaviour when calling instance.
    """
    random.seed(41298)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    assert selector.previous_index is None
    assert selector.previous_result is None
    result = ''
    for _ in range(30):
        result += str(selector())
    assert result == '203001402200011111101400310140'
    assert selector.previous_index == 0
    assert selector.previous_result == 0


def test_CartographySelector_decay_rate():
    r"""Confirm decay_rate argument in __init__ correctly initialises weights.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4], decay_rate=0.5)
    assert selector.weights == [1.0, 0.5, 0.25, 0.125, 0.0625]


def test_CartographySelector_drop_first_and_append():
    r"""Confirm drop_first_and_append() appends input to list and drops first
    element.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.drop_first_and_append(5)
    assert selector.contents == [1, 2, 3, 4, 5]
    selector.drop_first_and_append(42)
    assert selector.contents == [2, 3, 4, 5, 42]


def test_CartographySelector_drop_n_and_append():
    r"""Confirm drop_n_and_append() drops n-th element and appends new element
    at the end of the list.
    """
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    selector.drop_n_and_append(100, n=2)
    assert selector.contents == [10, 7, 31, 98, 100]


def test_CartographySelector_drop_last_and_prepend():
    r"""Confirm drop_last_and_prepend() drops last element and prepends input
    at index 0.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.drop_last_and_prepend(-1)
    assert selector.contents == [-1, 0, 1, 2, 3]
    selector.drop_last_and_prepend(71)
    assert selector.contents == [71, -1, 0, 1, 2]


def test_CartographySelector_rotate():
    r"""Confirm rotate() moves all elements from index n to index n + 1, with
    the last element moving into index 0.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.rotate()
    assert selector.contents == [1, 2, 3, 4, 0]
    selector.rotate(anticlockwise=True)
    assert selector.contents == [0, 1, 2, 3, 4]
    selector.rotate(anticlockwise=True)
    assert selector.contents == [4, 0, 1, 2, 3]


def test_CartographySelector_shuffle():
    r"""Confirm shuffle() will shuffle the selector's contents."""
    random.seed(15424)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.shuffle()
    assert selector.contents == [1, 4, 3, 0, 2]


def test_CartographySelector__len__():
    r"""Confirm __len__ returns the correct length of contents and weights."""
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4], decay_rate=0.5)
    assert len(selector) == 5
    selector.contents = [0, 1, 2, 3, 4]
    assert selector.weights == [1.0, 0.5, 0.25, 0.125, 0.0625]


def test_CartographySelector_weights_after_change_of_contents():
    r"""Confirm weights have the same length of contents if contents change
    after instantiation with a new length.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4], decay_rate=0.5)
    selector.contents = [10, 7, 14, 31, 98, 47, 32]
    assert len(selector) == 7
    assert selector.contents == [10, 7, 14, 31, 98, 47, 32]
    assert selector.weights == [1.0,
                                0.5,
                                0.25,
                                0.125,
                                0.0625,
                                0.03125,
                                0.015625,
                                ]


def test_CartographySelector_change_decay_rate():
    r"""Confirm decay_rate change after instantiation results in the correct
    weights attribute.
    """
    random.seed(83552)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.decay_rate = 0.2
    assert selector.weights == pytest.approx([1.0, 0.2, 0.04, 0.008, 0.0016])
    result = ''
    for _ in range(30):
        result += str(selector())
    assert result == '000001002100000201001030000100'


def test_CartographySelector_11():
    r"""
    """
    random.seed(19844)
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    assert selector() == 31
    assert selector.previous_index == 3
    assert selector.previous_result == 31


def test_CartographySelector__getitem__():
    r"""Confirm __getitem__ returns elements from a given index or index range.
    """
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    assert selector[1] == 7
    assert selector[1:4] == [7, 14, 31]
    assert selector[:] == [10, 7, 14, 31, 98]


def test_CartographySelector__delitem__():
    r"""Confirm __delitem__ deletes elements from a given index or index range.
    """
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    del selector[0]
    assert selector.contents == [7, 14, 31, 98]
    del selector[2:4]
    assert selector.contents == [7, 14]


def test_CartographySelector__setitem__():
    r"""Confirm __setitem__ can set items in specific index or index ranges.
    """
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    selector[2] = 207
    assert selector.contents == [10, 7, 207, 31, 98]
    selector[3:5] = [42, 43]
    assert selector.contents == [10, 7, 207, 42, 43]


def test_CartographySelector__delitem__regenerates_weights():
    r"""Confirm __delitem__ regenerates weights due to change in length."""
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    del selector[0]
    assert selector.contents == [1, 2, 3, 4]
    assert selector.weights == [1.0, 0.75, 0.5625, 0.421875]
    del selector[2:4]
    assert selector.contents == [1, 2]
    assert selector.weights == [1.0, 0.75]


def test_CartographySelector__setitem__regenerates_weights():
    r"""Confirm __setitem__ can set items in specific index or index ranges.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector[2] = 207
    assert selector.contents == [0, 1, 207, 3, 4]
    assert selector.weights == pytest.approx(
        [1.0, 0.75, 0.5625, 0.421875, 0.31640625],
    )
    selector[5:7] = [42, 43]
    assert selector.contents == [0, 1, 207, 3, 4, 42, 43]
    assert selector.weights == pytest.approx(
        [1.0, 0.75, 0.5625, 0.421875, 0.31640625, 0.237304687, 0.177978515],
    )


def test_CartographySelector_no_repeat():
    r"""Confirm the argument no_repeat in __call__ returns values without
    consecutive repeats.
    """
    random.seed(98743)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    result = ''
    for _ in range(30):
        result += str(selector())
    assert result == '210431340000344203001220034203'
    result = ''
    for _ in range(30):
        result += str(selector(no_repeat=True))
    assert result == '210421021020304024230120241202'


def test_CartographySelector_mirror_swap_odd_elements():
    r"""Confirm mirror_swap() swaps the element at a given index with its
    complementary element. Testing with odd number of elements in contents.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.mirror_swap(0)
    assert selector.contents == [4, 1, 2, 3, 0]
    selector.mirror_swap(0)
    assert selector.contents == [0, 1, 2, 3, 4]
    selector.mirror_swap(3)
    assert selector.contents == [0, 3, 2, 1, 4]
    selector.mirror_swap(2)
    assert selector.contents == [0, 3, 2, 1, 4]


def test_CartographySelector_mirror_swap_even_elements():
    r"""Confirm mirror_swap() swaps the element at a given index with its
    complementary element. Testing with even number of elements in contents.
    """
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4, 5])
    selector.mirror_swap(0)
    assert selector.contents == [5, 1, 2, 3, 4, 0]
    selector.mirror_swap(0)
    assert selector.contents == [0, 1, 2, 3, 4, 5]
    selector.mirror_swap(3)
    assert selector.contents == [0, 1, 3, 2, 4, 5]
    selector.mirror_swap(2)
    assert selector.contents == [0, 1, 2, 3, 4, 5]


def test_CartographySelector_mirror_random_swap():
    r"""Confirm mirror_random_swap() swaps a randomly selected element at a
    given index with its complementary element.
    """
    random.seed(90129)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.mirror_random_swap()
    assert selector.contents == [4, 1, 2, 3, 0]
    selector.mirror_random_swap()
    assert selector.contents == [4, 3, 2, 1, 0]
    selector.mirror_random_swap()
    assert selector.contents == [4, 1, 2, 3, 0]


def test_CartographySelector__next__():
    r"""Confirm __next__ behaves identical to __call__."""
    random.seed(12387)
    selector = auxjad.CartographySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    result = ''
    result += selector.__next__()
    result += selector.__next__()
    result += selector.__next__()
    result += next(selector)
    result += next(selector)
    result += next(selector)
    assert result == 'CBBEAE'
