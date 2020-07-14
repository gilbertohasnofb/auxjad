import copy
import random
from typing import Optional, Union

import abjad

from ..utilities.enforce_time_signature import enforce_time_signature
from ..utilities.remove_repeated_time_signatures import (
    remove_repeated_time_signatures,
)
from ..utilities.time_signature_extractor import time_signature_extractor


class Shuffler:
    r"""``Shuffler`` takes an input ``abjad.Container`` and shuffles or rotates
    its logical ties or pitches. When shuffling or rotating pitches only,
    tuplets are supported, otherwise tuplets are not supported.

    Example:
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

        .. figure:: ../_images/image-Shuffler-1.png

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

        .. figure:: ../_images/image-Shuffler-2.png

        To get the result of the last operation, use the property
        ``current_window``.

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

        .. figure:: ../_images/image-Shuffler-3.png

        Calling the object outputs the same result as using the method
        ``shuffle()``.

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

        .. figure:: ../_images/image-Shuffler-4.png

    ..  warning::

        Unlike the other classes in auxjad, the very first call of ``Shuffler``
        will already process the initial container. To disable this behaviour
        and output the initial container once before shuffling or rotating it,
        initialise the class with the keyword argument
        ``processs_on_first_call`` set to ``False``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            processs_on_first_call=False,
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

        .. figure:: ../_images/image-Shuffler-5.png

    Example:
        Applying the ``len()`` function to the shuffler will return the number
        of logical ties of ``contents``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4 ~ | f'2 g'2")
        >>> shuffler = auxjad.Shuffler(container)
        >>> len(shuffler)
        5

         Do note that consecutive rests are considered as a single logical tie,
         so in the example below the ``len()`` function returns ``5`` and not
         ``6``. When shuffling or rotating logical ties, consecutive rests are
         also shuffled and rotated together.

         >>> container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
         >>> shuffler = auxjad.Shuffler(container)
         >>> len(shuffler)
         5

    Example:
        This class has many keyword arguments, all of which can be altered
        after instantiation using properties with the same names as shown
        below. Setting ``pitch_only`` to ``True`` will enable pitch mode; by
        default, this class shuffles and rotates logical ties, but in pitch
        mode only pitches are shuffled or rotated. By setting
        ``preserve_rest_position`` to ``True`` the shuffle and rotation
        operations will not change the position or duration of rests.
        ``disable_rewrite_meter`` disables the ``rewrite_meter()`` mutation
        which is applied to the container after every call, and
        ``omit_time_signatures`` will remove all time signatures from the
        output (both are ``False`` by default). By default, the first time
        signature is attached only to the first leaf of the first call (unless
        time signature changes require it). The properties ``boundary_depth``,
        ``maximum_dot_count``, and ``rewrite_tuplets`` are passed as arguments
        to abjad's ``rewrite_meter()``, see its documentation for more
        information. By default, calling the object will first return the
        original container and subsequent calls will process it; set
        ``processs_on_first_call`` to ``True`` and the looping process will be
        applied on the very first call.

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            pitch_only=False,
        ...                            preserve_rest_position=True,
        ...                            disable_rewrite_meter=False,
        ...                            omit_time_signatures=True,
        ...                            boundary_depth=0,
        ...                            maximum_dot_count=1,
        ...                            rewrite_tuplets=False,
        ...                            processs_on_first_call=True,
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
        >>> shuffler.processs_on_first_call
        True

        Use the properties below to change these values after initialisation.

        >>> shuffler.pitch_only = True
        >>> shuffler.preserve_rest_position = False
        >>> shuffler.disable_rewrite_meter = True
        >>> shuffler.omit_time_signatures = False
        >>> shuffler.boundary_depth = 1
        >>> shuffler.maximum_dot_count = 2
        >>> shuffler.rewrite_tuplets = True
        >>> shuffler.processs_on_first_call = False
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
        >>> shuffler.processs_on_first_call
        False

    Example:
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

        .. figure:: ../_images/image-Shuffler-6.png

        Setting ``pitch_only`` to ``True`` enables pitch mode, so only pitches
        are shuffled (and not durations). Note how in the example below the
        duration of each leaf is the same as the input container.

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

        .. figure:: ../_images/image-Shuffler-7.png

    Example:
        Besides shuffling, logical ties and pitches can also be rotated using
        the ``rotate()`` method. Similarly to shuffling, it can be applied to
        logical ties or pitches only depending on the property ``pitch_only``.

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32")
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

        .. figure:: ../_images/image-Shuffler-8.png

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32")
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

        .. figure:: ../_images/image-Shuffler-9.png

        This method can also take the optional parameters ``n_rotations`` and
        ``anticlockwise``. The first is an integer setting the number of
        rotations applied to the material, and the second is a boolean setting
        the direction of the rotation (default ``False``).

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32")
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

        .. figure:: ../_images/image-Shuffler-10.png

    Example:
        If ``preserve_rest_position`` is set to ``True``, the positions of all
        rests will remain the same after either shuffling and rotation. In
        pitch mode (when ``pitch_only`` is set to ``True``), this means that
        only the pitched notes will be shuffled or rotated, while the rests
        remain in the exact same place.

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

        .. figure:: ../_images/image-Shuffler-11.png

        In logical ties mode, the rests will remain at the same index and will
        have the same total duration as before, but their position in the bar
        might vary since the duration of the pitched logical ties preceeding
        it might change.

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

        .. figure:: ../_images/image-Shuffler-12.png

    Example:
        If ``disable_rewrite_meter`` is set to ``True``, then the automatic
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

        .. figure:: ../_images/image-Shuffler-13.png

    Example:
        To output several shuffled containers at once, use the methods
        ``shuffle_n`` and ``rotate_n``, inputting the desired number of
        iterations. ``rotate_n`` can also take the optional arguments
        ``n_rotations`` and ``anticlockwise``, similarly to ``rotate()``.

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
            e'4.
            c'8
            ~
            c'8
            d'8
        }

        .. figure:: ../_images/image-Shuffler-14.png

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
            c'8
            ~
            c'8
            d'8
        }

        .. figure:: ../_images/image-Shuffler-15.png

    Example:
        To disable time signatures altogether, initialise this class with the
        keyword argument ``omit_time_signatures`` set to ``True`` (default is
        ``False``), or change the ``omit_time_signatures`` property after
        initialisation.

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

        .. figure:: ../_images/image-Shuffler-16.png

    ..  tip::

        All methods that return an ``abjad.Selection`` will add an initial time
        signature to it. The ``shuffle_n()`` and ``rotate_n()`` methods
        automatically remove repeated time signatures. When joining selections
        output by multiple method calls, use
        ``auxjad.remove_repeated_time_signatures()`` on the whole container
        after fusing the selections to remove any unecessary time signature
        changes.

    Example:
        This class handles time signature changes too:

        >>> container = abjad.Container(
        ...     r"\time 3/4 c'8. d'4 r8 r8. \time 2/4 e'16 f'4..")
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

        .. figure:: ../_images/image-Shuffler-17.png

    Example:
        Tuplets are supported when ``pitch_only`` is ``True`` (pitch-only
        mode).

        >>> container = abjad.Container(
        ...     r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8")
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

        .. figure:: ../_images/image-Shuffler-18.png

    ..  error::

        Tuplets are not supported when ``pitch_only`` is ``False`` (logical tie
        mode).

        >>> container = abjad.Container(
        ...     r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler()
        TypeError: 'contents' contain one ore more tuplets, which are not
        currently supported by the shuffle method

    Example:
        This class can also handle dynamics and articulations.

        >>> container = abjad.Container(
        ...     r"<c' e' g'>4--\p d'8-. e'8-. f'4-^\f r4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> notes = shuffler.shuffle_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            r4
            f'4
            \f
            - \marcato
            d'8
            - \staccato
            <c' e' g'>8
            \p
            - \tenuto
            ~
            <c' e' g'>8
            e'8
            - \staccato
            f'4
            \f
            - \marcato
            d'8
            - \staccato
            <c' e' g'>8
            \p
            - \tenuto
            ~
            <c' e' g'>8
            r8
            r8
            e'8
            - \staccato
            f'4
            \f
            - \marcato
            r4
            e'8
            - \staccato
            d'8
            - \staccato
            <c' e' g'>4
            \p
            - \tenuto
        }

        .. figure:: ../_images/image-Shuffler-19.png

    .. tip::

        The functions ``auxjad.remove_repeated_dynamics()`` and
        ``auxjad.reposition_clefs()`` can be used to clean the output and
        remove repeated dynamics and unnecessary clef changes.

    ..  warning::

        Do note that elements that span multiple notes (such as hairpins,
        ottava indicators, manual beams, etc.) can become problematic when
        notes containing them are split into two. As a rule of thumb, it is
        always better to attach those to the music after the shuffling process
        has ended.

    Example:
        Use the property ``contents`` to get the input container upon which the
        shuffler operates. Notice that ``contents`` remains invariant after
        any shuffling or rotation operations (use ``current_window`` for the
        transformed selection of music). ``contents`` can be used to change the
        ``abjad.Container`` to be shuffled.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> abjad.f(shuffler.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Shuffler-20.png

        >>> shuffler()
        >>> abjad.f(shuffler.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Shuffler-21.png

        >>> shuffler.contents = abjad.Container(r"cs2 ds2")
        >>> abjad.f(shuffler.contents)
        {
            cs2
            ds2
        }

        .. figure:: ../_images/image-Shuffler-22.png

    Example:
        This function uses the default logical tie splitting algorithm from
        abjad's ``rewrite_meter()``.

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

        .. figure:: ../_images/image-Shuffler-23.png

        Set ``boundary_depth`` to a different number to change its behaviour.

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

        .. figure:: ../_images/image-Shuffler-24.png

        Other arguments available for tweaking the output of abjad's
        ``rewrite_meter()`` are ``maximum_dot_count`` and ``rewrite_tuplets``,
        which work exactly as the identically named arguments of
        ``rewrite_meter()``.

    Example:
        By default, this class rewrites uses abjad's ``rewrite_meter()``
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

        .. figure:: ../_images/image-Shuffler-25.png

        Set ``disable_rewrite_meter`` to ``True`` in order to disable this
        behaviour.

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

        .. figure:: ../_images/image-Shuffler-26.png

    Example:
        The instances of ``Shuffler`` can also be used as an iterator, which
        can then be used in a for loop. Note that unlike the methods
        ``shuffle_n()`` and ``rotate_n()``, time signatures are added to each
        window returned by the shuffler. Use the function
        ``auxjad.remove_repeated_time_signatures()`` to clean the output when
        using ``Shuffler`` in this way. It is also important to note that a
        ``break`` statement is needed when using ``Shuffler`` as an iterator.
        The reason is that shuffling is a process that can happen indefinitely
        (unlike some of the other classes in this library).

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> staff = abjad.Staff()
        >>> for window in shuffler:
        ...     staff.append(window)
        ...     if abjad.inspect(staff).duration() == abjad.Duration((9, 4)):
        ...         break
        >>> auxjad.remove_repeated_time_signatures(staff)
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

        .. figure:: ../_images/image-Shuffler-27.png
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
                 '_processs_on_first_call',
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
                 processs_on_first_call: bool = True,
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
        self.processs_on_first_call = processs_on_first_call
        self._is_first_window = True

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Returns interpret representation of ``contents``.'
        return format(self._contents)

    def __len__(self) -> int:
        r'Returns the number of logical ties of ``contents``.'
        return len(self._logical_selections)

    def __call__(self) -> abjad.Selection:
        r'Calls the shuffling process, returning an ``abjad.Selection``'
        return self.shuffle()

    def __next__(self) -> abjad.Selection:
        r"""Calls the shuffling process for one iteration, returning an
        ``abjad.Selection``.
        """
        return self.__call__()

    def __iter__(self):
        r'Returns an iterator, allowing instances to be used as iterators.'
        return self

    ### PUBLIC METHODS ###

    def shuffle(self) -> abjad.Selection:
        r'Shuffles logical ties or pitches of ``contents``.'
        if self._is_first_window and not self._processs_on_first_call:
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
        r'Rotates logical ties or pitches of ``contents``.'
        if not isinstance(n_rotations, int):
            raise TypeError("'n_rotations' must be 'int'")
        if n_rotations < 1:
            raise ValueError("'n_rotations' must be greater than zero")
        if not isinstance(anticlockwise, bool):
            raise TypeError("'anticlockwise' must be 'bool'")
        if self._is_first_window and not self._processs_on_first_call:
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
        a single ``abjad.Selection``.
        """
        if not isinstance(n, int):
            raise TypeError("argument must be 'int'")
        if n < 1:
            raise ValueError("argument must be greater than zero")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.__call__())
        remove_repeated_time_signatures(dummy_container)
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
        outputs a single ``abjad.Selection``.
        """
        if not isinstance(n, int):
            raise TypeError("argument must be 'int'")
        if n < 1:
            raise ValueError("argument must be greater than zero")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.rotate(n_rotations=n_rotations,
                                               anticlockwise=anticlockwise))
        remove_repeated_time_signatures(dummy_container)
        output = dummy_container[:]
        dummy_container[:] = []
        return output

    ### PRIVATE METHODS ###

    def _get_logical_selections(self):
        r'Updates the selection of logical ties of ``contents``.'
        def group_logical_ties(logical_tie):
            if isinstance(logical_tie.head, abjad.Rest):
                return True
            else:
                return logical_tie.head
        logical_ties = abjad.select(self._contents).logical_ties()
        self._logical_selections = logical_ties.group_by(group_logical_ties)
        self._logical_selections_indeces = list(range(self.__len__()))

    def _get_pitch_list(self) -> list:
        r'Creates a list of all pitches in ``contents``.'
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
                                       input_list: list
                                       ) -> list:
        r'Shuffles a list while keeping rest indeces unchanged.'
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
        r'Rotates a list while keeping rest indeces unchanged.'
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
        r'Substitutes back an altered list while preserving rests.'
        index = 0
        for i, pitch in enumerate(self._pitches):
            if pitch is not None:
                destination_list[i] = input_list[index]
                index += 1

    def _shuffle_logical_selections(self) -> abjad.Selection:
        r'Shuffles the logical ties of ``contents``.'
        if len(abjad.select(self._contents).tuplets()) > 0:
            raise ValueError("'contents' contain one ore more tuplets; "
                             "tuplets are currently supported only in "
                             "pitch-only mode")
        if not self._preserve_rest_position:
            random.shuffle(self._logical_selections_indeces)
        else:
            self._shuffle_list_preserving_rests(
                self._logical_selections_indeces)
        self._rewrite_logical_selections()
        return self.current_window

    def _shuffle_pitches(self) -> abjad.Selection:
        r'Shuffles only the pitches of ``contents``.'
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
        r'Rotates the logical ties of ``contents``.'
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
        r'Rotates the pitches of ``contents``.'
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
        for index in self._logical_selections_indeces:
            logical_selection = copy.deepcopy(
                self._logical_selections[index])
            dummy_container.append(logical_selection.leaves())
        # splitting leaves at bar line points
        abjad.mutate(dummy_container[:]).split(
            [ts.duration for ts in self._time_signatures],
            cyclic=True,
        )
        # attaching time signature structure
        enforce_time_signature(dummy_container,
                               self._time_signatures,
                               disable_rewrite_meter=True,
                               )
        # rewrite meter
        if not self._disable_rewrite_meter:
            measures = abjad.select(dummy_container[:]).group_by_measure()
            for measure, time_signature in zip(measures,
                                               self._time_signatures):
                abjad.mutate(measure).rewrite_meter(
                    time_signature,
                    boundary_depth=self._boundary_depth,
                    maximum_dot_count=self._maximum_dot_count,
                    rewrite_tuplets=self._rewrite_tuplets,
                )
        # output
        self._is_first_window = False
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    def _rewrite_pitches(self):
        r'Rewrites the pitches of the current window.'
        index = 0
        dummy_container = abjad.Container(
            abjad.mutate(self._current_window[:]).copy()
        )
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
                selection = abjad.select(dummy_container).leaf(index)
                abjad.mutate(selection).replace(new_leaf)
                index += 1
        # attaching time signature structure
        enforce_time_signature(dummy_container,
                               self._time_signatures,
                               disable_rewrite_meter=True,
                               )
        # output
        self._is_first_window = False
        self._current_window = dummy_container[:]
        dummy_container[:] = []
        self._get_logical_selections()  # new logical selections

    @staticmethod
    def _remove_all_time_signatures(container):
        r'Removes all time signatures of an ``abjad.Container``'
        for leaf in abjad.select(container).leaves():
            if abjad.inspect(leaf).effective(abjad.TimeSignature):
                abjad.detach(abjad.TimeSignature, leaf)

    @staticmethod
    def _rotate_list(input_list: list,
                     *,
                     n_rotations: int = 1,
                     anticlockwise: bool = False,
                     ) -> list:
        r'Rotates a list.'
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
        r'The ``abjad.Container`` to be shuffled.'
        return copy.deepcopy(self._contents)

    @contents.setter
    def contents(self,
                 contents: abjad.Container
                 ):
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or child "
                            "class")
        self._contents = copy.deepcopy(contents)
        dummy_container = copy.deepcopy(self._contents)
        self._current_window = dummy_container[:]
        dummy_container[:] = []
        self._get_logical_selections()
        self._get_pitch_list()
        self._time_signatures = time_signature_extractor(contents,
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
        rewritten by the ``rewrite_meter`` mutation.
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
        r"Sets the argument ``boundary_depth`` of abjad's ``rewrite_meter()``."
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
        r"""Sets the argument ``maximum_dot_count`` of abjad's
        ``rewrite_meter()``.
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
        r"""Sets the argument ``rewrite_tuplets`` of abjad's
        ``rewrite_meter()``.
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
    def processs_on_first_call(self) -> bool:
        r"""If ``True`` then the ``contents`` will be processed in the very
        first call.
        """
        return self._processs_on_first_call

    @processs_on_first_call.setter
    def processs_on_first_call(self,
                               processs_on_first_call: bool,
                               ):
        if not isinstance(processs_on_first_call, bool):
            raise TypeError("'processs_on_first_call' must be 'bool'")
        self._processs_on_first_call = processs_on_first_call

    @property
    def current_window(self) -> abjad.Selection:
        r'Read-only property, returns the result of the last operation.'
        current_window = copy.deepcopy(self._current_window)
        if self._omit_time_signatures:
            self._remove_all_time_signatures(current_window)
        return current_window
