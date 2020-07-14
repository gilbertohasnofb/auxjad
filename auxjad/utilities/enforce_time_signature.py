from typing import Optional, Union

import abjad

from .close_container import close_container as close_container_function
from .fill_with_rests import fill_with_rests as fill_with_rests_function


def enforce_time_signature(container: abjad.Container,
                           time_signatures: Union[abjad.TimeSignature, tuple,
                                                  list],
                           *,
                           cyclic: bool = False,
                           fill_with_rests: bool = True,
                           close_container: bool = False,
                           disable_rewrite_meter: bool = False,
                           boundary_depth: Optional[int] = None,
                           maximum_dot_count: Optional[int] = None,
                           rewrite_tuplets: bool = True,
                           ):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function applies a time signature
    (or a list of time signatures) to the input container.

    Example:
        The function mutates a container in place, applying a time signature
        to it.

        >>> staff = abjad.Staff(r"c'1 d'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/image-enforce_time_signature-1.png

        >>> auxjad.enforce_time_signature(staff, abjad.TimeSignature((2, 4)))
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'2
            ~
            c'2
            d'2
            ~
            d'2
        }

        .. figure:: ../_images/image-enforce_time_signature-2.png

    Example:
        The second positional argument can take either ``abjad.TimeSignature``
        or a ``tuple`` for a single time signature (for multiple time
        signatures, use a ``list`` as shown further below). By default,
        rests will be appended to the end of the staff if necessary.

        >>> staff = abjad.Staff(r"c'1 d'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/image-enforce_time_signature-3.png

        >>> auxjad.enforce_time_signature(staff, (3, 4))
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            c'4
            d'2
            ~
            d'2
            r4
        }

        .. figure:: ../_images/image-enforce_time_signature-4.png

    Example:
        Set the optional keyword argument ``close_container`` to ``True`` in
        order to adjust the last bar's time signature instead of filling it
        with rests.

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-5.png

        >>> auxjad.enforce_time_signature(staff,
        ...                               abjad.TimeSignature((3, 4)),
        ...                               close_container=True,
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            c'4
            d'2
            ~
            d'2
            e'4
            ~
            e'2.
            f'2.
            ~
            \time 1/4
            f'4
        }

        .. figure:: ../_images/image-enforce_time_signature-6.png

    Example:
        Alternatively, to leave the last bar as it is input (i.e. not filling
        it with rests nor adjusting the time signature), set the optional
        keyword argument ``fill_with_rests`` to ``False`` (default value is
        ``True``).

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-7.png

        >>> auxjad.enforce_time_signature(staff,
        ...                               abjad.TimeSignature((3, 4)),
        ...                               fill_with_rests=False,
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            c'4
            d'2
            ~
            d'2
            e'4
            ~
            e'2.
            f'2.
            ~
            f'4
        }

        .. figure:: ../_images/image-enforce_time_signature-8.png

    Example:
        The second argument can also take a ``list`` of ``abjad.TimeSignature``
        or ``tuple``.

        >>> staff = abjad.Staff(r"c'1 d'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/image-enforce_time_signature-9.png

        >>> time_signatures = [abjad.TimeSignature((3, 4)),
        ...                    abjad.TimeSignature((5, 4)),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff, time_signatures)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            \time 5/4
            c'4
            d'1
        }

        .. figure:: ../_images/image-enforce_time_signature-10.png

    Example:
        Consecutive identical time signatures are omitted. Also note that time
        signatures can also be represented as a ``list`` of ``tuples``.

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-11.png

        >>> time_signatures = [(2, 4),
        ...                    (2, 4),
        ...                    (4, 4),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff, time_signatures)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'2
            ~
            c'2
            \time 4/4
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-12.png

        Alternatively, use ``None`` to indicate repeated time signatures:

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-13.png

        >>> time_signatures = [(2, 4),
        ...                    None,
        ...                    None,
        ...                    (3, 4),
        ...                    None,
        ...                    (4, 4),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff, time_signatures)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'2
            ~
            c'2
            d'2
            ~
            \time 3/4
            d'2
            e'4
            ~
            e'2.
            \time 4/4
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-14.png

    Example:
        To cycle through the list of time signatures until the container is
        exhausted, set the optional keyword argument ``cyclic`` to ``True``.

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-15.png

        >>> time_signatures = [abjad.TimeSignature((3, 8)),
        ...                    abjad.TimeSignature((2, 8)),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff,
        ...                               time_signatures,
        ...                               cyclic=True,
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4.
            ~
            \time 2/8
            c'4
            ~
            \time 3/8
            c'4.
            \time 2/8
            d'4
            ~
            \time 3/8
            d'4.
            ~
            \time 2/8
            d'4
            ~
            \time 3/8
            d'8
            e'4
            ~
            \time 2/8
            e'4
            ~
            \time 3/8
            e'4.
            ~
            \time 2/8
            e'8
            f'8
            ~
            \time 3/8
            f'4.
            ~
            \time 2/8
            f'4
            ~
            \time 3/8
            f'4
            r8
        }

        .. figure:: ../_images/image-enforce_time_signature-16.png

    Example:
        By default, this function appled the mutation ``rewrite_meter()`` to
        its output.

        >>> staff = abjad.Staff(r"c'1 ~ c'4 r8 d'4. e'4")
        >>> time_signatures = [abjad.TimeSignature((5, 4)),
        ...                    abjad.TimeSignature((3, 4)),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff,
        ...                               time_signatures,
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/4
            c'2.
            ~
            c'2
            \time 3/4
            r8
            d'4.
            e'4
        }

        .. figure:: ../_images/image-enforce_time_signature-17.png

        To disable this, set the keyword argument ``disable_rewrite_meter`` to
        ``True``.

        >>> staff = abjad.Staff(r"c'1 ~ c'4 r8 d'4. e'4")
        >>> time_signatures = [abjad.TimeSignature((5, 4)),
        ...                    abjad.TimeSignature((3, 4)),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff,
        ...                               time_signatures,
        ...                               disable_rewrite_meter=True,
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/4
            c'1
            ~
            c'4
            \time 3/4
            r8
            d'4.
            e'4
        }

        .. figure:: ../_images/image-enforce_time_signature-18.png

    Example:
        The function handles tuplets, even if they must be split.

        >>> staff = abjad.Staff(r"\times 2/3 {c'2 d'2 e'2} f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'2
                d'2
                e'2
            }
            f'1
        }

        .. figure:: ../_images/image-enforce_time_signature-19.png

        >>> time_signatures = [abjad.TimeSignature((2, 4)),
        ...                    abjad.TimeSignature((3, 4)),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff, time_signatures)
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                \time 2/4
                c'2
                d'4
                ~
            }
            \times 2/3 {
                \time 3/4
                d'4
                e'2
            }
            f'4
            ~
            f'2.
        }

        .. figure:: ../_images/image-enforce_time_signature-20.png

    Example:
        Note that any time signatures in the input container will be ignored.

        >>> staff = abjad.Staff(r"\time 3/4 c'2. d'2. e'2. f'2.")
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            d'2.
            e'2.
            f'2.
        }

        .. figure:: ../_images/image-enforce_time_signature-21.png

        >>> time_signatures = [abjad.TimeSignature((5, 8)),
        ...                    abjad.TimeSignature((1, 16)),
        ...                    abjad.TimeSignature((2, 4)),
        ...                    ]
        >>> auxjad.enforce_time_signature(staff,
        ...                               time_signatures,
        ...                               cyclic=True,
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/8
            c'4.
            ~
            c'4
            ~
            \time 1/16
            c'16
            ~
            \time 2/4
            c'16
            d'4..
            ~
            \time 5/8
            d'4
            ~
            d'16
            e'16
            ~
            e'4
            ~
            \time 1/16
            e'16
            ~
            \time 2/4
            e'4.
            f'8
            ~
            \time 5/8
            f'4.
            ~
            f'4
        }

        .. figure:: ../_images/image-enforce_time_signature-22.png

    Example:
        This function uses the default logical tie splitting algorithm from
        abjad's ``rewrite_meter()``.

        >>> staff = abjad.Staff(r"c'4. d'8 e'2")
        >>> auxjad.enforce_time_signature(staff,
        ...                               abjad.TimeSignature((4, 4)),
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4.
            d'8
            e'2
        }

        .. figure:: ../_images/image-enforce_time_signature-23.png

        Set ``boundary_depth`` to a different number to change its behaviour.

        >>> staff = abjad.Staff(r"c'4. d'8 e'2")
        >>> auxjad.enforce_time_signature(staff,
        ...                               abjad.TimeSignature((4, 4)),
        ...                               boundary_depth=1,
        ...                               )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'8
            d'8
            e'2
        }

        .. figure:: ../_images/image-enforce_time_signature-24.png

        Other arguments available for tweaking the output of abjad's
        ``rewrite_meter()`` are ``maximum_dot_count`` and ``rewrite_tuplets``,
        which work exactly as the identically named arguments of
        ``rewrite_meter()``.

    .. note::

        It is important to notice that the time signatures in the output are
        commented out with ``%%%`` if the input is of type ``abjad.Container``.
        This is because Abjad only applies time signatures to containers that
        belong to a ``abjad.Staff``. The present function works with either
        ``abjad.Container`` and ``abjad.Staff``.

        >>> container = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'4")
        >>> abjad.f(container)
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            g'4
        }
        >>> auxjad.enforce_time_signature(container,
        ...                               abjad.TimeSignature((3, 4)),
        ...                               )
        >>> abjad.f(container)
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            f'4
            g'4
            r4
        }
        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            c'4
            d'4
            e'4
            f'4
            g'4
            r4
        }
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first argument must be 'abjad.Container' or "
                        "child class")
    if isinstance(time_signatures, list):
        time_signatures_ = time_signatures[:]
    else:
        time_signatures_ = [time_signatures]
    if time_signatures_[0] is None:
        raise ValueError("first element of the input list must not be 'None'")
    # converting all elements to abjad.TimeSignature
    for index in range(len(time_signatures_)):
        time_signature = time_signatures_[index]
        if time_signature is None:
            previous_ts_duration = time_signatures_[index - 1].pair
            time_signatures_[index] = abjad.TimeSignature(previous_ts_duration)
        elif not isinstance(time_signature, abjad.TimeSignature):
            time_signatures_[index] = abjad.TimeSignature(time_signature)
    partial_time_signature = None
    if time_signatures_[0].partial is not None:
        partial_time_signature = time_signatures_[0]
        time_signatures_[0] = abjad.TimeSignature(
            partial_time_signature.duration)
        time_signatures_.insert(0, abjad.TimeSignature(
            partial_time_signature.partial))
    if not isinstance(cyclic, bool):
        raise TypeError("'cyclic' must be 'bool'")
    if not isinstance(fill_with_rests, bool):
        raise TypeError("'fill_with_rests' must be 'bool'")
    if not isinstance(close_container, bool):
        raise TypeError("'close_container' must be 'bool'")
    if not isinstance(disable_rewrite_meter, bool):
        raise TypeError("'disable_rewrite_meter' must be 'bool'")
    if boundary_depth is not None:
        if not isinstance(boundary_depth, int):
            raise TypeError("'boundary_depth' must be 'int'")
    if maximum_dot_count is not None:
        if not isinstance(maximum_dot_count, int):
            raise TypeError("'maximum_dot_count' must be 'int'")
    if not isinstance(rewrite_tuplets, bool):
        raise TypeError("'rewrite_tuplets' must be 'bool'")
    # remove all time signatures from container
    for leaf in abjad.select(container).leaves():
        if abjad.inspect(leaf).indicators(abjad.TimeSignature):
            abjad.detach(abjad.TimeSignature, leaf)
    # slice container at the places where time signatures change
    durations = [time_signature.duration for time_signature
                 in time_signatures_]
    if cyclic:
        abjad.mutate(container[:]).split(durations, cyclic=True)
    else:
        while sum(durations) < abjad.inspect(container).duration():
            durations.append(durations[-1])
        abjad.mutate(container[:]).split(durations)
    # attach new time signatures
    previous_ts = None
    ts_index = 0
    duration = abjad.Duration(0)
    previous_ts_duration = abjad.Duration(0)
    for leaf in abjad.select(container).leaves():
        if duration == previous_ts_duration:
            duration = abjad.Duration(0)
            previous_ts_duration = durations[ts_index]
            if partial_time_signature is not None and ts_index in (0, 1):
                ts = partial_time_signature
            else:
                ts = time_signatures_[ts_index]
            if ts != previous_ts:
                abjad.attach(ts, leaf)
            previous_ts = ts
            ts_index += 1
            if ts_index == len(time_signatures_):
                if cyclic:
                    ts_index = 0
                else:
                    break
        duration += abjad.inspect(leaf).duration()
    # filling with rests or closing container
    if close_container:
        close_container_function(container)
    elif fill_with_rests:
        fill_with_rests_function(container)
    # rewrite meter
    if not disable_rewrite_meter:
        measures = abjad.select(container[:]).group_by_measure()
        if cyclic:
            pattern = time_signatures_[:]
            while len(time_signatures_) < len(measures):
                time_signatures_ += pattern[:]
        else:
            while len(time_signatures_) < len(measures):
                time_signatures_.append(time_signatures_[-1])
        for measure, time_signature in zip(measures, time_signatures_):
            abjad.mutate(measure).rewrite_meter(
                time_signature,
                boundary_depth=boundary_depth,
                maximum_dot_count=maximum_dot_count,
                rewrite_tuplets=rewrite_tuplets,
            )
