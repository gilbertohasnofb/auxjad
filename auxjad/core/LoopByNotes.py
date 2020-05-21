import copy
import abjad
from ._LoopParent import _LoopParent
from ..utilities.simplified_time_signature_ratio import (
    simplified_time_signature_ratio
)


class LoopByNotes(_LoopParent):
    r"""This class can be used to output slices of an ``abjad.Container`` using
    the metaphor of a looping window of a variable size. This size is given by
    the argument ``window_size``, which is an ``int`` representing how many
    notes are to be included in each slice. The duration of the slice will be
    the sum of the duration of these notes.

    For instance, if the initial container had the logical ties
    ``[A, B, C, D, E, F]`` (where each letter represents one logical tie) and
    the looping window was size ``3``, the output would be:

    ``A B C B C D C D E D E F E F F``

    This can be better visualised as:

    .. code-block:: none

        A B C
          B C D
            C D E
              D E F
                E F
                  F

    ..  container:: example

        Usage is similar to other factory classes. It takes a container (or
        child class equivalent) and the number of elements of the window as
        arguments. Each call of the object, in this case ``looper()``, will
        move the window forwards and output the result.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=3,
        ...                             )
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

        .. figure:: ../_images/image-LoopByNotes-1.png

        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }

        .. figure:: ../_images/image-LoopByNotes-2.png

        The property ``current_window`` can be used to access the current
        window without moving the head forwards.

        >>> notes = looper.current_window
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }

        .. figure:: ../_images/image-LoopByNotes-3.png

    ..  container:: example

        The very first call will output the input container without processing
        it. To disable this behaviour and have the looping window move on the
        very first call, initialise the class with the keyword argument
        ``move_window_on_first_call`` set to ``True``.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByNotes(
        ...     input_music,
        ...     window_size=3,
        ...     move_window_on_first_call=True,
        ... )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }

        .. figure:: ../_images/image-LoopByNotes-4.png

    ..  container:: example

        The instances of ``LoopByNotes`` can also be used as an iterator, which
        can then be used in a for loop to exhaust all windows.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=2,
        ...                             )
        >>> staff = abjad.Staff()
        >>> for window in looper:
        ...     staff.append(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'2
            d'2
            e'4
            \time 1/4
            e'4
        }

        .. figure:: ../_images/image-LoopByNotes-5.png

        Notice how the second staff in the example above does not have a time
        signature. This is because consecutive identical time signatures are
        omitted by default. To change this behaviour, instantialise this class
        with the keyword argument ``force_identical_time_signatures`` set to
        ``True``, or change the ``force_identical_time_signatures`` property
        to alter its value after the initialisation.

    ..  container:: example

        This class can take many optional keyword arguments during its
        creation. ``step_size`` dictates the size of each individual step in
        number of elements (default value is 1). ``max_steps`` sets the maximum
        number of steps that the window can advance when the object is called,
        ranging between 1 and the input value (default is also 1).
        ``repetition_chance`` sets the chance of a window result repeating
        itself (that is, the window not moving forwards when called). It should
        range from 0.0 to 1.0 (default 0.0, i.e. no repetition).
        ``forward_bias`` sets the chance of the window moving forward instead
        of backwards. It should range from 0.0 to 1.0 (default 1.0, which means
        the window can only move forwards. A value of 0.5 gives 50% chance of
        moving forwards while a value of 0.0 will move the window only
        backwards). Finally, ``head_position`` can be used to offset the
        starting position of the looping window. It must be an integer and its
        default value is 0.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=3,
        ...                             step_size=1,
        ...                             max_steps=2,
        ...                             repetition_chance=0.25,
        ...                             forward_bias=0.2,
        ...                             head_position=0,
        ...                             omit_all_time_signatures=False,
        ...                             force_identical_time_signatures=False,
        ...                             )
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
        >>> looper.omit_all_time_signatures
        False
        >>> looper.force_identical_time_signatures
        False

        Use the properties below to change these values after initialisation.

        >>> looper.window_size = 2
        >>> looper.step_size = 2
        >>> looper.max_steps = 3
        >>> looper.repetition_chance = 0.1
        >>> looper.forward_bias = 0.8
        >>> looper.head_position = 2
        >>> looper.omit_all_time_signatures = True
        >>> looper.force_identical_time_signatures = True
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
        >>> looper.omit_all_time_signatures
        True
        >>> looper.force_identical_time_signatures
        True

    ..  container:: example

        To disable time signatures altogether, initialise ``LoopByNotes`` with
        the keyword argument ``omit_all_time_signatures`` set to ``True``
        (default is ``False``), or use the ``omit_time_signature`` property
        after initialisation.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=3,
        ...                             omit_all_time_signatures=True,
        ...                             )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'2
            e'4
        }

        .. figure:: ../_images/image-LoopByNotes-6.png

    ..  container:: example

        The function ``len()`` can be used to get the total number of elements
        in the contents.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=3,
        ...                             )
        >>> len(looper)
        5

    ..  container:: example

        To run through the whole process and output it as a single container,
        from the initial head position until the process outputs the single
        last element, use the method ``output_all()``.

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=2,
        ...                             )
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

        .. figure:: ../_images/image-LoopByNotes-7.png

    ..  container:: example

        When using ``output_all()``, set the keyword argument
        ``tie_identical_pitches`` to ``True`` in order to tie identical notes
        or chords at the end and beginning of consecutive windows.

        >>> input_music = abjad.Container(r"c'4 d'2 r8 d'4 <e' g'>8 r4 f'2. "
        ...                               "<e' g'>16")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=4,
        ...                             )
        >>> music = looper.output_all(tie_identical_pitches=True)
        >>> staff = abjad.Staff(music)
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

        .. figure:: ../_images/image-LoopByNotes-8.png

    ..  container:: example

        To run through just part of the process and output it as a single
        container, starting from the initial head position, use the method
        ``output_n()`` and pass the number of iterations as argument. Similarly
        to ``output_all()``, the keyword argument ``tie_identical_pitches`` is
        available for tying pitches.

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=2,
        ...                             )
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

        .. figure:: ../_images/image-LoopByNotes-9.png

    .. container:: example

        To change the size of the looping window after instantiation, use the
        property ``window_size``. In the example below, the initial window is
        of size 3, and so the first call of the looper object outputs the
        first, second, and third leaves. The window size is then set to 4, and
        the looper is called again, moving to the leaf in the next position,
        thus outputting the second, third, fourth, and fifth leaves.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=3,
        ...                             )
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

        .. figure:: ../_images/image-LoopByNotes-10.png

        >>> looper.window_size = 4
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 19/8
            d'2
            e'4
            f'2
            ~
            f'8
            g'1
        }

        .. figure:: ../_images/image-LoopByNotes-11.png

    .. container:: example

        Use the ``contents`` property to read as well as overwrite the contents
        of the looper. Notice that the ``head_position`` will remain on its
        previous value and must be reset to ``0`` if that's required.

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
        >>> looper = auxjad.LoopByNotes(input_music,
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

        .. figure:: ../_images/image-LoopByNotes-12.png

        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-LoopByNotes-13.png

        >>> looper.contents = abjad.Container(r"c'''4 r4 d'''4 r4 "
        ...                                   "e'''4 r4 f'''4 r4")
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            d'''4
            r4
            e'''4
        }

        .. figure:: ../_images/image-LoopByNotes-14.png

        >>> looper.head_position = 0
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'''4
            r4
            d'''4
        }

        .. figure:: ../_images/image-LoopByNotes-15.png

    ..  container:: example

        This class can handle tuplets, but the output is not ideal and so this
        functionality should be considered experimental. Time signatures will
        be correct when dealing with partial tuplets (thus having non-standard
        values in their denominators), but each individual note of a tuplet
        will have the ratio printed above it.

        >>> input_music = abjad.Container(r"c'4 d'8 \times 2/3 {a4 g2}")
        >>> looper = auxjad.LoopByNotes(input_music,
        ...                             window_size=2,
        ...                             )
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

        .. figure:: ../_images/image-LoopByNotes-16.png
    """

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
                 omit_all_time_signatures: bool = False,
                 force_identical_time_signatures: bool = False,
                 move_window_on_first_call: bool = False,
                 ):
        self.contents = contents
        self._omit_all_time_signatures = omit_all_time_signatures
        self._force_identical_time_signatures = force_identical_time_signatures
        self._last_time_signature = None
        super().__init__(head_position,
                         window_size,
                         step_size,
                         max_steps,
                         repetition_chance,
                         forward_bias,
                         move_window_on_first_call,
                         )

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Outputs the representation of ``contents``.'
        return str(self._contents)

    def __len__(self) -> int:
        r'Outputs the number of logical ties of ``contents``.'
        return len(self._contents)

    ### PRIVATE METHODS ###

    def _slice_contents(self):
        r"""This method takes a slice with ``window_size`` number of logical
        ties out of the contents starting at the current ``head_position``.
        """
        start = self.head_position
        end = self.head_position + self.window_size
        logical_ties = self._contents[start:end]
        dummy_container = abjad.Container()
        time_signature_duration = 0
        for logical_tie in logical_ties:
            effective_duration = abjad.inspect(logical_tie).duration()
            logical_tie_ = copy.deepcopy(logical_tie)
            dummy_container.append(logical_tie_)
            multiplier = effective_duration / logical_tie_.written_duration
            logical_tie_ = abjad.mutate(logical_tie_).scale(multiplier)
            time_signature_duration += effective_duration
        if len(logical_ties) > 0 and not self._omit_all_time_signatures:
            time_signature = abjad.TimeSignature(time_signature_duration)
            time_signature = simplified_time_signature_ratio(time_signature)
            if (time_signature != self._last_time_signature
                    or self._force_identical_time_signatures):
                abjad.attach(time_signature,
                             abjad.select(dummy_container).leaves()[0],
                             )
            self._last_time_signature = time_signature
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'The ``list`` which serves as the basis for the slices of the looper.'
        return self._contents

    @contents.setter
    def contents(self,
                 contents: abjad.Container,
                 ):
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or "
                            "child class")
        contents_ = copy.deepcopy(contents)
        self._remove_all_time_signatures(contents_)
        self._contents = abjad.select(contents_).logical_ties()

    @property
    def omit_all_time_signatures(self) -> list:
        r'When ``True``, the output will contain no time signatures.'
        return self._omit_all_time_signatures

    @omit_all_time_signatures.setter
    def omit_all_time_signatures(self,
                                 omit_all_time_signatures: bool,
                                 ):
        if not isinstance(omit_all_time_signatures, bool):
            raise TypeError("'omit_all_time_signatures' must be 'bool'")
        self._omit_all_time_signatures = omit_all_time_signatures

    @property
    def force_identical_time_signatures(self) -> list:
        r"""When ``True``, identical time signatures will not be removed from
        the output.
        """
        return self._force_identical_time_signatures

    @force_identical_time_signatures.setter
    def force_identical_time_signatures(self,
                                        force_identical_time_signatures: bool,
                                        ):
        if not isinstance(force_identical_time_signatures, bool):
            raise TypeError("'force_identical_time_signatures' must be 'bool'")
        self._force_identical_time_signatures = force_identical_time_signatures
