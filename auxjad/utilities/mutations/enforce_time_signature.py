from typing import Optional, Union

import abjad

from .auto_rewrite_meter import auto_rewrite_meter
from .close_container import close_container as close_container_function
from .fill_with_rests import fill_with_rests as fill_with_rests_function


def enforce_time_signature(container: abjad.Container,
                           time_signatures: Union[abjad.TimeSignature,
                                                  tuple,
                                                  list,
                                                  ],
                           *,
                           cyclic: bool = False,
                           fill_with_rests: bool = True,
                           close_container: bool = False,
                           disable_rewrite_meter: bool = False,
                           prettify_rewrite_meter: bool = True,
                           boundary_depth: Optional[int] = None,
                           maximum_dot_count: Optional[int] = None,
                           rewrite_tuplets: bool = True,
                           extract_trivial_tuplets: bool = True,
                           fuse_across_groups_of_beats: bool = True,
                           fuse_quadruple_meter: bool = True,
                           fuse_triple_meter: bool = True,
                           split_quadruple_meter: bool = True,
                           ):
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function applies a time signature
    (or a :obj:`list` of time signatures) to the input container.

    Basic usage:
        The function mutates a container in place, applying a time signature
        to it.

        >>> staff = abjad.Staff(r"c'1 d'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/enforce_time_signature-9bf9zmnm19k.png

        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     abjad.TimeSignature((2, 4))
        ... )
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

        .. figure:: ../_images/enforce_time_signature-kerf9uos62i.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     abjad.TimeSignature((2, 4))
        ... )
        >>> abjad.mutate(staff).enforce_time_signature(
        ...     abjad.TimeSignature((2, 4))
        ... )

    Single value for second positional argument:
        The second positional argument can take either |abjad.TimeSignature|
        or a :obj:`tuple` for a single time signature (for multiple time
        signatures, use a :obj:`list` as shown further below). By default,
        rests will be appended to the end of the staff if necessary.

        >>> staff = abjad.Staff(r"c'1 d'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/enforce_time_signature-218f65bsco3.png

        >>> auxjad.mutate(staff).enforce_time_signature((3, 4))
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

        .. figure:: ../_images/enforce_time_signature-u4p457k6ib7.png

    ``close_container``:
        Set the optional keyword argument ``close_container`` to ``True`` in
        order to adjust the last measure's time signature instead of filling it
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

        .. figure:: ../_images/enforce_time_signature-tn1l53yimir.png

        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     abjad.TimeSignature((3, 4)),
        ...     close_container=True,
        ... )
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

        .. figure:: ../_images/enforce_time_signature-1uhp08fqlpl.png

    ``fill_with_rests``:
        Alternatively, to leave the last measure as it is input (i.e. not
        filling it with rests nor adjusting the time signature), set the
        optional keyword argument ``fill_with_rests`` to ``False`` (default
        value is ``True``).

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/enforce_time_signature-bit2y19hncr.png

        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     abjad.TimeSignature((3, 4)),
        ...     fill_with_rests=False,
        ... )
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

        .. figure:: ../_images/enforce_time_signature-xo7fpeqsoek.png

    Multiple values for second positional argument:
        The second argument can also take a :obj:`list` of
        |abjad.TimeSignature| or :obj:`tuple`.

        >>> staff = abjad.Staff(r"c'1 d'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/enforce_time_signature-rl1csjn9osl.png

        >>> time_signatures = [abjad.TimeSignature((3, 4)),
        ...                    abjad.TimeSignature((5, 4)),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(time_signatures)
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

        .. figure:: ../_images/enforce_time_signature-tqqrqi34bu.png

    Repeated time signatures:
        Consecutive identical time signatures are omitted. Also note that time
        signatures can also be represented as a :obj:`list` of :obj:`tuple`'s.

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/enforce_time_signature-vn9ngz2k6cd.png

        >>> time_signatures = [(2, 4),
        ...                    (2, 4),
        ...                    (4, 4),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(time_signatures)
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

        .. figure:: ../_images/enforce_time_signature-nj2c90o0pe.png

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

        .. figure:: ../_images/enforce_time_signature-2og5ld8bkxe.png

        >>> time_signatures = [(2, 4),
        ...                    None,
        ...                    None,
        ...                    (3, 4),
        ...                    None,
        ...                    (4, 4),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(time_signatures)
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

        .. figure:: ../_images/enforce_time_signature-3s9h7p1k05x.png

    ``cyclic``:
        To cycle through the :obj:`list` of time signatures until the container
        is exhausted, set the optional keyword argument ``cyclic`` to ``True``.

        >>> staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
        }

        .. figure:: ../_images/enforce_time_signature-vl1bwp21saq.png

        >>> time_signatures = [abjad.TimeSignature((3, 8)),
        ...                    abjad.TimeSignature((2, 8)),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     time_signatures,
        ...     cyclic=True,
        ... )
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

        .. figure:: ../_images/enforce_time_signature-9mq64erlth6.png

    ``disable_rewrite_meter``:
        By default, this function applies the mutation
        |abjad.mutate().rewrite_meter()| to its output.

        >>> staff = abjad.Staff(r"c'1 ~ c'4 r8 d'4. e'4")
        >>> time_signatures = [abjad.TimeSignature((5, 4)),
        ...                    abjad.TimeSignature((3, 4)),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(time_signatures)
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

        .. figure:: ../_images/enforce_time_signature-xsjbr0vnev9.png

        To disable this, set the keyword argument ``disable_rewrite_meter`` to
        ``True``.

        >>> staff = abjad.Staff(r"c'1 ~ c'4 r8 d'4. e'4")
        >>> time_signatures = [abjad.TimeSignature((5, 4)),
        ...                    abjad.TimeSignature((3, 4)),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     time_signatures,
        ...     disable_rewrite_meter=True,
        ... )
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

        .. figure:: ../_images/enforce_time_signature-ezjnpwjd3xu.png

    Tuplets:
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

        .. figure:: ../_images/enforce_time_signature-v4ndqpmqjk.png

        >>> time_signatures = [abjad.TimeSignature((2, 4)),
        ...                    abjad.TimeSignature((3, 4)),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(time_signatures)
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

        .. figure:: ../_images/enforce_time_signature-5jdoukq2rkd.png

    Time signatures in the input container:
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

        .. figure:: ../_images/enforce_time_signature-bnnz1hov5bu.png

        >>> time_signatures = [abjad.TimeSignature((5, 8)),
        ...                    abjad.TimeSignature((1, 16)),
        ...                    abjad.TimeSignature((2, 4)),
        ...                    ]
        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     time_signatures,
        ...     cyclic=True,
        ... )
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

        .. figure:: ../_images/enforce_time_signature-2l289r8sdzl.png

    Tweaking |abjad.mutate().rewrite_meter()|:
        This function uses the default logical tie splitting algorithm from
        |abjad.mutate().rewrite_meter()|.

        >>> staff = abjad.Staff(r"c'4. d'8 e'2")
        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     abjad.TimeSignature((4, 4)),
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4.
            d'8
            e'2
        }

        .. figure:: ../_images/enforce_time_signature-bykbobzx47.png

        Set ``boundary_depth`` to a different number to change its behaviour.

        >>> staff = abjad.Staff(r"c'4. d'8 e'2")
        >>> auxjad.mutate(staff).enforce_time_signature(
        ...     abjad.TimeSignature((4, 4)),
        ...     boundary_depth=1,
        ... )
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

        .. figure:: ../_images/enforce_time_signature-wljhgmjh9c.png

        Other arguments available for tweaking the output of
        |abjad.mutate().rewrite_meter()| are ``maximum_dot_count`` and
        ``rewrite_tuplets``, which work exactly as the identically named
        arguments of |abjad.mutate().rewrite_meter()|.

        This function also accepts the arguments
        ``fuse_across_groups_of_beats``, ``fuse_quadruple_meter``,
        ``fuse_triple_meter``, ``extract_trivial_tuplets``, and
        ``split_quadruple_meter``, which are passed on to
        |auxjad.mutate().prettify_rewrite_meter()| (the latter can be disabled
        by setting ``prettify_rewrite_meter`` to ``False``). See the
        documentation of this function for more details on these arguments.

    .. note::

        When using |abjad.Container|'s, all time signatures in the output will
        be commented out with ``%%%.`` This is because Abjad only applies time
        signatures to containers that belong to a |abjad.Staff|. The present
        function works with either |abjad.Container| and |abjad.Staff|.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> abjad.f(container)
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/enforce_time_signature-ntl3jgbi7j.png

        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/enforce_time_signature-y5sjtx3j0v.png

    .. warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first argument must be 'abjad.Container' or "
                        "child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("first argument must be contiguous logical voice")
    if isinstance(time_signatures, list):
        time_signatures_ = time_signatures[:]
    else:
        time_signatures_ = [time_signatures]
    if time_signatures_[0] is None:
        raise ValueError("first element of the input list must not be 'None'")
    # converting all elements to abjad.TimeSignature
    for index, time_signature in enumerate(time_signatures_):
        if time_signature is None:
            previous_ts_duration = time_signatures_[index - 1].pair
            time_signatures_[index] = abjad.TimeSignature(previous_ts_duration)
        elif not isinstance(time_signature, abjad.TimeSignature):
            time_signatures_[index] = abjad.TimeSignature(time_signature)
    partial_time_signature = None
    if time_signatures_[0].partial is not None:
        partial_time_signature = time_signatures_[0]
        time_signatures_[0] = abjad.TimeSignature(
            partial_time_signature.duration
        )
        partial_element = abjad.TimeSignature(partial_time_signature.partial)
        time_signatures_.insert(0, partial_element)
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
    if not isinstance(split_quadruple_meter, bool):
        raise TypeError("'split_quadruple_meter' must be 'bool'")
    # remove all time signatures from container
    for leaf in abjad.select(container).leaves():
        if abjad.inspect(leaf).indicators(abjad.TimeSignature):
            abjad.detach(abjad.TimeSignature, leaf)
    # slice container at the places where time signatures change
    durations = [time_signature.duration for time_signature
                 in time_signatures_]
    if not cyclic:
        while sum(durations) < abjad.inspect(container).duration():
            durations.append(durations[-1])
    abjad.mutate(container[:]).split(durations, cyclic=cyclic)
    # attach new time signatures
    previous_ts = None
    index = 0
    duration = abjad.Duration(0)
    previous_ts_duration = abjad.Duration(0)
    for leaf in abjad.select(container).leaves():
        if duration == previous_ts_duration:
            duration = abjad.Duration(0)
            previous_ts_duration = durations[index]
            if partial_time_signature is not None and index in (0, 1):
                ts = partial_time_signature
            else:
                ts = time_signatures_[index]
            if ts != previous_ts:
                abjad.attach(ts, leaf)
            previous_ts = ts
            index += 1
            if index == len(time_signatures_):
                if cyclic:
                    index = 0
                else:
                    break
        duration += abjad.inspect(leaf).duration()
    # filling with rests or closing container
    if close_container:
        close_container_function(container)
    elif fill_with_rests:
        fill_with_rests_function(
            container,
            disable_rewrite_meter=disable_rewrite_meter,
        )
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
        auto_rewrite_meter(
            container,
            meter_list=time_signatures_,
            boundary_depth=boundary_depth,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
            prettify_rewrite_meter=prettify_rewrite_meter,
            extract_trivial_tuplets=extract_trivial_tuplets,
            fuse_across_groups_of_beats=fuse_across_groups_of_beats,
            fuse_quadruple_meter=fuse_quadruple_meter,
            fuse_triple_meter=fuse_triple_meter,
            split_quadruple_meter=split_quadruple_meter,
        )
