import copy
import random
import abjad
from ..utilities.time_signature_extractor import time_signature_extractor
from ..utilities.enforce_time_signature import enforce_time_signature
from ..utilities.leaves_are_tieable import leaves_are_tieable


class Phaser():
    r"""Phaser will shift all leaves of an ``abjad.Container`` by a fixed
    amount. Subsequent calls apply further shifts.

    ..  container:: example

        Calling the object will return an ``abjad.Selection`` generated by
        the phasing process. Each call of the object will shift the contents of
        the input container by a fixed amount.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container)
        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Phaser-1.png

        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }

        .. figure:: ../_images/image-Phaser-2.png

        The property ``current_window`` can be used to access the current
        window without moving the head forwards.

        >>> notes = phaser.current_window()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }

        .. figure:: ../_images/image-Phaser-3.png

    ..  container:: example

        The very first call will output the input container without processing
        it. To disable this behaviour and phase on the very first call,
        initialise the class with the keyword argument ``phase_on_first_call``
        set to ``True``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        phase_on_first_call=True,
        ...                        )
        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }

        .. figure:: ../_images/image-Phaser-4.png

    ..  container:: example

        The optional argument ``step_size`` can be used to step sizes for the
        phasing process. It takes a tuple or an ``abjad.Duration``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 8),
        ...                        )
        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Phaser-5.png

        >>> notes = phaser()
        >>> staff.append(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'8
            ~
            f'8
            c'8
        }

        .. figure:: ../_images/image-Phaser-6.png

    ..  container:: example

        The instances of ``Phaser`` can also be used as an iterator,
        which can then be used in a for loop to exhaust all windows. Notice how
        it appends rests at the end of the container, until it is totally
        exhausted.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 ~ e'2.")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 4),
        ...                        )
        >>> staff = abjad.Staff()
        >>> for window in phaser:
        ...     staff.append(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            ~
            e'2.
            d'4
            e'2
            ~
            e'2
            c'4
            e'2.
            ~
            e'4
            c'4
            d'4
            e'2.
            c'4
            d'4
            e'4
            e'2
            c'4
            d'4
            e'2
            e'4
            c'4
            d'4
            e'2.
        }

        .. figure:: ../_images/image-Phaser-7.png

    ..  container:: example

        This class can take many optional keyword arguments during its
        creation, besides ``step_size``. ``max_steps`` sets
        the maximum number of steps that can be applied for a single call,
        ranging between ``1`` and the input value (default is also ``1``); if
        ``max_steps`` is set to a value larger than 1, the number of steps at
        every call will be randomly chosen. ``forward_bias`` sets the chance of
        the process moving forward instead of backwards. It should range from
        ``0.0`` to ``1.0`` (default ``1.0``, which means the process can only
        move forwards. A value of ``0.5`` gives 50% chance of moving forwards
        while a value of ``0.0`` will result in the process moving only
        backwards). By default, when a logical tie is split in between windows,
        any unterminated ties will be removed; set ``remove_unterminated_ties``
        to ``False`` to disable this behaviour.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(5, 8),
        ...                        max_steps=2,
        ...                        forward_bias=0.2,
        ..                         remove_unterminated_ties=True,
        ...                        )
        >>> phaser.step_size
        5/8
        >>> phaser.max_steps
        2
        >>> phaser.forward_bias
        0.2
        >>> phaser.remove_unterminated_ties
        True

        Use the properties below to change these values after initialisation.

        >>> phaser.step_size = (1, 4)
        >>> phaser.max_steps = 3
        >>> phaser.forward_bias = 0.8
        >>> phaser.remove_unterminated_ties = False
        >>> phaser.step_size
        1/4
        >>> phaser.max_steps
        3
        >>> phaser.forward_bias
        0.8
        >>> phaser.remove_unterminated_ties
        False

    .. container:: example

        Set ``forward_bias`` to ``0.0`` to move backwards instead of forwards
        (default is ``1.0``).

        >>> container = abjad.Container(r"\time 3/8 c'8 d'8 e'8")
        >>> phaser = auxjad.Phaser(container)
        >>> notes = phaser.output_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'8
            d'8
            e'8
            c'16
            d'16
            ~
            d'16
            e'16
            ~
            e'16
            c'16
            d'8
            e'8
            c'8
        }

        .. figure:: ../_images/image-Phaser-8.png

        >>> container = abjad.Container(r"\time 3/8 c'8 d'8 e'8")
        >>> phaser = auxjad.Phaser(container,
        ...                        forward_bias=0.0,
        ...                        )
        >>> notes = phaser.output_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'8
            d'8
            e'8
            e'16
            c'16
            ~
            c'16
            d'16
            ~
            d'16
            e'16
            e'8
            c'8
            d'8
        }

        .. figure:: ../_images/image-Phaser-9.png

    .. container:: example

        Setingt ``forward_bias`` to a value in between ``0.0`` and ``1.0`` will
        result in random steps being taken forward or backward, according to
        the bias.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 4),
        ...                        forward_bias=0.5,
        ...                        )
        >>> notes = phaser.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            d'4
            e'4
            f'4
            c'4
            c'4
            d'4
            e'4
            f'4
            f'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Phaser-10.png

    ..  container:: example

        Setting the keyword argument ``max_steps`` to a value larger than ``1``
        will result in a random number of steps (between ``1`` and
        ``max_steps``) being applied at each call.

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 8),
        ...                        max_steps=4,
        ...                        )
        >>> notes = phaser.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
            f'8
            g'8
            a'8
            b'8
            c''8
            c'8
            d'8
            e'8
            c''8
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            f'8
            g'8
            a'8
            b'8
            c''8
            c'8
            d'8
            e'8
            a'8
            b'8
            c''8
            c'8
            d'8
            e'8
            f'8
            g'8
        }

        .. figure:: ../_images/image-Phaser-11.png

    ..  container:: example

        The function ``len()`` can be used to get the total number of steps
        that are necessary to return to the initial container.

        >>> container = abjad.Container(r"c'1")
        >>> phaser = auxjad.Phaser(container)
        >>> len(phaser)
        16
        >>> container = abjad.Container(r"c'1")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 4),
        ...                        )
        >>> len(phaser)
        4
        >>> container = abjad.Container(r"\time 3/4 c'2.")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 2),
        ...                        )
        >>> len(phaser)
        3

    ..  container:: example

        To run through the whole process and output it as a single container,
        from the initial head position until the process outputs the single
        last element, use the method ``output_all()``.

        >>> container = abjad.Container(r"\time 3/4 c'4. d'4.")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 4),
        ...                        )
        >>> notes = phaser.output_all()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4.
            d'4.
            c'8
            d'8
            ~
            d'4
            c'4
            d'4
            c'4
            ~
            c'8
            d'8
            c'4.
            d'4.
        }

        .. figure:: ../_images/image-Phaser-12.png

    ..  container:: example

        By default, ``output_all()`` will cycle back to the very first window.
        To stop at the iteration step just before looping back to the initial
        container, set the keyword argument ``cycle_back_to_first`` to
        ``False``.

        >>> container = abjad.Container(r"\time 3/4 c'4. d'4.")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 4),
        ...                        )
        >>> notes = phaser.output_all(cycle_back_to_first=False)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4.
            d'4.
            c'8
            d'8
            ~
            d'4
            c'4
            d'4
            c'4
            ~
            c'8
            d'8
        }

        .. figure:: ../_images/image-Phaser-13.png

    ..  container:: example

        To run through just part of the process and output it as a single
        container, starting from the initial head position, use the method
        ``output_n()`` and pass the number of iterations as argument.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 32),
        ...                        )
        >>> notes = phaser.output_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'8..
            d'32
            ~
            d'8..
            e'32
            ~
            e'8..
            f'32
            ~
            f'8..
            c'32
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }

        .. figure:: ../_images/image-Phaser-14.png

    .. container:: example

        All methods that call the phasing process (``__call__()``,
        ``__next__()``, ``output_all()``, ``output_n()``) remove unterminated
        ties at the end of a selection, which are a result of a logical tie
        being split at that point. Use the optional keyword argument
        ``remove_unterminated_ties=False`` when initialising the phaser to
        disable this behaviour.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        phase_on_first_call=True,
        ...                        remove_unterminated_ties=False,
        ...                        )
        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
            ~
        }

        .. figure:: ../_images/image-Phaser-15.png

    ..  container:: example

        By default, only the first output selection will contain a time
        signature (unless time signature changes require it, see below). Use
        the optional keyword argument ``force_time_signature`` when calling the
        phaser in order to force an initial time signature. Compare the two
        cases below; in the first, the variable ``notes2`` won't have a time
        signature appended to its first leaf because the phaser had been called
        before (though LilyPond will fallback to a default 4/4 time signature
        when none is found in the source file). In the second,
        ``force_time_signature`` is set to ``True``, and the output of
        ``abjad.f(staff)`` now includes ``\time 3/4`` (and LilyPond does not
        fallback to a 4/4 time signature).

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 8),
        ...                        )
        >>> notes1 = phaser()
        >>> notes2 = phaser()
        >>> staff = abjad.Staff(notes2)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            c'8
        }

        .. figure:: ../_images/image-Phaser-16.png

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 8),
        ...                        )
        >>> notes1 = phaser()
        >>> notes2 = phaser(force_time_signature=True)
        >>> staff = abjad.Staff(notes2)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            c'8
        }

        .. figure:: ../_images/image-Phaser-17.png

    ..  container:: example

        This class handles time signature changes.

        >>> container = abjad.Container(
        ...     r"\time 2/4 c'2 \time 3/8 d'4. \time 2/4 e'2")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 8),
        ...                        )
        >>> notes = phaser.output_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'2
            \time 3/8
            d'4.
            \time 2/4
            e'2
            c'4
            ~
            c'8
            d'8
            ~
            \time 3/8
            d'4
            e'8
            ~
            \time 2/4
            e'4
            ~
            e'8
            c'8
            c'4
            d'4
            ~
            \time 3/8
            d'8
            e'4
            ~
            \time 2/4
            e'4
            c'4
        }

        .. figure:: ../_images/image-Phaser-18.png

    ..  container:: example

        This class can handle dynamics and articulations too. When a logical
        tie is split into two during the phasing process, dynamics and
        articulations are passed on to both of them.

        >>> container = abjad.Container(r"c'4-.\p\< d'4--\f e'4->\p f'4")
        >>> phaser = auxjad.Phaser(container,
        ...                        step_size=(1, 8),
        ...                        )
        >>> staff = abjad.Staff()
        >>> music = phaser.output_n(5)
        >>> staff.append(music)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \p
            - \staccato
            \<
            d'4
            \f
            - \tenuto
            e'4
            \p
            - \accent
            f'4
            c'8
            \p
            - \staccato
            \<
            d'8
            \f
            - \tenuto
            ~
            d'8
            e'8
            \p
            - \accent
            ~
            e'8
            f'8
            ~
            f'8
            c'8
            \p
            - \staccato
            d'4
            \f
            - \tenuto
            e'4
            \p
            - \accent
            f'4
            c'4
            \p
            - \staccato
            \<
            d'8
            \f
            - \tenuto
            e'8
            \p
            - \accent
            ~
            e'8
            f'8
            ~
            f'8
            c'8
            \p
            - \staccato
            ~
            c'8
            \<
            d'8
            \f
            - \tenuto
            e'4
            \p
            - \accent
            f'4
            c'4
            \p
            - \staccato
            \<
            d'4
            \f
            - \tenuto
        }

        .. figure:: ../_images/image-Phaser-19.png

    ..  warning::

        Do note that elements that span multiple notes (such as hairpins,
        ottava indicators, manual beams, etc.) can become problematic when
        notes containing them are split into two. Whenever possible, it is
        always better to attach those to the music after the phasing process is
        concluded.

    .. container:: example

        Use the ``contents`` property to read as well as overwrite the contents
        of the phaser. Notice that the phasing process will start from the
        beginning of the new container.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> phaser = auxjad.Phaser(container)
        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Phaser-20.png

        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }

        .. figure:: ../_images/image-Phaser-21.png

        >>> phaser.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2.")
        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'16
            e'16
            f'16
            g'2.
        }

        .. figure:: ../_images/image-Phaser-22.png

        >>> notes = phaser()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            d'16
            e'16
            f'16
            g'16
            ~
            g'2
            ~
            g'8.
            c'16
        }

        .. figure:: ../_images/image-Phaser-23.png

    ..  warning::

        This class can handle tuplets, but the output is often quite complex.
        Although the result will be rhythmically correct, consecutive tuplets
        are not fused together, and tuplets may be output off-beat. This
        functionality should be considered experimental.

        >>> container = abjad.Container(r"\times 2/3 {c'8 d'8 e'8} d'2.")
        >>> phaser = auxjad.Phaser(container)
        >>> staff = abjad.Staff()
        >>> for _ in range(3):
        ...     window = phaser()
        ...     staff.append(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            d'2.
            \times 2/3 {
                c'32
                d'16
                ~
                d'16
                e'32
                ~
                e'16.
            }
            d'16
            ~
            d'2
            ~
            d'8.
            \times 2/3 {
                c'16.
            }
            \times 2/3 {
                d'16
                e'8
            }
            d'8
            ~
            d'2
            ~
            d'8
            \times 2/3 {
                c'8
                d'16
            }
        }

        .. figure:: ../_images/image-Phaser-24.png
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_contents',
                 '_pivot_point',
                 '_step_size',
                 '_max_steps',
                 '_forward_bias',
                 '_remove_unterminated_ties',
                 '_current_window',
                 '_is_first_window',
                 '_new_time_signature',
                 '_contents_length',
                 )

    ### INITIALISER ###

    def __init__(self,
                 contents: abjad.Container,
                 *,
                 step_size: (int, float, tuple, str, abjad.Duration) = (1, 16),
                 max_steps: int = 1,
                 forward_bias: float = 1.0,
                 phase_on_first_call: bool = False,
                 remove_unterminated_ties: bool = True,
                 ):
        r'Initialises self.'
        self.contents = contents
        self._pivot_point = abjad.Duration(0)
        self._new_time_signature = True
        self.step_size = step_size
        self.max_steps = max_steps
        self.forward_bias = forward_bias
        self.remove_unterminated_ties = remove_unterminated_ties
        if not isinstance(phase_on_first_call, bool):
            raise TypeError("'phase_on_first_call' must be 'bool'")
        self._is_first_window = not phase_on_first_call
        self._current_window = None

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Returns interpret representation of  ``contents``.'
        return format(self._contents)

    def __len__(self) -> int:
        r'Returns the length of ``contents`` in terms of ``step_size``.'
        proportion = self._contents_length / self._step_size
        return int(proportion * proportion.denominator)

    def __call__(self,
                 *,
                 force_time_signature: bool = False,
                 ) -> abjad.Selection:
        r"""Calls the phaser process for one iteration, returning an
        ``abjad.Selection``.
        """
        if not isinstance(force_time_signature, bool):
            raise TypeError("'force_time_signature' must be 'bool'")
        if force_time_signature:
            self._new_time_signature = True
        self._move_pivot_point()
        self._phase_contents()
        return copy.deepcopy(self._current_window)

    def __next__(self,
                 *,
                 force_time_signature: bool = False,
                 ) -> abjad.Selection:
        r"""Calls the phaser process for one iteration, returning an
        ``abjad.Selection``.
        """
        if not isinstance(force_time_signature, bool):
            raise TypeError("'force_time_signature' must be 'bool'")
        if force_time_signature:
            self._new_time_signature = True
        self._move_pivot_point()
        if self._done:
            raise StopIteration
        self._phase_contents()
        return copy.deepcopy(self._current_window)

    def __iter__(self):
        r'Returns an iterator, allowing instances to be used as iterators.'
        return self

    ### PUBLIC METHODS ###

    def output_all(self,
                   *,
                   cycle_back_to_first: bool = True,
                   tie_identical_pitches: bool = False,
                   ) -> abjad.Selection:
        r"""Goes through the whole phasing process and outputs a single
        ``abjad.Selection``.
        """
        if not isinstance(cycle_back_to_first, bool):
            raise TypeError("'cycle_back_to_first' must be 'bool'")
        if not isinstance(tie_identical_pitches, bool):
            raise TypeError("'tie_identical_pitches' must be 'bool'")
        dummy_container = abjad.Container()
        while True:
            selection = self.__call__()
            if not self._done:
                if tie_identical_pitches:
                    self._tie_identical_pitches(selection, dummy_container)
                dummy_container.append(selection)
            else:
                break
        if cycle_back_to_first:
            if tie_identical_pitches:
                self._tie_identical_pitches(selection, dummy_container)
            dummy_container.append(selection)
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    def output_n(self,
                 n: int,
                 *,
                 tie_identical_pitches: bool = False,
                 ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the phasing process and outputs a
        single ``abjad.Selection``.
        """
        if not isinstance(n, int):
            raise TypeError("first positional argument must be 'int'")
        if n < 1:
            raise ValueError("first positional argument must be a positive "
                             "'int'")
        if not isinstance(tie_identical_pitches, bool):
            raise TypeError("'tie_identical_pitches' must be 'bool'")
        dummy_container = abjad.Container()
        for _ in range(n):
            selection = self.__call__()
            if tie_identical_pitches:
                self._tie_identical_pitches(selection, dummy_container)
            dummy_container.append(selection)
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    ### PRIVATE METHODS ###

    def _move_pivot_point(self):
        r"""Moves the pivot point by a certain number of steps of fixed size,
        either forwards or backwards according to the forward bias.
        """
        if not self._is_first_window:  # 1st window always at initial position
            step = self._step_size * random.randint(1, self._max_steps)
            diretion = self._biased_choice(self._forward_bias)
            self._pivot_point += step * diretion
        else:
            self._is_first_window = False

    def _phase_contents(self):
        r"""This method phases ``contents`` using ``_pivot_point`` as the
        pivot point.
        """
        pivot = self._pivot_point % self._contents_length
        dummy_container = copy.deepcopy(self._contents)
        time_signatures = time_signature_extractor(dummy_container)
        # splitting leaves at both slicing points
        if pivot > abjad.Duration(0):
            abjad.mutate(dummy_container[:]).split([pivot])
            # finding start and end indeces for the window
            for start in range(len(dummy_container)):
                if abjad.inspect(dummy_container[:start+1]).duration() > pivot:
                    break
            last_leaf = dummy_container[:start].leaf(-1)
            # copying indicators to both leaves
            if abjad.inspect(last_leaf).indicator(abjad.Tie):  # i.e. split
                for indicator in abjad.inspect(last_leaf).indicators():
                    if isinstance(indicator, (abjad.Dynamic,
                                              abjad.Articulation,
                                              abjad.Staccato,
                                              abjad.Staccatissimo,
                                              abjad.Fermata,
                                              )):
                        first_leaf = dummy_container[start:].leaf(0)
                        abjad.attach(indicator, first_leaf)
            # removing ties of splitted logical tie if necessary
            if (self._remove_unterminated_ties and
                    abjad.inspect(last_leaf).indicator(abjad.Tie)):
                abjad.detach(abjad.Tie, last_leaf)
            # joining two subcontainers
            dummy_end_container = abjad.Container(
                abjad.mutate(dummy_container[:start]).copy()
            )
            dummy_container = abjad.Container(
                abjad.mutate(dummy_container[start:]).copy()
            )
            dummy_container.extend(dummy_end_container)
            dummy_end_container[:] = []
            # adding time signatures back and rewriting meter
            enforce_time_signature(dummy_container, time_signatures)
        # removing first time signature if repeated
        if not self._new_time_signature:
            for time_signature in time_signatures[::-1]:
                if time_signature is not None:
                    last_time_signature = time_signature
                    break
            if time_signatures[0] == last_time_signature:
                abjad.detach(abjad.TimeSignature,
                             abjad.select(dummy_container).leaf(0),
                             )
        self._new_time_signature = False
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    @staticmethod
    def _tie_identical_pitches(currrent_selection, previous_container):
        r'Ties identical pitches when joining windows.'
        if len(previous_container) == 0:
            return
        first_leaf = currrent_selection.leaf(0)
        last_leaf = abjad.select(previous_container).leaf(-1)
        if (leaves_are_tieable(first_leaf, last_leaf) and not
                abjad.inspect(last_leaf).indicators(abjad.Tie)):
            abjad.attach(abjad.Tie(), last_leaf)

    @staticmethod
    def _biased_choice(bias):
        r'Returns either +1 or -1 according to a bias value.'
        return random.choices([1, -1], weights=[bias, 1.0-bias])[0]

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> abjad.Container:
        r'The ``abjad.Container`` to be phased.'
        return copy.deepcopy(self._contents)

    @contents.setter
    def contents(self,
                 contents: abjad.Container,
                 ):
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or "
                            "child class")
        self._contents = copy.deepcopy(contents)
        self._contents_length = abjad.inspect(contents[:]).duration()
        self._pivot_point = abjad.Duration(0)
        self._is_first_window = True

    @property
    def current_window(self) -> abjad.Selection:
        r'Read-only property, returns the previously output selection.'
        return copy.deepcopy(self._current_window)

    @property
    def pivot_point(self) -> abjad.Duration:
        r'Read-only property, returns the position of the pivot point.'
        return self._pivot_point

    @property
    def step_size(self) -> abjad.Duration:
        r'The size of each step when moving the pivot point.'
        return self._step_size

    @step_size.setter
    def step_size(self,
                  step_size: (tuple, abjad.Duration),
                  ):
        if not isinstance(step_size,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'step_size' must be a 'tuple' or "
                            "'abjad.Duration'")
        self._step_size = abjad.Duration(step_size)

    @property
    def max_steps(self) -> int:
        r'The maximum number of steps per operation.'
        return self._max_steps

    @max_steps.setter
    def max_steps(self,
                  max_steps: int,
                  ):
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if max_steps < 1:
            raise ValueError("'max_steps' must be greater than zero")
        self._max_steps = max_steps

    @property
    def forward_bias(self) -> float:
        r"""The chance of the window moving forward instead of backwards. It
        should range from 0.0 to 1.0 (default 1.0, which means the window can
        only move forwards. A value of 0.5 gives 50% chance of moving forwards
        while a value of 0.0 will move the window only backwards).
        """
        return self._forward_bias

    @forward_bias.setter
    def forward_bias(self,
                     forward_bias: float,
                     ):
        if not isinstance(forward_bias, float):
            raise TypeError("'forward_bias' must be 'float'")
        if forward_bias < 0.0 or forward_bias > 1.0:
            raise ValueError("'forward_bias' must be between 0.0 and 1.0")
        self._forward_bias = forward_bias

    @property
    def remove_unterminated_ties(self) -> bool:
        r"""When ``True``, the last element of the ``abjad.Selection`` returned
        by a call will have any ties removed. This means that splitted logical
        ties will not tie accross multiple calls.
        """
        return self._remove_unterminated_ties

    @remove_unterminated_ties.setter
    def remove_unterminated_ties(self,
                                 remove_unterminated_ties: bool,
                                 ):
        if not isinstance(remove_unterminated_ties, bool):
            raise TypeError("'remove_unterminated_ties' must be 'bool'")
        self._remove_unterminated_ties = remove_unterminated_ties

    ### PRIVATE PROPERTIES ###

    @property
    def _done(self) -> bool:
        r"""Boolean indicating whether the process is done (i.e. whether the
        pivot point has overtaken the ``contents`` length). Only
        ``__next__()`` and ``output_all()`` make use of it, since regular calls
        make use of the module of the position of the pivot point in relation
        to the duration of ``contents``, allowing for infinitely many calls.
        """
        return (self._pivot_point >= self._contents_length
                or self._pivot_point <= -self._contents_length)
