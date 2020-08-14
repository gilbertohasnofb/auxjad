import abjad

from ..inspect import inspect
from .extract_trivial_tuplets import (
    extract_trivial_tuplets as extract_trivial_tuplets_function,
)
from .prettify_rewrite_meter import prettify_rewrite_meter


def auto_rewrite_meter(container: abjad.Container,
                       meter_list: list = None,
                       *,
                       prettify: bool = True,
                       extract_trivial_tuplets: bool = True,
                       ):
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function takes every measure of a
    container, detects its time signature, and apply both
    |abjad.mutate().rewrite_meter()| and
    |auxjad.mutate().prettify_rewrite_meter()| to it.

    Basic usage:
        This function can be call simply on a container.

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"c'16 d'8 e'16 f'8 g'4 a'4 b'8")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
        }

        .. figure:: ../_images/image-auto_rewrite_meter-1.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.mutate(staff).auto_rewrite_meter()

    Time signature changes:
        It automatically handles time signature changes.

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"\time 6/8 b'4 c''4 r4 ")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
            \time 6/8
            b'4
            c''8
            ~
            c''8
            r4
        }

        .. figure:: ../_images/image-auto_rewrite_meter-2.png

    ``prettify``:
        By default, this function invokes both |abjad.mutate().rewrite_meter()|
        and |auxjad.mutate().prettify_rewrite_meter()|.

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"c'16 d'8 e'16 f'8 g'4 a'4 b'8")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
        }

        .. figure:: ../_images/image-auto_rewrite_meter-3.png

        Set ``prettify`` to ``False`` to not invoke
        |auxjad.mutate().prettify_rewrite_meter()|.

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"c'16 d'8 e'16 f'8 g'4 a'4 b'8")
        >>> auxjad.mutate(staff).auto_rewrite_meter(prettify=False)
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'16
            ~
            d'16
            e'16
            f'8
            g'8
            ~
            g'8
            a'8
            ~
            a'8
            b'8
            c'16
            d'16
            ~
            d'16
            e'16
            f'8
            g'8
            ~
            g'8
            a'8
            ~
            a'8
            b'8
        }

        .. figure:: ../_images/image-auto_rewrite_meter-4.png

    ``meter_list``:
        When no ``meter_list`` is supplied, this function detects the time
        signature of each measure and uses those when rewritting it:

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8 "
        ...                     r"\time 5/4 d''8 e''4 f''4 g''4 a''4 b''8")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 7/4
            c'8
            d'4
            e'4
            f'8
            ~
            f'8
            g'4
            a'8
            ~
            a'8
            b'4
            c''8
            \time 5/4
            d''8
            e''4
            f''4
            g''8
            ~
            g''8
            a''4
            b''8
        }

        .. figure:: ../_images/image-auto_rewrite_meter-5.png

        To use a custom list of meters (one for each measure), set
        ``meter_list`` to a :obj:`list` of |abjad.Meter|'s or
        |abjad.TimeSignature|'s.

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8 "
        ...                     r"\time 5/4 d''8 e''4 f''4 g''4 a''4 b''8")
        >>> meter_list = [abjad.Meter((7, 4), increase_monotonic=True),
        ...               abjad.Meter((5, 4), increase_monotonic=True),
        ...               ]
        >>> auxjad.mutate(staff).auto_rewrite_meter(meter_list=meter_list)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 7/4
            c'8
            d'4
            e'8
            ~
            e'8
            f'4
            g'8
            ~
            g'8
            a'4
            b'4
            c''8
            \time 5/4
            d''8
            e''4
            f''8
            ~
            f''8
            g''4
            a''4
            b''8
        }

        .. figure:: ../_images/image-auto_rewrite_meter-6.png

    Number of measures:
        This function handles a container with any number of measures and any
        number of time signature changes:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'8 d'4 e'4 f'8 "
        ...     r"\time 5/8 g'4 a'4 r8 "
        ...     r"\time 6/8 b'4 c''4 r4 "
        ...     r"\time 4/4 d''8 e''4 f''8 g''16 a''4 r8."
        ... )
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'4
            e'4
            f'8
            \time 5/8
            g'4
            a'8
            ~
            a'8
            r8
            \time 6/8
            b'4
            c''8
            ~
            c''8
            r4
            \time 4/4
            d''8
            e''4
            f''8
            g''16
            a''8.
            ~
            a''16
            r8.
        }

        .. figure:: ../_images/image-auto_rewrite_meter-7.png

    ``extract_trivial_tuplets``:
        By default, tuplets filled with rests or tied notes or chords are
        extracted:

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        ...     r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
        ... )
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \times 2/3 {
                d'8
                r4
            }
            r4
            <e' g'>4
        }

        .. figure:: ../_images/image-auto_rewrite_meter-8.png

        Set ``extract_trivial_tuplets`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        ...     r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
        ... )
        >>> auxjad.mutate(staff).auto_rewrite_meter(
        ...     extract_trivial_tuplets=False
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'4.
            }
            \times 2/3 {
                d'8
                r4
            }
            \times 2/3 {
                r4.
            }
            \times 2/3 {
                <e' g'>4.
            }
        }

        .. figure:: ../_images/image-auto_rewrite_meter-9.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first positional argument must be 'abjad.Container' "
                        "or child class")
    if meter_list is not None:
        if not isinstance(meter_list, list):
            raise TypeError("'meter_list' must be a 'list' of 'abjad.Meter' "
                            "or 'abjad.TimeSignature'")
        else:
            for meter in meter_list:
                if not isinstance(meter, (abjad.Meter, abjad.TimeSignature)):
                    raise TypeError("elements of 'meter_list' must be "
                                    "'abjad.Meter' or 'abjad.TimeSignature'")
                if isinstance(meter, abjad.TimeSignature):
                    meter = abjad.Meter(meter.pair)
    if not isinstance(prettify, bool):
        raise TypeError("'prettify' must be 'bool'")

    if extract_trivial_tuplets:
        extract_trivial_tuplets_function(abjad.select(container))

    if meter_list is None:
        time_signatures = inspect(container).time_signature_extractor(
            do_not_use_none=True,
        )
        meter_list = [abjad.Meter(ts.pair) for ts in time_signatures]
    measures = abjad.select(container[:]).group_by_measure()
    for meter, measure in zip(meter_list, measures):
        abjad.mutate(measure).rewrite_meter(meter)
    if prettify:
        measures = abjad.select(container[:]).group_by_measure()
        for meter, measure in zip(meter_list, measures):
            prettify_rewrite_meter(
                measure,
                meter,
                extract_trivial_tuplets=extract_trivial_tuplets,
            )
