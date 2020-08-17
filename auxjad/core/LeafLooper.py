from typing import Optional, Union

import abjad

from ..utilities.mutate import mutate
from ..utilities.simplified_time_signature_ratio import (
    simplified_time_signature_ratio,
)
from ._LooperParent import _LooperParent


class LeafLooper(_LooperParent):
    r"""This class outputs slices of an |abjad.Container| using the metaphor
    of a looping window of a constant number of elements. This number is given
    by the argument :attr:`window_size`, which is an :obj:`int` representing
    how many notes are to be included in each slice. The duration of the slice
    will be the sum of the duration of these notes.

    For instance, if the initial container had the logical ties
    :math:`[A, B, C, D, E, F]` (where each letter represents one logical tie)
    and the looping window was size ``3``, the output would be:

    :math:`A B C B C D C D E D E F E F F`

    This can be better visualised as:

    .. code-block:: none

        A B C
          B C D
            C D E
              D E F
                E F
                  F

    Basic usage:
        Calling the object will return an |abjad.Selection| generated by the
        looping process. It takes a container (or child class equivalent) and
        the number of elements of the window as arguments. Each call of the
        object will move the window forwards and output the result.

        >>> container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }

        .. figure:: ../_images/LeafLooper-o372nj7r3sb.png

        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 11/8
            d'2
            e'8
            ~
            e'8
            f'8
            ~
            f'2
        }

        .. figure:: ../_images/LeafLooper-lszpb96x0rf.png

        The property :attr:`current_window` can be used to access the current
        window without moving the head forwards.

        >>> notes = looper.current_window
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 11/8
            d'2
            e'8
            ~
            e'8
            f'8
            ~
            f'2
        }

        .. figure:: ../_images/LeafLooper-2c1jo6ftfnu.png

    :attr:`process_on_first_call`:
        The very first call will output the input container without processing
        it. To disable this behaviour and have the looping window move on the
        very first call, initialise the class with the keyword argument
        :attr:`process_on_first_call` set to ``True``.

        >>> container = abjad.Container(r"c'4 d'8 e'2 f'8 g'4")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            process_on_first_call=True,
        ...                            )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            d'8
            e'8
            ~
            e'4.
            f'8
        }

        .. figure:: ../_images/LeafLooper-uvu1p1g04ne.png

    Using as iterator:
        The instances of this class can also be used as an iterator, which can
        then be used in a for loop to exhaust all windows. Note that unlike the
        methods :meth:`output_n` and :meth:`output_all`, time signatures are
        added to each window returned by the shuffler. Use the function
        |auxjad.mutate().remove_repeated_time_signatures()| to clean the output
        when using this class in this way.

        >>> container = abjad.Container(r"c'4 d'2 e'8 f'2")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=2,
        ...                            )
        >>> staff = abjad.Staff()
        >>> for window in looper:
        ...     staff.append(window)
        >>> auxjad.mutate(staff).remove_repeated_time_signatures()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'2
            \time 5/8
            d'2
            e'8
            e'8
            f'2
            \time 2/4
            f'2
        }

        .. figure:: ../_images/LeafLooper-tlddw14wnrm.png

    Arguments and properties:
        This class can take many optional keyword arguments during its
        creation. :attr:`step_size` dictates the size of each individual step
        in number of elements (default value is ``1``). :attr:`max_steps` sets
        the maximum number of steps that the window can advance when the object
        is called, ranging between ``1`` and the input value (default is also
        ``1``). :attr:`repetition_chance` sets the chance of a window result
        repeating itself (that is, the window not moving forwards when called).
        It should range from ``0.0`` to ``1.0`` (default ``0.0``, i.e. no
        repetition). :attr:`forward_bias` sets the chance of the window moving
        forward instead of backwards. It should range from ``0.0`` to ``1.0``
        (default ``1.0``, which means the window can only move forwards. A
        value of ``0.5`` gives :math:`50\%` chance of moving forwards while a
        value of ``0.0`` will move the window only backwards). Lastly,
        :attr:`head_position` can be used to offset the starting position of
        the looping window. It must be an :obj:`int` and its default value is
        ``0``.

        >>> container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            step_size=1,
        ...                            max_steps=2,
        ...                            repetition_chance=0.25,
        ...                            forward_bias=0.2,
        ...                            head_position=0,
        ...                            omit_time_signatures=False,
        ...                            process_on_first_call=True,
        ...                            )
        >>> looper.window_size
        3
        >>> looper.step_size
        1
        >>> looper.repetition_chance
        0.25
        >>> looper.forward_bias
        0.2
        >>> looper.max_steps
        2
        >>> looper.head_position
        0
        >>> looper.omit_time_signatures
        False
        >>> looper.process_on_first_call
        True

        Use the properties below to change these values after initialisation.

        >>> looper.window_size = 2
        >>> looper.step_size = 2
        >>> looper.max_steps = 3
        >>> looper.repetition_chance = 0.1
        >>> looper.forward_bias = 0.8
        >>> looper.head_position = 2
        >>> looper.omit_time_signatures = True
        >>> looper.process_on_first_call = False
        >>> looper.window_size
        2
        >>> looper.step_size
        2
        >>> looper.max_steps
        3
        >>> looper.repetition_chance
        0.1
        >>> looper.forward_bias
        0.8
        >>> looper.head_position
        2
        >>> looper.omit_time_signatures
        True
        >>> looper.process_on_first_call
        False

    Setting :attr:`forward_bias` to ``0.0``:
        Set :attr:`forward_bias` to ``0.0`` to move backwards instead of
        forwards (default is ``1.0``). The initial :attr:`head_position` must
        be greater than ``0`` otherwise the contents will already be exhausted
        in the very first call (since it will not be able to move backwards
        from that position).

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=2,
        ...                            head_position=2,
        ...                            forward_bias=0.0,
        ...                            )
        >>> notes = looper.output_all()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            e'4
            f'4
            d'4
            e'4
            c'4
            d'4
        }

        .. figure:: ../_images/LeafLooper-tdypneg8a1i.png

    :attr:`forward_bias` between ``0.0`` and ``1.0``:
        Setting :attr:`forward_bias` to a value in between ``0.0`` and ``1.0``
        will result in random steps being taken forward or backward, according
        to the bias. The initial value of :attr:`head_position` will once gain
        play an important role here, as the contents might be exhausted if the
        looper attempts to move backwards after reaching the head position
        ``0``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            head_position=3,
        ...                            forward_bias=0.5,
        ...                            )
        >>> notes = looper.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            f'4
            g'4
            a'4
            e'4
            f'4
            g'4
            f'4
            g'4
            a'4
            e'4
            f'4
            g'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/LeafLooper-la5quq8s3al.png

    :attr:`max_steps`:
        Setting the keyword argument :attr:`max_steps` to a value larger than
        ``1`` will result in a random number of steps (between ``1`` and
        :attr:`max_steps`) being applied at each call.

        >>> container = abjad.Container(
        ...     r"c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4 d''4 e''4"
        ... )
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=2,
        ...                            max_steps=4,
        ...                            )
        >>> notes = looper.output_n(4)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            g'4
            a'4
            a'4
            b'4
            c''4
            d''4
        }

        .. figure:: ../_images/LeafLooper-u7t1hsb1o79.png

    :func:`len()`:
        The function :func:`len()` can be used to get the total number of
        elements in the contents.

        >>> container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            )
        >>> len(looper)
        5

    :meth:`output_all`:
        To run through the whole process and output it as a single container,
        from the initial head position until the process outputs the single
        last element, use the method :meth:`output_all`.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=2,
        ...                            )
        >>> window = looper.output_all()
        >>> staff = abjad.Staff(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            \time 2/4
            d'4
            e'4
            \time 2/4
            e'4
            f'4
            \time 1/4
            f'4
        }

        .. figure:: ../_images/LeafLooper-o5yqw4xinp.png

    ``tie_identical_pitches``:
        When using :meth:`output_all`, set the keyword argument
        ``tie_identical_pitches`` to ``True`` in order to tie identical notes
        or chords at the end and beginning of consecutive windows.

        >>> container = abjad.Container(
        ...     r"c'4 d'2 r8 d'4 <e' g'>8 r4 f'2. <e' g'>16"
        ... )
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=4,
        ...                            disable_rewrite_meter=True,
        ...                            )
        >>> notes = looper.output_all(tie_identical_pitches=True)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 9/8
            c'4
            d'2
            r8
            d'4
            ~
            \time 4/4
            d'2
            r8
            d'4
            <e' g'>8
            \time 3/4
            r8
            d'4
            <e' g'>8
            r4
            \time 11/8
            d'4
            <e' g'>8
            r4
            f'2.
            \time 19/16
            <e' g'>8
            r4
            f'2.
            <e' g'>16
            \time 17/16
            r4
            f'2.
            <e' g'>16
            \time 13/16
            f'2.
            <e' g'>16
            ~
            \time 1/16
            <e' g'>16
        }

        .. figure:: ../_images/LeafLooper-v1a75ntci7r.png

    :meth:`output_n`:
        To run through just part of the process and output it as a single
        container, starting from the initial head position, use the method
        :meth:`output_n` and pass the number of iterations as argument.
        Similarly to :meth:`output_all`, the keyword argument
        ``tie_identical_pitches`` is available for tying pitches.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=2,
        ...                            )
        >>> window = looper.output_n(2)
        >>> staff = abjad.Staff(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            \time 2/4
            d'4
            e'4
        }

        .. figure:: ../_images/LeafLooper-w389c0wnl2.png

    :attr:`omit_time_signatures`:
        To disable time signatures altogether, initialise this class with the
        keyword argument :attr:`omit_time_signatures` set to ``True`` (default
        is ``False``), or use the :attr:`omit_time_signatures` property after
        initialisation.

        >>> container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            omit_time_signatures=True,
        ...                            )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'2
            e'4
        }

        .. figure:: ../_images/LeafLooper-t3wqox0d0qe.png

    .. tip::

        All methods that return an |abjad.Selection| will add an initial time
        signature to it. The :meth:`output_n` and :meth:`output_all` methods
        automatically remove repeated time signatures. When joining selections
        output by multiple method calls, use
        |auxjad.mutate().remove_repeated_time_signatures()| on the whole
        container after fusing the selections to remove any unecessary time
        signature changes.

    :attr:`window_size`:
        To change the size of the looping window after instantiation, use the
        property :attr:`window_size`. In the example below, the initial window
        is of size ``3``, and so the first call of the looper object outputs
        the first, second, and third leaves. The window size is then set to
        ``4``, and the looper is called again, moving to the leaf in the next
        position, thus outputting the second, third, fourth, and fifth leaves.

        >>> container = abjad.Container(r"c'4 d'4 e'8 f'4 g'2")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/8
            c'4
            d'8
            ~
            d'8
            e'8
        }

        .. figure:: ../_images/LeafLooper-euq7xez3whk.png

        >>> looper.window_size = 4
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 9/8
            d'4
            e'8
            f'4
            g'2
        }

        .. figure:: ../_images/LeafLooper-9niipiwpbz.png

    :attr:`contents`:
        Use the :attr:`contents` property to read as well as overwrite the
        contents of the looper. Notice that the :attr:`head_position` will
        remain on its previous value and must be reset to ``0`` if that's
        required.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
        >>> looper = auxjad.LeafLooper(container,
        >>>                             window_size=3,
        >>>                             )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/LeafLooper-39uewm1fzrj.png

        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/LeafLooper-n6jrizfcon.png

        >>> looper.contents = abjad.Container(
        ...     r"cs'''4 ds'''4 es'''4 fs'''4"
        ... )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            ds'''4
            es'''4
            fs'''4
        }

        .. figure:: ../_images/LeafLooper-3lqsqrd3sar.png

        >>> looper.head_position = 0
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            cs'''4
            ds'''4
            es'''4
        }

        .. figure:: ../_images/LeafLooper-g3xybel6xu.png

    Indicators:
        This class supports dynamics and slurs.

        >>> container = abjad.Container(
        ...     r"c'4\p( d'2 e'4\f) f'2( ~ f'8 g'4 a'1\pp)"
        ... )
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            disable_rewrite_meter=True,
        ...                            )
        >>> notes = looper.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            \p
            (
            d'2
            e'4
            \f
            )
            \time 11/8
            d'2
            \p
            (
            e'4
            \f
            )
            f'2
            ~
            f'8
            \time 9/8
            e'4
            f'2
            (
            ~
            f'8
            g'4
            )
            \time 15/8
            f'2
            (
            ~
            f'8
            g'4
            a'1
            \pp
            )
            \time 5/4
            g'4
            \f
            (
            a'1
            \pp
            )
        }

        .. figure:: ../_images/LeafLooper-cqzbiawxp4.png

    :attr:`disable_rewrite_meter`:
        By default, this class uses the |abjad.mutate().rewrite_meter()|
        mutation.

        >>> container = abjad.Container(r"c'16 d'4 e'8. f'4 g'16")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            )
        >>> notes = looper.output_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'16
            d'8.
            ~
            d'16
            e'8.
            \time 11/16
            d'4
            e'8.
            f'4
            \time 2/4
            e'8.
            f'16
            ~
            f'8.
            g'16
        }

        .. figure:: ../_images/LeafLooper-ab18rc3voqn.png

        Set :attr:`disable_rewrite_meter` to ``True`` in order to disable this
        behaviour.

        >>> container = abjad.Container(r"c'16 d'4 e'8. f'4 g'16")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=3,
        ...                            disable_rewrite_meter=True,
        ...                            )
        >>> notes = looper.output_n(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'16
            d'4
            e'8.
            \time 11/16
            d'4
            e'8.
            f'4
            \time 2/4
            e'8.
            f'4
            g'16
        }

        .. figure:: ../_images/LeafLooper-fa30crzy146.png

    .. note::

        This class also accepts the properties ``boundary_depth``,
        ``maximum_dot_count``, and ``rewrite_tuplets``, which are passed on to
        |abjad.mutate().rewrite_meter()|, and ``fuse_across_groups_of_beats``,
        ``fuse_quadruple_meter``, ``fuse_triple_meter``, and
        ``extract_trivial_tuplets``, which are passed on to
        |auxjad.mutate().prettify_rewrite_meter()| (the latter can be disabled
        by setting ``prettify_rewrite_meter`` to ``False``). See the
        documentation of those functions for more details on these arguments.

    .. warning::

        This class can handle tuplets, but the engraving of the output is not
        ideal and so this functionality should be considered experimental. Time
        signatures will be correct when dealing with partial tuplets (thus
        having non-standard values in their denominators), but each individual
        note of a tuplet will have the ratio printed above them and there won't
        be a bracket spanning all notes.

        >>> container = abjad.Container(r"c'4 d'8 \times 2/3 {a4 g2}")
        >>> looper = auxjad.LeafLooper(container,
        ...                            window_size=2,
        ...                            )
        >>> window = looper.output_all()
        >>> staff = abjad.Staff(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            #(ly:expect-warning "strange time signature found")
            \time 7/24
            d'8
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                a4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                \time 2/4
                a4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g2
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                #(ly:expect-warning "strange time signature found")
                \time 2/6
                g2
            }
        }

        .. figure:: ../_images/LeafLooper-nre2ecw27l.png

    .. tip::

        The functions |auxjad.mutate().remove_repeated_dynamics()| and
        |auxjad.mutate().reposition_clefs()| can be used to clean the output
        and remove repeated dynamics and unnecessary clef changes.

    .. warning::

        Do note that some elements that span multiple notes (such as ottava
        indicators, manual beams, etc.) can become problematic when notes
        containing them are split into two. As a rule of thumb, it is always
        better to attach those to the music after the fading process has ended.
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_omit_time_signatures',
                 '_contents_logical_ties',
                 '_disable_rewrite_meter',
                 '_boundary_depth',
                 '_maximum_dot_count',
                 '_rewrite_tuplets',
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
                 window_size: int,
                 step_size: int = 1,
                 max_steps: int = 1,
                 repetition_chance: float = 0.0,
                 forward_bias: float = 1.0,
                 head_position: int = 0,
                 omit_time_signatures: bool = False,
                 process_on_first_call: bool = False,
                 disable_rewrite_meter: bool = False,
                 boundary_depth: Optional[int] = None,
                 maximum_dot_count: Optional[int] = None,
                 rewrite_tuplets: bool = True,
                 prettify_rewrite_meter: bool = True,
                 extract_trivial_tuplets: bool = True,
                 fuse_across_groups_of_beats: bool = True,
                 fuse_quadruple_meter: bool = True,
                 fuse_triple_meter: bool = True,
                 ):
        r'Initialises self.'
        self.contents = contents
        self._omit_time_signatures = omit_time_signatures
        self._disable_rewrite_meter = disable_rewrite_meter
        self._boundary_depth = boundary_depth
        self._maximum_dot_count = maximum_dot_count
        self._rewrite_tuplets = rewrite_tuplets
        self._prettify_rewrite_meter = prettify_rewrite_meter
        self._extract_trivial_tuplets = extract_trivial_tuplets
        self._fuse_across_groups_of_beats = fuse_across_groups_of_beats
        self._fuse_quadruple_meter = fuse_quadruple_meter
        self._fuse_triple_meter = fuse_triple_meter
        super().__init__(head_position,
                         window_size,
                         step_size,
                         max_steps,
                         repetition_chance,
                         forward_bias,
                         process_on_first_call,
                         )

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Returns interpreter representation of :attr:`contents`.'
        return format(self._contents)

    def __len__(self) -> int:
        r'Returns the number of logical ties of :attr:`contents`.'
        return len(self._contents_logical_ties)

    ### PRIVATE METHODS ###

    def _slice_contents(self):
        r"""This method takes a slice with :attr:`window_size` number of
        logical ties out of :attr:`contents` starting at the current
        :attr:`head_position`.
        """
        start = self._head_position
        end = self._head_position + self._window_size
        logical_ties = self._contents_logical_ties[start:end]
        dummy_container = abjad.Container()
        time_signature_duration = 0
        for logical_tie in logical_ties:
            effective_duration = abjad.inspect(logical_tie).duration()
            logical_tie_ = abjad.mutate(logical_tie).copy()
            dummy_container.append(logical_tie_)
            multiplier = effective_duration / logical_tie_.written_duration
            logical_tie_ = abjad.mutate(logical_tie_).scale(multiplier)
            time_signature_duration += effective_duration
        if len(logical_ties) > 0:
            time_signature = abjad.TimeSignature(time_signature_duration)
            time_signature = simplified_time_signature_ratio(time_signature)
            abjad.attach(time_signature, abjad.select(dummy_container).leaf(0))
        self._notate_music(dummy_container, start)

    def _notate_music(self,
                      dummy_container: abjad.Container,
                      start: int,
                      ):
        r'Handles the notation aspects of the looping window.'
        start_head = abjad.select(dummy_container).logical_tie(0)[0]
        start_tail = abjad.select(dummy_container).logical_tie(0)[-1]
        if (abjad.inspect(start_head).indicator(abjad.StartSlur) is None
                and abjad.inspect(start_tail).indicator(abjad.StopSlur)
                is None):
            for leaf in self._contents_logical_ties[start - 1::-1].leaves():
                if abjad.inspect(leaf).indicator(abjad.StartSlur) is not None:
                    abjad.attach(abjad.StartSlur(), start_head)
                    break
                elif abjad.inspect(leaf).indicator(abjad.StopSlur) is not None:
                    break
        if abjad.inspect(start_head).indicator(abjad.Dynamic) is None:
            for leaf in self._contents_logical_ties[start - 1::-1].leaves():
                dynamic = abjad.inspect(leaf).indicator(abjad.Dynamic)
                if dynamic is not None:
                    abjad.attach(dynamic, start_head)
                    break
        mutate(dummy_container[:]).reposition_dynamics()
        mutate(dummy_container[:]).reposition_slurs()
        # rewriting meter
        if not self._disable_rewrite_meter:
            mutate(dummy_container).auto_rewrite_meter(
                boundary_depth=self._boundary_depth,
                maximum_dot_count=self._maximum_dot_count,
                rewrite_tuplets=self._rewrite_tuplets,
                prettify_rewrite_meter=self._prettify_rewrite_meter,
                extract_trivial_tuplets=self._extract_trivial_tuplets,
                fuse_across_groups_of_beats=self._fuse_across_groups_of_beats,
                fuse_quadruple_meter=self._fuse_quadruple_meter,
                fuse_triple_meter=self._fuse_triple_meter,
            )
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> abjad.Container:
        r'The |abjad.Container| to be sliced and looped.'
        return abjad.mutate(self._contents).copy()

    @contents.setter
    def contents(self,
                 contents: abjad.Container,
                 ):
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or "
                            "child class")
        if not abjad.select(contents).leaves().are_contiguous_logical_voice():
            raise ValueError("'contents' must be contiguous logical voice")
        if isinstance(contents, abjad.Score):
            self._contents = abjad.mutate(contents[0]).copy()
        elif isinstance(contents, abjad.Tuplet):
            self._contents = abjad.Container([abjad.mutate(contents).copy()])
        else:
            self._contents = abjad.mutate(contents).copy()
        dummy_container = abjad.mutate(self._contents).copy()
        self._remove_all_time_signatures(dummy_container)
        selector = abjad.select(dummy_container)
        self._contents_logical_ties = selector.logical_ties()
        self._is_first_window = True

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
    def disable_rewrite_meter(self) -> bool:
        r"""When ``True``, the durations of the notes in the output will not be
        rewritten by the |abjad.mutate().rewrite_meter()| mutation. Rests will
        have the same duration as the logical ties they replaced.
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
