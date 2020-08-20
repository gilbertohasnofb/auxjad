import random
from typing import Optional, Union

import abjad

from ..utilities.inspect import inspect
from ..utilities.mutate import mutate


class Shuffler:
    r"""This class takes an input |abjad.Container| (or child class) and
    shuffles or rotates its logical ties or pitches. When shuffling or rotating
    pitches only, tuplets are supported, otherwise tuplets are not supported.

    Basic usage:
        Calling the object will output a shuffled selection of the input
        container.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }

        .. figure:: ../_images/Shuffler-z2om98675v.png

        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            e'4
            d'4
            f'4
        }

        .. figure:: ../_images/Shuffler-xu7sln4vt7n.png

        To get the result of the last operation, use the property
        :attr:`current_window`.

        >>> notes = shuffler.current_window
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            e'4
            d'4
            f'4
        }

        .. figure:: ../_images/Shuffler-gphtpqn9jb.png

        Calling the object outputs the same result as using the method
        :meth:`shuffle`.

        >>> notes = shuffler.shuffle()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            e'4
            f'4
            c'4
            d'4
        }

        .. figure:: ../_images/Shuffler-g965k0d03if.png

    .. warning::

        Unlike the other classes in Auxjad, the very first call of an instance
        of this class will already process the initial container. To disable
        this behaviour and output the initial container once before shuffling
        or rotating it, initialise the class with the keyword argument
        :attr:`process_on_first_call` set to ``False``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            process_on_first_call=False,
        ...                            )
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/Shuffler-76039tn5b9k.png

    :func:`len()`:
        Applying the :func:`len()` function to the shuffler will return the
        number of logical ties of :attr:`contents`.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4 ~ | f'2 g'2")
        >>> shuffler = auxjad.Shuffler(container)
        >>> len(shuffler)
        5

         Do note that consecutive rests are considered as a single logical tie,
         so in the example below the :func:`len()` function returns ``5`` and
         not ``6``. When shuffling or rotating logical ties, consecutive rests
         are also shuffled and rotated together.

         >>> container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
         >>> shuffler = auxjad.Shuffler(container)
         >>> len(shuffler)
         5

    Arguments and properties:
        This class has many keyword arguments, all of which can be altered
        after instantiation using properties with the same names as shown
        below. Setting :attr:`pitch_only` to ``True`` will enable pitch mode;
        by default, this class shuffles and rotates logical ties, but in pitch
        mode only pitches are shuffled or rotated. By setting
        :attr:`preserve_rest_position` to ``True`` the shuffle and rotation
        operations will not change the position or duration of rests.
        :attr:`disable_rewrite_meter` disables the
        |abjad.mutate().rewrite_meter()| mutation which is applied to the
        container after every call, and :attr:`omit_time_signatures` will
        remove all time signatures from the output (both are ``False`` by
        default). The properties :attr:`boundary_depth`,
        :attr:`maximum_dot_count`, and :attr:`rewrite_tuplets` are passed as
        arguments to |abjad.mutate().rewrite_meter()|, see its documentation
        for more information. By default, calling the object will first return
        the original container and subsequent calls will process it; set
        :attr:`process_on_first_call` to ``True`` and the shuffling process
        will be applied on the very first call.

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4"
        ... )
        >>> shuffler = auxjad.Shuffler(container,
        ...                            pitch_only=False,
        ...                            preserve_rest_position=True,
        ...                            disable_rewrite_meter=False,
        ...                            omit_time_signatures=True,
        ...                            boundary_depth=0,
        ...                            maximum_dot_count=1,
        ...                            rewrite_tuplets=False,
        ...                            process_on_first_call=True,
        ...                            )
        >>> shuffler.pitch_only
        False
        >>> shuffler.preserve_rest_position
        True
        >>> shuffler.disable_rewrite_meter
        False
        >>> shuffler.omit_time_signatures
        True
        >>> shuffler.boundary_depth
        0
        >>> shuffler.maximum_dot_count
        1
        >>> shuffler.rewrite_tuplets
        False
        >>> shuffler.process_on_first_call
        True

        Use the properties below to change these values after initialisation.

        >>> shuffler.pitch_only = True
        >>> shuffler.preserve_rest_position = False
        >>> shuffler.disable_rewrite_meter = True
        >>> shuffler.omit_time_signatures = False
        >>> shuffler.boundary_depth = 1
        >>> shuffler.maximum_dot_count = 2
        >>> shuffler.rewrite_tuplets = True
        >>> shuffler.process_on_first_call = False
        >>> shuffler.pitch_only
        True
        >>> shuffler.preserve_rest_position
        True
        >>> shuffler.disable_rewrite_meter
        True
        >>> shuffler.omit_time_signatures
        False
        >>> shuffler.boundary_depth
        1
        >>> shuffler.maximum_dot_count
        2
        >>> shuffler.rewrite_tuplets
        True
        >>> shuffler.process_on_first_call
        False

    :attr:`pitch_only`:
        By default, the shuffling operation will shuffle logical ties:

        >>> container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            r4
            r16
            e'16
            f'8
            ~
            f'16
            d'8.
            ~
            d'16
            c'8.
        }

        .. figure:: ../_images/Shuffler-5j79m0wuxu.png

        Setting :attr:`pitch_only` to ``True`` enables pitch mode, so only
        pitches are shuffled (and not durations). Note how in the example below
        the duration of each leaf is the same as the input container.

        >>> container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
        >>> shuffler = auxjad.Shuffler(container, pitch_only=True)
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            f'8.
            r4
            d'8
            ~
            d'8.
            ~
            c'16
            e'8.
        }

        .. figure:: ../_images/Shuffler-f9jbzqkrkdf.png

    .. note::

        Altering the value of :attr:`pitch_only`: will replace the original
        :attr:`contents`: with the contents of :attr:`current_window`. Note how
        in the example below, the shuffled leaves in measure 3 comes from the
        previous measure and not from the initial :attr:`contents`:.

        >>> container = abjad.Container(r"c'4.. d'16 e'4. f'8")
        >>> shuffler = auxjad.Shuffler(container, pitch_only=True)
        >>> notes = shuffler.shuffle_n(2)
        >>> staff = abjad.Staff(notes)
        >>> shuffler.pitch_only = False
        >>> notes = shuffler.shuffle_n(2)
        >>> staff.append(notes)
        >>> auxjad.mutate(staff[:]).remove_repeated_time_signatures()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'4..
            c'16
            f'4.
            e'8
            d'4..
            f'16
            c'4.
            e'8
            f'16
            d'4..
            e'8
            c'4.
            c'4.
            d'8
            ~
            d'4
            ~
            d'16
            e'8
            f'16
        }

        .. figure:: ../_images/Shuffler-tyq8y6q8zr9.png

    :meth:`rotate`:
        Besides shuffling, logical ties and pitches can also be rotated using
        the :meth:`rotate` method. Similarly to shuffling, it can be applied to
        logical ties or pitches only depending on the property
        :attr:`pitch_only`.

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32"
        ... )
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler.rotate()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            d'4..
            e'16
            ~
            e'8.
            r16
            r8.
            f'16
            ~
            f'4
            ~
            f'8
            ~
            f'32
            g'32
            c'16
        }

        .. figure:: ../_images/Shuffler-7vamgsxlr6.png

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32"
        ... )
        >>> shuffler = auxjad.Shuffler(container, pitch_only=True)
        >>> notes = shuffler.rotate()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            d'16
            e'8.
            ~
            e'4
            r4
            f'4
            g'4
            ~
            g'8..
            c'32
        }

        .. figure:: ../_images/Shuffler-89cx79bjji8.png

        This method can also take the optional parameters ``n_rotations`` and
        ``anticlockwise``. The first is an :obj:`int` setting the number of
        rotations applied to the material, and the second is a :obj:`bool`
        setting the direction of the rotation (default ``False``).

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32"
        ... )
        >>> shuffler = auxjad.Shuffler(container, pitch_only=True)
        >>> notes = shuffler.rotate(n_rotations=2, anticlockwise=True)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            f'16
            g'8.
            ~
            g'4
            c'4
            d'4
            e'4
            ~
            e'8..
            r32
        }

        .. figure:: ../_images/Shuffler-g6v6wjm12ub.png

    :attr:`preserve_rest_position`:
        If :attr:`preserve_rest_position` is set to ``True``, the positions of
        all rests will remain the same after either shuffling and rotation. In
        pitch mode (when :attr:`pitch_only` is set to ``True``), this means
        that only the pitched notes will be shuffled or rotated, while the
        rests remain in the exact same place.

        >>> container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            pitch_only=True,
        ...                            preserve_rest_position=True,
        ...                            )
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'8.
            f'4
            r8
            r8.
            c'16
            e'8.
        }

        .. figure:: ../_images/Shuffler-pmou83f7rlj.png

        In logical ties mode, the rests will remain at the same index and will
        have the same total duration as before, but their position in the
        measure might vary since the duration of the pitched logical ties
        preceding it might change.

        >>> container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
        >>> shuffler = auxjad.Shuffler(container, preserve_rest_position=True)
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'4
            e'16
            r8.
            r8
            f'8
            ~
            f'16
            c'8.
        }

        .. figure:: ../_images/Shuffler-7hbp2kdpqof.png

    :attr:`disable_rewrite_meter`:
        If :attr:`disable_rewrite_meter` is set to ``True``, then the automatic
        behaviour of rewriting the leaves according to the meter is disabled.

        >>> container = abjad.Container(r"c'4 d'8 e'8 f'2")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            disable_rewrite_meter=True,
        ...                            )
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            e'8
            f'2
            c'4
            d'8
        }

        .. figure:: ../_images/Shuffler-tb78izpzvjp.png

    :meth:`shuffle_n` and :meth:`rotate_n`:
        To output several shuffled containers at once, use the methods
        :meth:`shuffle_n` and :meth:`rotate_n`, inputting the desired number of
        iterations. :meth:`rotate_n` can also take the optional arguments
        ``n_rotations`` and ``anticlockwise``, similarly to :meth:`rotate`.

        >>> container = abjad.Container(r"c'4 d'8 e'4. f'8. g'16")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler.shuffle_n(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'8
            g'16
            c'16
            ~
            c'8.
            f'16
            ~
            f'8
            e'4.
            g'16
            f'8.
            e'4
            ~
            e'8
            c'4
            d'8
        }

        .. figure:: ../_images/Shuffler-vtia65lbk5.png

        >>> container = abjad.Container(r"c'4 d'8 e'4. f'8. g'16")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler.rotate_n(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'8
            e'4.
            f'8.
            g'16
            c'4
            e'4.
            f'8
            ~
            f'16
            g'16
            c'4
            d'8
        }

        .. figure:: ../_images/Shuffler-3dqhy8eoiez.png

    :attr:`omit_time_signatures`:
        To disable time signatures altogether, initialise this class with the
        keyword argument :attr:`omit_time_signatures` set to ``True`` (default
        is ``False``), or change the :attr:`omit_time_signatures` property
        after initialisation.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            omit_time_signatures=True,
        ...                            )
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'4..
            e'16
            ~
            e'8.
            f'16
            ~
            f'4..
            r16
            r8.
            c'16
        }

        .. figure:: ../_images/Shuffler-1v3lwhj430b.png

    .. tip::

        All methods that return an |abjad.Selection| will add an initial time
        signature to it. The :meth:`shuffle_n` and :meth:`rotate_n` methods
        automatically remove repeated time signatures. When joining selections
        output by multiple method calls, use
        |auxjad.mutate().remove_repeated_time_signatures()| on the whole
        container after fusing the selections to remove any unecessary time
        signature changes.

    Time signature changes:
        This class handles time signature changes too:

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'8. d'4 r8 r8. \time 2/4 e'16 f'4.."
        ... )
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler.shuffle_n(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            e'16
            d'8.
            ~
            d'16
            f'4..
            \time 2/4
            c'8.
            r16
            r4
            \time 3/4
            c'8.
            f'16
            ~
            f'4.
            r8
            \time 2/4
            r8.
            d'16
            ~
            d'8.
            e'16
        }

        .. figure:: ../_images/Shuffler-yx11u6o14v.png

    Tuplet support:
        Tuplets are supported when :attr:`pitch_only` is ``True`` (pitch-only
        mode).

        >>> container = abjad.Container(
        ...     r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8"
        ... )
        >>> shuffler = auxjad.Shuffler(container, pitch_only=True)
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/4
            d'4
            \times 2/3 {
                f'4
                c'2
            }
            e'4.
            r8
        }

        .. figure:: ../_images/Shuffler-mjxubkel8y.png

    .. error::

        Tuplets are not supported when :attr:`pitch_only` is ``False`` (logical
        tie mode). Using a container with tuplets and :attr:`pitch_only` set to
        ``True`` will raise a :exc:`TypeError` exception.

        >>> container = abjad.Container(
        ...     r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8"
        ... )
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler()
        TypeError: 'contents' contain one ore more tuplets, which are not
        currently supported by the shuffle method

    Indicators:
        This class can also handle dynamics and articulations.

        >>> container = abjad.Container(
        ...     r"<c' e' g'>4--\p d'8-. e'8-. f'4-^\f r4"
        ... )
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler.shuffle_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            e'8
            \p
            - \staccato
            d'8
            - \staccato
            f'4
            \f
            - \marcato
            <c' e' g'>4
            \p
            - \tenuto
            r4
            r4
            d'8
            - \staccato
            f'8
            \f
            - \marcato
            ~
            f'8
            <c' e' g'>4
            \p
            - \tenuto
            e'8
            - \staccato
            f'4
            \f
            - \marcato
            e'8
            \p
            - \staccato
            <c' e' g'>8
            - \tenuto
            ~
            <c' e' g'>8
            d'8
            - \staccato
            r4
        }

        .. figure:: ../_images/Shuffler-2ibui58pj8w.png

    .. tip::

        The functions |auxjad.mutate().remove_repeated_dynamics()| and
        |auxjad.mutate().reposition_clefs()| can be used to clean the output
        and remove repeated dynamics and unnecessary clef changes.

    .. warning::

        Do note that some elements that span multiple notes (such as ottava
        indicators, manual beams, etc.) can become problematic when notes
        containing them are split into two. As a rule of thumb, it is always
        better to attach those to the music after the fading process has ended.
        In the case of shuffling logical ties, slurs and hairpins can also
        become a problem, since their start and end position can shift around.
        Dynamics are shuffled together with their leaves, so the initial leaf
        may lack a dynamic marking.

    :attr:`contents`:
        Use the property :attr:`contents` to get the input container upon which
        the shuffler operates. Notice that :attr:`contents` remains invariant
        after any shuffling or rotation operations (use :attr:`current_window`
        for the transformed selection of music). :attr:`contents` can be used
        to change the |abjad.Container| to be shuffled.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> abjad.f(shuffler.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/Shuffler-qsee7chymo.png

        >>> shuffler()
        >>> abjad.f(shuffler.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/Shuffler-ii3fxe001ki.png

        >>> shuffler.contents = abjad.Container(r"cs2 ds2")
        >>> abjad.f(shuffler.contents)
        {
            cs2
            ds2
        }

        .. figure:: ../_images/Shuffler-p2vd4mfvucp.png

    Tweaking |abjad.mutate().rewrite_meter()|:
        This function uses the default logical tie splitting algorithm from
        |abjad.mutate().rewrite_meter()|.

        >>> container = abjad.Container(r"c'4. d'8 e'2")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            e'2
            c'4.
            d'8
        }

        .. figure:: ../_images/Shuffler-t4lsqxg18ab.png

        Set :attr:`boundary_depth` to a different number to change its
        behaviour.

        >>> shuffler = auxjad.Shuffler(container,
        ...                            boundary_depth=1,
        ...                            )
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            e'2
            c'4
            ~
            c'8
            d'8
        }

        .. figure:: ../_images/Shuffler-7na5znnhhwe.png

        Other arguments available for tweaking the output of
        |abjad.mutate().rewrite_meter()| are :attr:`maximum_dot_count` and
        :attr:`rewrite_tuplets`, which work exactly as the identically named
        arguments of |abjad.mutate().rewrite_meter()|.

        This class also accepts the arguments ``fuse_across_groups_of_beats``,
        ``fuse_quadruple_meter``, ``fuse_triple_meter``, and
        ``extract_trivial_tuplets``, which are passed on to
        |auxjad.mutate().prettify_rewrite_meter()| (the latter can be disabled
        by setting ``prettify_rewrite_meter`` to ``False``). See the
        documentation of this function for more details on these arguments.

    :attr:`disable_rewrite_meter`:
        By default, this class uses the |abjad.mutate().rewrite_meter()|
        mutation.

        >>> container = abjad.Container(r"c'4 d'8 e'8 f'2")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            e'8
            f'8
            ~
            f'4.
            c'8
            ~
            c'8
            d'8
        }

        .. figure:: ../_images/Shuffler-7cfnxx7shci.png

        Set :attr:`disable_rewrite_meter` to ``True`` in order to disable this
        behaviour.

        >>> container = abjad.Container(r"c'4 d'8. e'16 f'2")
        >>> abjad.f(container)
        \new Staff
        {
            \time 4/4
            e'16
            f'8.
            ~
            f'4
            ~
            f'16
            c'8.
            ~
            c'16
            d'8.
        }

        .. figure:: ../_images/Shuffler-6gm4ev48j9k.png

        >>> shuffler = auxjad.Shuffler(container,
        ...                            disable_rewrite_meter=True,
        ...                            )
        >>> notes = shuffler()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            e'16
            f'2
            c'4
            d'8.
        }

        .. figure:: ../_images/Shuffler-xlr4x3bhj6n.png

    Using as iterator:
        The instances of this class can also be used as an iterator, which can
        then be used in a for loop. Note that unlike the methods
        :meth:`shuffle_n` and :meth:`rotate_n`, time signatures are added to
        each window returned by the shuffler. Use the function
        |auxjad.mutate().remove_repeated_time_signatures()| to clean the output
        when using this class in this way. It is also important to note that a
        ``break`` statement is needed when using this class as an iterator. The
        reason is that shuffling is a process that can happen indefinitely
        (unlike some of the other classes in this library).

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> staff = abjad.Staff()
        >>> for window in shuffler:
        ...     staff.append(window)
        ...     if abjad.inspect(staff).duration() == abjad.Duration((9, 4)):
        ...         break
        >>> auxjad.mutate(staff[:]).remove_repeated_time_signatures()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            e'4
            c'4
            d'4
            d'4
            c'4
            e'4
            c'4
            e'4
            d'4
        }

        .. figure:: ../_images/Shuffler-3gyz7atvemx.png
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_contents',
                 '_pitch_only',
                 '_preserve_rest_position',
                 '_disable_rewrite_meter',
                 '_omit_time_signatures',
                 '_current_window',
                 '_logical_selections',
                 '_logical_selections_indeces',
                 '_pitches',
                 '_time_signatures',
                 '_is_first_window',
                 '_boundary_depth',
                 '_maximum_dot_count',
                 '_rewrite_tuplets',
                 '_process_on_first_call',
                 '_prettify_rewrite_meter',
                 '_extract_trivial_tuplets',
                 '_fuse_across_groups_of_beats',
                 '_fuse_quadruple_meter',
                 '_fuse_triple_meter',
                 )

    ### INITIALISER ###

    def __init__(self,
                 contents: abjad.Container,
                 *,
                 pitch_only: bool = False,
                 preserve_rest_position: bool = False,
                 disable_rewrite_meter: bool = False,
                 omit_time_signatures: bool = False,
                 boundary_depth: Optional[int] = None,
                 maximum_dot_count: Optional[int] = None,
                 rewrite_tuplets: bool = True,
                 process_on_first_call: bool = True,
                 prettify_rewrite_meter: bool = True,
                 extract_trivial_tuplets: bool = True,
                 fuse_across_groups_of_beats: bool = True,
                 fuse_quadruple_meter: bool = True,
                 fuse_triple_meter: bool = True,
                 ):
        r'Initialises self.'
        self.contents = contents
        self.pitch_only = pitch_only
        self.preserve_rest_position = preserve_rest_position
        self.disable_rewrite_meter = disable_rewrite_meter
        self.omit_time_signatures = omit_time_signatures
        self.boundary_depth = boundary_depth
        self.maximum_dot_count = maximum_dot_count
        self.rewrite_tuplets = rewrite_tuplets
        self.prettify_rewrite_meter = prettify_rewrite_meter
        self.extract_trivial_tuplets = extract_trivial_tuplets
        self.fuse_across_groups_of_beats = fuse_across_groups_of_beats
        self.fuse_quadruple_meter = fuse_quadruple_meter
        self.fuse_triple_meter = fuse_triple_meter
        self.process_on_first_call = process_on_first_call
        self._is_first_window = True

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Returns interpreter representation of :attr:`contents`.'
        return format(self._contents)

    def __len__(self) -> int:
        r'Returns the number of logical ties of :attr:`contents`.'
        return len(self._logical_selections)

    def __call__(self) -> abjad.Selection:
        r'Calls the shuffling process, returning an |abjad.Selection|'
        return self.shuffle()

    def __next__(self) -> abjad.Selection:
        r"""Calls the shuffling process for one iteration, returning an
        |abjad.Selection|.
        """
        return self.__call__()

    def __iter__(self):
        r'Returns an iterator, allowing instances to be used as iterators.'
        return self

    ### PUBLIC METHODS ###

    def shuffle(self) -> abjad.Selection:
        r'Shuffles logical ties or pitches of :attr:`contents`.'
        if self._is_first_window and not self._process_on_first_call:
            if not self._pitch_only:
                self._rewrite_logical_selections()
                return self.current_window
            else:
                self._rewrite_pitches()
                return self.current_window
        else:
            if not self._pitch_only:
                return self._shuffle_logical_selections()
            else:
                return self._shuffle_pitches()

    def rotate(self,
               *,
               n_rotations: int = 1,
               anticlockwise: bool = False,
               ) -> abjad.Selection:
        r'Rotates logical ties or pitches of :attr:`contents`.'
        if not isinstance(n_rotations, int):
            raise TypeError("'n_rotations' must be 'int'")
        if n_rotations < 1:
            raise ValueError("'n_rotations' must be greater than zero")
        if not isinstance(anticlockwise, bool):
            raise TypeError("'anticlockwise' must be 'bool'")
        if self._is_first_window and not self._process_on_first_call:
            if not self._pitch_only:
                self._rewrite_logical_selections()
                return self.current_window
            else:
                self._rewrite_pitches()
                return self.current_window
        else:
            if not self._pitch_only:
                return self._rotate_logical_selections(
                    n_rotations=n_rotations,
                    anticlockwise=anticlockwise,
                )
            else:
                return self._rotate_pitches(
                    n_rotations=n_rotations,
                    anticlockwise=anticlockwise,
                )

    def shuffle_n(self,
                  n: int,
                  ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the shuffling process and outputs
        a single |abjad.Selection|.
        """
        if not isinstance(n, int):
            raise TypeError("argument must be 'int'")
        if n < 1:
            raise ValueError("argument must be greater than zero")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.__call__())
        mutate(dummy_container[:]).remove_repeated_time_signatures()
        mutate(dummy_container[:]).remove_repeated_dynamics()
        output = dummy_container[:]
        dummy_container[:] = []
        return output

    def rotate_n(self,
                 n: int,
                 *,
                 n_rotations: int = 1,
                 anticlockwise: bool = False,
                 ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the pitch shuffling process and
        outputs a single |abjad.Selection|.
        """
        if not isinstance(n, int):
            raise TypeError("argument must be 'int'")
        if n < 1:
            raise ValueError("argument must be greater than zero")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.rotate(n_rotations=n_rotations,
                                               anticlockwise=anticlockwise))
        mutate(dummy_container[:]).remove_repeated_time_signatures()
        mutate(dummy_container[:]).remove_repeated_dynamics()
        output = dummy_container[:]
        dummy_container[:] = []
        return output

    ### PRIVATE METHODS ###

    def _update_logical_selections(self):
        r'Updates the selection of logical ties of :attr:`contents`.'
        self._logical_selections = self._get_logical_selections(
            self._contents
        )
        self._logical_selections_indeces = list(range(self.__len__()))

    def _get_pitch_list(self) -> list:
        r'Creates a :obj:`list` of all pitches in :attr:`contents`.'
        self._pitches = []
        for logical_selection in self._logical_selections:
            leaf = logical_selection.leaves()[0]
            if isinstance(leaf, abjad.Rest):
                self._pitches.append(None)
            elif isinstance(leaf, abjad.Note):
                self._pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                self._pitches.append(leaf.written_pitches)

    def _shuffle_list_preserving_rests(self,
                                       input_list: list,
                                       ) -> list:
        r'Shuffles a :obj:`list` while keeping rest indeces unchanged.'
        dummy_list = [input_list[i] for i in range(len(input_list))
                      if self._pitches[i] is not None]
        random.shuffle(dummy_list)
        self._replace_list_preserving_rests(dummy_list, input_list)

    def _rotate_list_preserving_rests(self,
                                      input_list: list,
                                      *,
                                      n_rotations: int = 1,
                                      anticlockwise: bool = False,
                                      ) -> list:
        r'Rotates a :obj:`list` while keeping rest indeces unchanged.'
        dummy_list = [input_list[i] for i in range(len(input_list))
                      if self._pitches[i] is not None]
        self._rotate_list(dummy_list,
                          n_rotations=n_rotations,
                          anticlockwise=anticlockwise,
                          )
        self._replace_list_preserving_rests(dummy_list, input_list)

    def _replace_list_preserving_rests(self,
                                       input_list: list,
                                       destination_list: list,
                                       ) -> list:
        r'Substitutes back an altered :obj:`list` while preserving rests.'
        counter = 0
        for index, pitch in enumerate(self._pitches):
            if pitch is not None:
                destination_list[index] = input_list[counter]
                counter += 1

    def _shuffle_logical_selections(self) -> abjad.Selection:
        r'Shuffles the logical ties of :attr:`contents`.'
        if len(abjad.select(self._contents).tuplets()) > 0:
            raise ValueError("'contents' contain one ore more tuplets; "
                             "tuplets are currently supported only in "
                             "pitch-only mode")
        if not self._preserve_rest_position:
            random.shuffle(self._logical_selections_indeces)
        else:
            self._shuffle_list_preserving_rests(
                self._logical_selections_indeces
            )
        self._rewrite_logical_selections()
        return self.current_window

    def _shuffle_pitches(self) -> abjad.Selection:
        r'Shuffles only the pitches of :attr:`contents`.'
        if not self._preserve_rest_position:
            random.shuffle(self._pitches)
        else:
            self._shuffle_list_preserving_rests(self._pitches)
        self._rewrite_pitches()
        return self.current_window

    def _rotate_logical_selections(self,
                                   *,
                                   n_rotations: int = 1,
                                   anticlockwise: bool = False,
                                   ) -> abjad.Selection:
        r'Rotates the logical ties of :attr:`contents`.'
        if len(abjad.select(self._contents).tuplets()) > 0:
            raise ValueError("'contents' contain one ore more tuplets; "
                             "tuplets are currently supported only in "
                             "pitch-only mode")
        if not self._preserve_rest_position:
            self._rotate_list(self._logical_selections_indeces,
                              n_rotations=n_rotations,
                              anticlockwise=anticlockwise,
                              )
        else:
            self._rotate_list_preserving_rests(
                self._logical_selections_indeces,
                n_rotations=n_rotations,
                anticlockwise=anticlockwise,
            )
        self._rewrite_logical_selections()
        return self.current_window

    def _rotate_pitches(self,
                        *,
                        n_rotations: int = 1,
                        anticlockwise: bool = False,
                        ) -> abjad.Selection:
        r'Rotates the pitches of :attr:`contents`.'
        if not self._preserve_rest_position:
            self._rotate_list(self._pitches,
                              n_rotations=n_rotations,
                              anticlockwise=anticlockwise,
                              )
        else:
            self._rotate_list_preserving_rests(self._pitches,
                                               n_rotations=n_rotations,
                                               anticlockwise=anticlockwise,
                                               )
        self._rewrite_pitches()
        return self.current_window

    def _rewrite_logical_selections(self):
        r'Rewrites the logical selections of the current window.'
        # writing dummy_container in shuffled order
        dummy_container = abjad.Container()
        logical_selections = self._get_logical_selections(
            abjad.mutate(self._contents).copy()
        )
        self._force_dynamics(logical_selections)
        for index in self._logical_selections_indeces:
            logical_selection = logical_selections[index]
            dummy_container.append(logical_selection.leaves())
        # splitting leaves at measure line points
        abjad.mutate(dummy_container[:]).split(
            [ts.duration for ts in self._time_signatures],
            cyclic=True,
        )
        # attaching time signature structure
        mutate(dummy_container).enforce_time_signature(
            self._time_signatures,
            disable_rewrite_meter=True,
        )
        # handling dynamics and slurs
        mutate(dummy_container[:]).reposition_dynamics()
        mutate(dummy_container[:]).reposition_slurs()
        # rewrite meter
        if not self._disable_rewrite_meter:
            mutate(dummy_container).auto_rewrite_meter(
                meter_list=self._time_signatures,
                boundary_depth=self._boundary_depth,
                maximum_dot_count=self._maximum_dot_count,
                rewrite_tuplets=self._rewrite_tuplets,
                prettify_rewrite_meter=self._prettify_rewrite_meter,
                extract_trivial_tuplets=self._extract_trivial_tuplets,
                fuse_across_groups_of_beats=self._fuse_across_groups_of_beats,
                fuse_quadruple_meter=self._fuse_quadruple_meter,
                fuse_triple_meter=self._fuse_triple_meter,
            )
        # output
        self._is_first_window = False
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    def _rewrite_pitches(self):
        r'Rewrites the pitches of the current window.'
        dummy_container = abjad.Container(
            abjad.mutate(self._contents[:]).copy()
        )
        leaf_counter = 0
        for pitch, logical_selection in zip(self._pitches,
                                            self._logical_selections):
            logical_tie = logical_selection.leaves()
            for leaf in logical_tie:
                if pitch is None:
                    new_leaf = abjad.Rest(leaf.written_duration)
                elif isinstance(pitch, abjad.PitchSegment):
                    new_leaf = abjad.Chord(pitch, leaf.written_duration)
                    if (isinstance(leaf, abjad.Rest) and len(logical_tie) > 1
                            and leaf is not logical_tie[-1]):
                        abjad.attach(abjad.Tie(), new_leaf)
                else:
                    new_leaf = abjad.Note(pitch, leaf.written_duration)
                    if (isinstance(leaf, abjad.Rest) and len(logical_tie) > 1
                            and leaf is not logical_tie[-1]):
                        abjad.attach(abjad.Tie(), new_leaf)
                for indicator in abjad.inspect(leaf).indicators():
                    if (isinstance(indicator, (abjad.Tie, abjad.Articulation))
                            and pitch is None):
                        continue
                    if isinstance(indicator, abjad.TimeSignature):
                        abjad.attach(indicator, new_leaf)
                    else:
                        abjad.attach(indicator, new_leaf)
                selection = abjad.select(dummy_container).leaf(leaf_counter)
                abjad.mutate(selection).replace(new_leaf)
                leaf_counter += 1
        # attaching time signature structure
        mutate(dummy_container[:]).extract_trivial_tuplets()
        mutate(dummy_container).enforce_time_signature(
            self._time_signatures,
            disable_rewrite_meter=True,
        )
        # output
        self._is_first_window = False
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    @staticmethod
    def _get_logical_selections(container):
        r'Updates the selection of logical ties of a container.'
        def group_logical_ties(logical_tie):
            if isinstance(logical_tie.head, abjad.Rest):
                return True
            else:
                return logical_tie.head
        logical_ties = abjad.select(container).logical_ties()
        return logical_ties.group_by(group_logical_ties)

    @staticmethod
    def _remove_all_time_signatures(container):
        r'Removes all time signatures of an |abjad.Container|.'
        for leaf in abjad.select(container).leaves():
            if abjad.inspect(leaf).effective(abjad.TimeSignature):
                abjad.detach(abjad.TimeSignature, leaf)

    @staticmethod
    def _force_dynamics(container):
        logical_ties = abjad.select(container).logical_ties()
        for logical_tie in logical_ties[1:]:
            if abjad.inspect(logical_tie[0]).indicator(abjad.Dynamic) is None:
                index = logical_ties.index(logical_tie)
                previous_logical_tie = logical_ties[index - 1]
                inspector = abjad.inspect(previous_logical_tie[0])
                if inspector.indicator(abjad.Dynamic) is not None:
                    abjad.attach(inspector.indicator(abjad.Dynamic),
                                 logical_tie[0],
                                 )

    @staticmethod
    def _rotate_list(input_list: list,
                     *,
                     n_rotations: int = 1,
                     anticlockwise: bool = False,
                     ) -> list:
        r'Rotates a :obj:`list`.'
        for _ in range(n_rotations):
            if not anticlockwise:
                element = input_list.pop(0)
                input_list.append(element)
            else:
                element = input_list.pop(-1)
                input_list.insert(0, element)

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> abjad.Container:
        r'The |abjad.Container| to be shuffled.'
        return abjad.mutate(self._contents).copy()

    @contents.setter
    def contents(self,
                 contents: abjad.Container,
                 ):
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or child "
                            "class")
        if not abjad.select(contents).leaves().are_contiguous_logical_voice():
            raise ValueError("'contents' must be contiguous logical voice")
        if isinstance(contents, abjad.Score):
            self._contents = abjad.mutate(contents[0]).copy()
        elif isinstance(contents, abjad.Tuplet):
            self._contents = abjad.Container([abjad.mutate(contents).copy()])
        else:
            self._contents = abjad.mutate(contents).copy()
        dummy_container = abjad.mutate(contents).copy()
        self._current_window = dummy_container[:]
        dummy_container[:] = []
        self._update_logical_selections()
        self._get_pitch_list()
        inspector = inspect(self._contents)
        self._time_signatures = inspector.time_signature_extractor(
            do_not_use_none=True,
        )
        self._is_first_window = True

    @property
    def pitch_only(self) -> bool:
        r"""When ``True``, only the pitches will be shuffled or rotated while
        the durations remain the same.
        """
        return self._pitch_only

    @pitch_only.setter
    def pitch_only(self,
                   pitch_only: bool,
                   ):
        if not isinstance(pitch_only, bool):
            raise TypeError("'pitch_only' must be 'bool'")
        self._pitch_only = pitch_only
        # potentially new logical selections when shifting from pitch-only mode
        # to logical selections mode
        self._update_logical_selections()
        self._get_pitch_list()
        self._contents = abjad.Container(
            abjad.mutate(self._current_window).copy()
        )

    @property
    def preserve_rest_position(self) -> bool:
        r"""When ``True``, shuffle operations will preserve rest positions and
        durations.
        """
        return self._preserve_rest_position

    @preserve_rest_position.setter
    def preserve_rest_position(self,
                               preserve_rest_position: bool,
                               ):
        if not isinstance(preserve_rest_position, bool):
            raise TypeError("'preserve_rest_position' must be 'bool'")
        self._preserve_rest_position = preserve_rest_position

    @property
    def disable_rewrite_meter(self) -> bool:
        r"""When ``True``, the durations of the notes in the output will not be
        rewritten by the |abjad.mutate().rewrite_meter()| mutation.
        """
        return self._disable_rewrite_meter

    @disable_rewrite_meter.setter
    def disable_rewrite_meter(self,
                              disable_rewrite_meter: bool,
                              ):
        if not isinstance(disable_rewrite_meter, bool):
            raise TypeError("'disable_rewrite_meter' must be 'bool'")
        self._disable_rewrite_meter = disable_rewrite_meter

    @property
    def omit_time_signatures(self) -> bool:
        r'When ``True``, the output will contain no time signatures.'
        return self._omit_time_signatures

    @omit_time_signatures.setter
    def omit_time_signatures(self,
                             omit_time_signatures: bool,
                             ):
        if not isinstance(omit_time_signatures, bool):
            raise TypeError("'omit_time_signatures' must be 'bool'")
        self._omit_time_signatures = omit_time_signatures

    @property
    def boundary_depth(self) -> Union[int, None]:
        r"""Sets the argument ``boundary_depth`` of
        |abjad.mutate().rewrite_meter()|.
        """
        return self._boundary_depth

    @boundary_depth.setter
    def boundary_depth(self,
                       boundary_depth: Optional[int],
                       ):
        if boundary_depth is not None:
            if not isinstance(boundary_depth, int):
                raise TypeError("'boundary_depth' must be 'int'")
        self._boundary_depth = boundary_depth

    @property
    def maximum_dot_count(self) -> Union[int, None]:
        r"""Sets the argument ``maximum_dot_count`` of
        |abjad.mutate().rewrite_meter()|.
        """
        return self._maximum_dot_count

    @maximum_dot_count.setter
    def maximum_dot_count(self,
                          maximum_dot_count: Optional[int],
                          ):
        if maximum_dot_count is not None:
            if not isinstance(maximum_dot_count, int):
                raise TypeError("'maximum_dot_count' must be 'int'")
        self._maximum_dot_count = maximum_dot_count

    @property
    def rewrite_tuplets(self) -> bool:
        r"""Sets the argument ``rewrite_tuplets`` of
        |abjad.mutate().rewrite_meter()|.
        """
        return self._rewrite_tuplets

    @rewrite_tuplets.setter
    def rewrite_tuplets(self,
                        rewrite_tuplets: bool,
                        ):
        if not isinstance(rewrite_tuplets, bool):
            raise TypeError("'rewrite_tuplets' must be 'bool'")
        self._rewrite_tuplets = rewrite_tuplets

    @property
    def prettify_rewrite_meter(self) -> bool:
        r"""Used to enable or disable the mutation
        |auxjad.mutate().prettify_rewrite_meter()| (default ``True``).
        """
        return self._prettify_rewrite_meter

    @prettify_rewrite_meter.setter
    def prettify_rewrite_meter(self,
                               prettify_rewrite_meter: bool,
                               ):
        if not isinstance(prettify_rewrite_meter, bool):
            raise TypeError("'prettify_rewrite_meter' must be 'bool'")
        self._prettify_rewrite_meter = prettify_rewrite_meter

    @property
    def extract_trivial_tuplets(self) -> bool:
        r"""Sets the argument ``extract_trivial_tuplets`` of
        |auxjad.mutate().prettify_rewrite_meter()|.
        """
        return self._extract_trivial_tuplets

    @extract_trivial_tuplets.setter
    def extract_trivial_tuplets(self,
                                extract_trivial_tuplets: bool,
                                ):
        if not isinstance(extract_trivial_tuplets, bool):
            raise TypeError("'extract_trivial_tuplets' must be 'bool'")
        self._extract_trivial_tuplets = extract_trivial_tuplets

    @property
    def fuse_across_groups_of_beats(self) -> bool:
        r"""Sets the argument ``fuse_across_groups_of_beats`` of
        |auxjad.mutate().prettify_rewrite_meter()|.
        """
        return self._fuse_across_groups_of_beats

    @fuse_across_groups_of_beats.setter
    def fuse_across_groups_of_beats(self,
                                    fuse_across_groups_of_beats: bool,
                                    ):
        if not isinstance(fuse_across_groups_of_beats, bool):
            raise TypeError("'fuse_across_groups_of_beats' must be 'bool'")
        self._fuse_across_groups_of_beats = fuse_across_groups_of_beats

    @property
    def fuse_quadruple_meter(self) -> bool:
        r"""Sets the argument ``fuse_quadruple_meter`` of
        |auxjad.mutate().prettify_rewrite_meter()|.
        """
        return self._fuse_quadruple_meter

    @fuse_quadruple_meter.setter
    def fuse_quadruple_meter(self,
                             fuse_quadruple_meter: bool,
                             ):
        if not isinstance(fuse_quadruple_meter, bool):
            raise TypeError("'fuse_quadruple_meter' must be 'bool'")
        self._fuse_quadruple_meter = fuse_quadruple_meter

    @property
    def fuse_triple_meter(self) -> bool:
        r"""Sets the argument ``fuse_triple_meter`` of
        |auxjad.mutate().prettify_rewrite_meter()|.
        """
        return self._fuse_triple_meter

    @fuse_triple_meter.setter
    def fuse_triple_meter(self,
                          fuse_triple_meter: bool,
                          ):
        if not isinstance(fuse_triple_meter, bool):
            raise TypeError("'fuse_triple_meter' must be 'bool'")
        self._fuse_triple_meter = fuse_triple_meter

    @property
    def process_on_first_call(self) -> bool:
        r"""If ``True`` then :attr:`contents` will be processed in the very
        first call.
        """
        return self._process_on_first_call

    @process_on_first_call.setter
    def process_on_first_call(self,
                              process_on_first_call: bool,
                              ):
        if not isinstance(process_on_first_call, bool):
            raise TypeError("'process_on_first_call' must be 'bool'")
        self._process_on_first_call = process_on_first_call

    @property
    def current_window(self) -> abjad.Selection:
        r'Read-only property, returns the result of the last operation.'
        current_window = abjad.mutate(self._current_window).copy()
        if self._omit_time_signatures:
            self._remove_all_time_signatures(current_window)
        return current_window
