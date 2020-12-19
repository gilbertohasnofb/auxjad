from typing import Union

import abjad

from ..indicators.NumericOttava import NumericOttava


def numeric_ottava(argument: Union[abjad.Component, abjad.Selection],
                   start_ottava: Union[int, NumericOttava] = 1,
                   stop_ottava: Union[int, NumericOttava] = 0,
                   *,
                   selector: abjad.Expression = abjad.select().leaves(),
                   tag: abjad.Tag = None,
                   ) -> None:
    r"""Attaches numeric ottava indicators (:class:`auxjad.NumericOttava`).

    Basic usage:
        Usage is similar to |abjad.ottava()|:

        >>> staff = abjad.Staff(
        ...     r"c'''4 d'''4 e'''4 f'''4 g'''4 a'''4 b'''4 c''''4"
        ... )
        >>> auxjad.numeric_ottava(staff[:4], 1)
        >>> auxjad.numeric_ottava(staff[4:], 2)
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava #1 \set Staff.ottavation = "8"
            c'''4
            d'''4
            e'''4
            f'''4
            \ottava #0
            \ottava #2 \set Staff.ottavation = "15"
            g'''4
            a'''4
            b'''4
            c''''4
            \ottava #0
        }

        .. figure:: ../_images/numeric_ottava-iYaIcOzIlk.png

        Numeric ottavation is also used for ottava bassa:

        >>> staff = abjad.Staff(
        ...     r"\clef bass c,4 b,,4 a,,4 g,,4 f,,4 e,,4 d,,4 c,,4"
        ... )
        >>> auxjad.numeric_ottava(staff[:4], -1)
        >>> auxjad.numeric_ottava(staff[4:], -2)
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava #-1 \set Staff.ottavation = "8"
            \clef "bass"
            c,4
            b,,4
            a,,4
            g,,4
            \ottava #0
            \ottava #-2 \set Staff.ottavation = "15"
            f,,4
            e,,4
            d,,4
            c,,4
            \ottava #0
        }

        .. figure:: ../_images/numeric_ottava-3iXC4vZmiu.png
    """
    if not isinstance(start_ottava, (int, NumericOttava)):
        raise TypeError("'start_ottava' must be 'int' or "
                        "'auxjad.NumericOttava'")
    if not isinstance(stop_ottava, (int, NumericOttava)):
        raise TypeError("'stop_ottava' must be 'int' or "
                        "'auxjad.NumericOttava'")
    assert isinstance(selector, abjad.Expression)
    if isinstance(start_ottava, int):
        start_ottava = NumericOttava(start_ottava)
    if isinstance(stop_ottava, int):
        stop_ottava = NumericOttava(stop_ottava, format_slot='after')
    argument = selector(argument)
    leaves = abjad.Selection(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    abjad.attach(start_ottava, start_leaf, tag=tag)
    abjad.attach(stop_ottava, stop_leaf, tag=tag)
