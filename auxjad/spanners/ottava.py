from typing import Union

import abjad

from ..indicators.NumericOttava import NumericOttava


def ottava(argument: Union[abjad.Component, abjad.Selection],
           start_ottava: Union[int, abjad.Ottava, NumericOttava] = 1,
           stop_ottava: Union[int, abjad.Ottava, NumericOttava] = 0,
           *,
           numeric_ottava: bool = False,
           selector: abjad.Expression = abjad.select().leaves(),
           tag: abjad.Tag = None,
           ) -> None:
    r"""Attaches ottava indicators.

    Basic usage:
        Basic usage is identical to |abjad.ottava()|:

        >>> staff = abjad.Staff(r"c'''4 d'''4 e'''4 f'''4")
        >>> auxjad.ottava(staff[:])
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava 1
            c'''4
            d'''4
            e'''4
            f'''4
            \ottava 0
        }

        .. figure:: ../_images/ottava-oVt2RCxQOv.png

    .. note::

        Auxjad automatically replaces its built-in |abjad.ottava()| with this
        function. Therefore it can be used either as :func:`auxjad.ottava()` or
        |abjad.ottava()|, as shown below:

        >>> staff1 = abjad.Staff(r"c'''4 d'''4 e'''4 f'''4")
        >>> staff2 = abjad.Staff(r"c'''4 d'''4 e'''4 f'''4")
        >>> auxjad.ottava(staff1[:])
        >>> abjad.ottava(staff2[:])
        >>> selections = [staff1[:], staff2[:]]
        >>> auxjad.inspect(selections).selections_are_identical()
        True

    Arguments:
        Second and third positional arguments can be :obj:`int`,
        |abjad.Ottava|, or :class:`auxjad.NumericOttava`:

        >>> staff = abjad.Staff(
        ...     r"c'''4 d'''4 e'''4 f'''4 g'''4 a'''4 b'''4 c''''4"
        ... )
        >>> auxjad.ottava(staff[:4], 1)
        >>> auxjad.ottava(staff[4:], 2)
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava 1
            c'''4
            d'''4
            e'''4
            f'''4
            \ottava 0
            \ottava 2
            g'''4
            a'''4
            b'''4
            c''''4
            \ottava 0
        }

        .. figure:: ../_images/ottava-8kzdTxmmxR.png

    ``numeric_ottava``:
        Setting ``numeric_ottava`` to ``True`` will result in
        :class:`auxjad.NumericOttava` being used instead of the default
        |abjad.Ottava| when second argument is :obj:`int`:

        >>> staff = abjad.Staff(
        ...     r"c'''4 d'''4 e'''4 f'''4 g'''4 a'''4 b'''4 c''''4"
        ... )
        >>> auxjad.ottava(staff[:4], 1, numeric_ottava=True)
        >>> auxjad.ottava(staff[4:], 2, numeric_ottava=True)
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava 1 \set Staff.ottavation = "8"
            c'''4
            d'''4
            e'''4
            f'''4
            \ottava 0
            \ottava 2 \set Staff.ottavation = "15"
            g'''4
            a'''4
            b'''4
            c''''4
            \ottava 0
        }

        .. figure:: ../_images/ottava-iYaIcOzIlk.png

        Numeric ottavation can also be used for ottava bassa notation:

        >>> staff = abjad.Staff(
        ...     r"\clef bass c,4 b,,4 a,,4 g,,4 f,,4 e,,4 d,,4 c,,4"
        ... )
        >>> auxjad.ottava(staff[:4], -1, numeric_ottava=True)
        >>> auxjad.ottava(staff[4:], -2, numeric_ottava=True)
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava -1 \set Staff.ottavation = "8"
            \clef "bass"
            c,4
            b,,4
            a,,4
            g,,4
            \ottava 0
            \ottava -2 \set Staff.ottavation = "15"
            f,,4
            e,,4
            d,,4
            c,,4
            \ottava 0
        }

        .. figure:: ../_images/ottava-3iXC4vZmiu.png
    """
    if not isinstance(start_ottava, (int, abjad.Ottava, NumericOttava)):
        raise TypeError("'start_ottava' must be 'int', 'abjad.Ottava', or "
                        "'auxjad.NumericOttava'")
    if not isinstance(stop_ottava, (int, abjad.Ottava, NumericOttava)):
        raise TypeError("'stop_ottava' must be 'int', 'abjad.Ottava', or "
                        "'auxjad.NumericOttava'")
    if not isinstance(numeric_ottava, bool):
        raise TypeError("'numeric_ottava' must be 'bool'")
    assert isinstance(selector, abjad.Expression)
    if isinstance(start_ottava, int):
        if numeric_ottava:
            start_ottava = NumericOttava(start_ottava)
        else:
            start_ottava = abjad.Ottava(start_ottava)
    if isinstance(stop_ottava, int):
        if numeric_ottava:
            stop_ottava = NumericOttava(stop_ottava, format_slot='after')
        else:
            stop_ottava = abjad.Ottava(stop_ottava, format_slot='after')
    argument = selector(argument)
    leaves = abjad.Selection(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    abjad.attach(start_ottava, start_leaf, tag=tag)
    abjad.attach(stop_ottava, stop_leaf, tag=tag)


### MONKEY PATCHING ###

abjad.spanners.ottava = ottava
abjad.ottava = ottava
