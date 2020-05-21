import copy
from math import ceil
import abjad
from ._LoopParent import _LoopParent


class LoopByWindow(_LoopParent):
    r"""This class can be used to output slices of an ``abjad.Container`` using
    the metaphor of a looping window of a constant size given by an
    ``abjad.Duration``.

    ..  container:: example

        Usage is similar to other factory classes. It takes a container (or
        child class equivalent) as argument. Each call of the object, in this
        case ``looper()``, will move the window forwards and output the sliced
        window. If no window_size nor step_size are entered as arguments, they
        are set to the following default values, respectively: (4, 4), i.e. a
        window of the size of a 4/4 bar, and (1, 16), i.e. a step of the length
        of a sixteenth-note.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByWindow(input_music)
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

        .. figure:: ../_images/image-LoopByWindow-1.png

        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8.
            d'16
            ~
            d'4..
            e'16
            ~
            e'8.
            f'16
        }

        .. figure:: ../_images/image-LoopByWindow-2.png

        The property ``current_window`` can be used to access the current
        window without moving the head forwards.

        >>> notes = looper.current_window()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8.
            d'16
            ~
            d'4..
            e'16
            ~
            e'8.
            f'16
        }

        .. figure:: ../_images/image-LoopByWindow-3.png

    ..  container:: example

        The very first call will output the input container without processing
        it. To disable this behaviour and have the looping window move on the
        very first call, initialise the class with the keyword argument
        ``move_window_on_first_call`` set to ``True``.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              move_window_on_first_call=True,
        ...                              )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'4..
            e'16
            ~
            e'8.
            f'16
        }

        .. figure:: ../_images/image-LoopByWindow-4.png

    ..  container:: example

        The optional arguments ``window_size`` and ``step_size`` can be used to
        set different window and step sizes. ``window_size`` can take a tuple
        or an ``abjad.Meter`` as input, while ``step_size`` takes a tuple or an
        ``abjad.Duration``.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              window_size=(3, 4),
        ...                              step_size=(1, 4),
        ...                              )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }

        .. figure:: ../_images/image-LoopByWindow-5.png

        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            d'2
            e'4
        }

        .. figure:: ../_images/image-LoopByWindow-6.png

    ..  container:: example

        The instances of ``LoopByWindow`` can also be used as an iterator,
        which can then be used in a for loop to exhaust all windows. Notice how
        it appends rests at the end of the container, until it is totally
        exhausted.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              window_size=(3, 4),
        ...                              step_size=(1, 8),
        ...                              )
        >>> staff = abjad.Staff()
        >>> for window in looper:
        ...     staff.append(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'2
            c'8
            d'8
            ~
            d'4.
            e'8
            d'2
            e'4
            d'4.
            e'8
            ~
            e'8
            r8
            d'4
            e'4
            r4
            d'8
            e'8
            ~
            e'8
            r4.
            e'4
            r2
            e'8
            r8
            r2
        }

        .. figure:: ../_images/image-LoopByWindow-7.png

    ..  container:: example

        This class can take many optional keyword arguments during its
        creation, besides ``window_size`` and ``step_size``. ``max_steps`` sets
        the maximum number of steps that the window can advance when the object
        is called, ranging between 1 and the input value (default is also 1).
        ``repetition_chance`` sets the chance of a window result repeating
        itself (that is, the window not moving forwards when called). It should
        range from 0.0 to 1.0 (default 0.0, i.e. no repetition).
        ``forward_bias`` sets the chance of the window moving forward instead
        of backwards. It should range from 0.0 to 1.0 (default 1.0, which means
        the window can only move forwards. A value of 0.5 gives 50% chance of
        moving forwards while a value of 0.0 will move the window only
        backwards). Finally, ``head_position`` can be used to offset the
        starting position of the looping window. It must be a tuple or an
        ``abjad.Duration``, and its default value is 0.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              window_size=(3, 4),
        ...                              step_size=(5, 8),
        ...                              max_steps=2,
        ...                              repetition_chance=0.25,
        ...                              forward_bias=0.2,
        ...                              head_position=(2, 8),
        ...                              omit_time_signature=False,
        ...                              )
        >>> looper.window_size
        3/4
        >>> looper.step_size
        5/8
        >>> looper.repetition_chance
        0.25
        >>> looper.forward_bias
        0.2
        >>> looper.max_steps
        2
        >>> looper.head_position
        1/4
        >>> looper.omit_time_signature
        False

        Use the properties below to change these values after initialisation.

        >>> looper.window_size = (5, 4)
        >>> looper.step_size = (1, 4)
        >>> looper.max_steps = 3
        >>> looper.repetition_chance = 0.1
        >>> looper.forward_bias = 0.8
        >>> looper.head_position = 0
        >>> looper.omit_time_signature = True
        >>> looper.window_size
        5/4
        >>> looper.step_size
        1/4
        >>> looper.max_steps
        3
        >>> looper.repetition_chance
        0.1
        >>> looper.forward_bias
        0.8
        >>> looper.head_position
        0
        >>> looper.omit_time_signature
        True

    ..  container:: example

        The function ``len()`` can be used to get the total number of steps
        in the contents (always rounded up).

        >>> input_music = abjad.Container(r"c'1")
        >>> looper = auxjad.LoopByWindow(input_music)
        >>> len(looper)
        16
        >>> input_music = abjad.Container(r"c'1")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              step_size=(1, 4),
        ...                              )
        >>> len(looper)
        4
        >>> input_music = abjad.Container(r"c'2..")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              step_size=(1, 4),
        ...                              window_size=(2, 4),
        ...                              )
        >>> len(looper)
        4

    ..  container:: example

        To run through the whole process and output it as a single container,
        from the initial head position until the process outputs the single
        last element, use the method ``output_all()``.

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              window_size=(3, 4),
        ...                              step_size=(1, 4),
        ...                              )
        >>> music = looper.output_all()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            d'4
            e'4
            f'4
            e'4
            f'4
            r4
            f'4
            r2
        }

        .. figure:: ../_images/image-LoopByWindow-8.png

    ..  container:: example

        When using ``output_all()``, set the keyword argument
        ``tie_identical_pitches`` to ``True`` in order to tie identical notes
        or chords at the end and beginning of consecutive windows.

        >>> input_music = abjad.Container(r"c'4 <e' f' g'>2 r4 f'2.")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              window_size=(3, 4),
        ...                              step_size=(1, 4),
        ...                              )
        >>> music = looper.output_all(tie_identical_pitches=True)
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            <e' f' g'>2
            ~
            <e' f' g'>2
            r4
            <e' f' g'>4
            r4
            f'4
            r4
            f'2
            ~
            f'2.
            ~
            f'2
            r4
            f'4
            r2
        }

        .. figure:: ../_images/image-LoopByWindow-9.png

    ..  container:: example

        To run through just part of the process and output it as a single
        container, starting from the initial head position, use the method
        ``output_n()`` and pass the number of iterations as argument. Similarly
        to ``output_all()``, the keyword argument ``tie_identical_pitches`` is
        available for tying pitches.

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              window_size=(3, 4),
        ...                              step_size=(1, 4),
        ...                              )
        >>> music = looper.output_n(2)
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-LoopByWindow-10.png

    .. container:: example

        To change the size of the looping window after instantiation, use the
        property ``window_size``. In the example below, the initial window is
        of size (4, 4), but changes to (3, 8) after three calls. Notice how the
        very first call attaches a time signature equivalent to the window size
        to the output window; subsequent calls will not have time signatures
        unless the size of the looping window changes.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByWindow(input_music)
        >>> staff = abjad.Staff()
        >>> for _ in range(3):
        ...     notes = looper()
        ...     staff.append(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
            c'8.
            d'16
            ~
            d'4..
            e'16
            ~
            e'8.
            f'16
            c'8
            d'8
            ~
            d'4.
            e'8
            ~
            e'8
            f'8
        }

        .. figure:: ../_images/image-LoopByWindow-11.png

        >>> looper.window_size = (3, 8)
        >>> staff = abjad.Staff()
        >>> for _ in range(3):
        ...     notes = looper()
        ...     staff.append(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'16
            d'16
            ~
            d'4
            d'4.
            d'4.
        }

        .. figure:: ../_images/image-LoopByWindow-12.png

        To disable time signatures altogether, initialise ``LoopByWindow`` with
        the keyword argument ``omit_time_signature`` set to ``True`` (default
        is ``False``), or use the ``omit_time_signature`` property after
        initialisation.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByWindow(input_music, omit_time_signature=True)
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'2
            e'4
        }

        .. figure:: ../_images/image-LoopByWindow-13.png

    ..  container:: example

        This class can handle dynamics and articulations too. When a leaf is
        shortened by the looping window's movement, the dynamics and
        articulations are still applied to it.

        >>> input_music = abjad.Container(
        ... r"c'4-.\p\< d'2--\f e'4->\ppp f'2 ~ f'8")
        >>> looper = auxjad.LoopByWindow(input_music)
        >>> staff = abjad.Staff()
        >>> for _ in range(2):
        ...     music = looper()
        ...     staff.append(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            \p
            - \staccato
            \<
            d'2
            \f
            - \tenuto
            e'4
            \ppp
            - \accent
            c'8.
            \p
            - \staccato
            \<
            d'16
            \f
            - \tenuto
            ~
            d'4..
            e'16
            \ppp
            - \accent
            ~
            e'8.
            f'16
        }

        .. figure:: ../_images/image-LoopByWindow-14.png

    .. container:: example

        Use the ``contents`` property to read as well as overwrite the contents
        of the looper. Notice that the ``head_position`` will remain on its
        previous value and must be reset to ``0`` if that's required.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopByWindow(input_music)
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

        .. figure:: ../_images/image-LoopByWindow-15.png

        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'8.
            d'16
            ~
            d'4..
            e'16
            ~
            e'8.
            f'16
        }

        .. figure:: ../_images/image-LoopByWindow-16.png

        >>> looper.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2. a'1")
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            e'16
            f'16
            g'8
            ~
            g'2
            ~
            g'8
            a'8
        }

        .. figure:: ../_images/image-LoopByWindow-17.png

        >>> looper.head_position = 0
        >>> notes = looper()
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

        .. figure:: ../_images/image-LoopByWindow-18.png

    ..  container:: example

        This class can handle tuplets, but this functionality should be
        considered experimental.

        >>> input_music = abjad.Container(r"\times 2/3 {c'8 d'8 e'} d'2.")
        >>> looper = auxjad.LoopByWindow(input_music,
        ...                              window_size=(3, 4),
        ...                              step_size=(1, 16))
        >>> staff = abjad.Staff()
        >>> for _ in range(3):
        ...     window = looper()
        ...     staff.append(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                \time 3/4
                c'8
                d'8
                e'8
            }
            d'2
            \times 2/3 {
                c'32
                d'16
                ~
                d'16
                e'8
            }
            d'16
            ~
            d'2
            \times 2/3 {
                d'16
                e'8
            }
            d'8
            ~
            d'2
        }

        .. figure:: ../_images/image-LoopByWindow-19.png
    """

    ### INITIALISER ###

    def __init__(self,
                 contents: abjad.Container,
                 *,
                 window_size: (tuple, abjad.Meter) = (4, 4),
                 step_size: (int, float, tuple, str, abjad.Duration) = (1, 16),
                 max_steps: int = 1,
                 repetition_chance: float = 0.0,
                 forward_bias: float = 1.0,
                 head_position: (int, float, tuple, str, abjad.Duration) = 0,
                 omit_time_signature: bool = False,
                 move_window_on_first_call: bool = False,
                 ):
        self.contents = contents
        self._new_time_signature = True
        self.omit_time_signature = omit_time_signature
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
        return str(abjad.f(self._contents))

    def __len__(self) -> int:
        r'Outputs the length of ``contents`` in terms of ``step_size``.'
        return ceil(abjad.inspect(self._contents).duration() / self._step_size)

    ### PRIVATE METHODS ###

    def _slice_contents(self):
        r"""This method takes a slice of size ``window_size`` out of the
        contents starting at the current ``head_position``.
        """
        head = self._head_position
        window_size = self._window_size
        dummy_container = copy.deepcopy(self._contents)
        # splitting leaves at both slicing points
        if head > abjad.Duration(0):
            abjad.mutate(dummy_container[:]).split([head,
                                                    window_size.duration,
                                                    ])
        else:
            abjad.mutate(dummy_container[:]).split([window_size.duration])
        # finding start and end indeces for the window
        for start in range(len(dummy_container)):
            if abjad.inspect(dummy_container[:start + 1]).duration() > head:
                break
        for end in range(start + 1, len(dummy_container)):
            if (abjad.inspect(dummy_container[start : end]).duration()
                    == window_size.duration):
                break
        else:
            end = len(dummy_container)
        # passing on indicators from the head of an initial splitted leaf
        for index in range(start - 1, -1, -1):
            if abjad.inspect(dummy_container[index]).indicator(abjad.Tie):
                inspect_contents = abjad.inspect(dummy_container[index - 1])
                if index == 0 or not inspect_contents.indicator(abjad.Tie):
                    inspect_contents = abjad.inspect(dummy_container[index])
                    for indicator in inspect_contents.indicators():
                        if not isinstance(indicator,
                                          (abjad.TimeSignature, abjad.Tie),
                                          ):
                            abjad.attach(indicator, dummy_container[start])
        # removing ties generated by the split mutation
        abjad.detach(abjad.Tie(), dummy_container[start - 1])
        abjad.detach(abjad.Tie(), dummy_container[end - 1])
        # appending rests if necessary
        contents_dur = abjad.inspect(dummy_container[start : end]).duration()
        if contents_dur < window_size.duration:
            missing_dur = window_size.duration - contents_dur
            rests = abjad.LeafMaker()(None, missing_dur)
            dummy_container.extend(rests)
            end += len(rests)
        # transforming abjad.Selection -> abjad.Container for rewrite_meter
        dummy_container = abjad.Container(
            abjad.mutate(dummy_container[start : end]).copy()
        )
        abjad.mutate(dummy_container[:]).rewrite_meter(window_size)
        if self._new_time_signature and not self._omit_time_signature:
            abjad.attach(abjad.TimeSignature(window_size),
                         abjad.select(dummy_container).leaves()[0],
                         )
            self._new_time_signature = False
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
        self._contents = copy.deepcopy(contents)
        self._remove_all_time_signatures(self._contents)
        self._contents_length = abjad.inspect(contents[:]).duration()

    @property
    def head_position(self) -> abjad.Duration:
        r'The position of the head at the start of a looping window.'
        return self._head_position

    @head_position.setter
    def head_position(self,
                      head_position: (tuple, abjad.Duration),
                      ):
        r"""This setter method replaces the paren'ts one since the parent's 
        method uses integers as input intead of tuples or ``abjad.Duration``.
        """
        if not isinstance(head_position,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'head_position' must be a number, 'tuple', or "
                            "'abjad.Duration'")
        if abjad.Duration(head_position) >= self._contents_length:
            raise ValueError("'head_position' must be smaller than the "
                             "length of 'contents'")
        self._is_first_window = True
        self._head_position = abjad.Duration(head_position)

    @property
    def window_size(self) -> abjad.Meter:
        r'The length of the looping window.'
        return self._window_size

    @window_size.setter
    def window_size(self,
                    window_size: (int, float, tuple, abjad.Meter),
                    ):
        r"""This setter method replaces the paren'ts one since the parent's
        method uses integers as input intead of tuples or ``abjad.Duration``.
        """
        if not isinstance(window_size,
                          (int, float, tuple, str, abjad.Meter),
                          ):
            raise TypeError("'window_size' must be 'tuple' or 'abjad.Meter'")
        if (abjad.Meter(window_size).duration
                > self._contents_length - self._head_position):
            raise ValueError("'window_size' must be smaller than or equal "
                             "to the length of 'contents'")
        if (self._is_first_window or self._window_size.duration
                != abjad.Meter(window_size).duration):
            self._window_size = abjad.Meter(window_size)
            self._new_time_signature = True

    @property
    def step_size(self) -> abjad.Duration:
        r'The size of each step when moving the head.'
        return self._step_size

    @step_size.setter
    def step_size(self,
                  step_size: (tuple, abjad.Duration),
                  ):
        r"""This setter method replaces the paren'ts one since the parent's
        method uses integers as input intead of tuples or ``abjad.Duration``.
        """
        if not isinstance(step_size,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'step_size' must be a 'tuple' or "
                            "'abjad.Duration'")
        self._step_size = abjad.Duration(step_size)

    @property
    def omit_time_signature(self) -> list:
        r'When ``True``, the output will contain no time signatures.'
        return self._omit_time_signature

    @omit_time_signature.setter
    def omit_time_signature(self,
                            omit_time_signature: bool,
                            ):
        if not isinstance(omit_time_signature, bool):
            raise TypeError("'omit_time_signature' must be 'bool'")
        self._omit_time_signature = omit_time_signature

    ### PRIVATE PROPERTIES ###

    @property
    def _done(self) -> bool:
        r"""Boolean indicating whether the process is done (i.e. whether the
        head position has overtaken the ``contents`` length).

        This property replaces the parent's one since the parent's property
        uses the number of indeces of ``contents``.
        """
        return (self._head_position >= self._contents_length
            or self._head_position < 0)
