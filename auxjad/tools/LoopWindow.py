import abjad
import random
import copy


class LoopWindow():
    r"""Using a looping window, this slices an input abjad.Container and output
    them as containers.

    ..  container:: example

        Usage is similar to other factory classes. It takes a container (or
        child class equivalent) as argument. Each call of the object, in this
        case looper(), will move the window forwards and output the sliced
        window. If no window_size nor step_size are entered as arguments, they
        are set to the following default values, respectively: (4, 4), i.e. a
        window of the size of a 4/4 bar, and (1, 16), i.e. a step of the length
        of a sixteenth-note.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindow(input_music)
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

        The method get_current_window() will output the current window without
        moving the head forwards.

        >>> notes = looper.get_current_window()
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

    ..  container:: example

        The optional arguments window_size and step_size can be used to set
        different window and step sizes. window_size can take a tuple or an
        abjad.Meter as input, while step_size takes a tuple or an
        abjad.Duration.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindow(input_music,
        ...                            window_size=(3, 4),
        ...                            step_size=(1, 4),
        ...                            )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            d'2
            e'4
        }

    ..  container:: example

        The instances of LoopWindow can also be used as an iterator, which can
        then be used in a for loop to exhaust all windows. Notice how it
        appends rests at the end of the container, until it is totally
        exhausted.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4")
        >>> looper = auxjad.LoopWindow(input_music,
        ...                            window_size=(3, 4),
        ...                            step_size=(1, 8),
        ...                            )
        >>> for window in looper:
        ...     staff = abjad.Staff(window)
        ...     abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }
        \new Staff
        {
            c'8
            d'8
            ~
            d'4.
            e'8
        }
        \new Staff
        {
            d'2
            e'4
        }
        \new Staff
        {
            d'4.
            e'8
            ~
            e'8
            r8
        }
        \new Staff
        {
            d'4
            e'4
            r4
        }
        \new Staff
        {
            d'8
            e'8
            ~
            e'8
            r4.
        }
        \new Staff
        {
            e'4
            r2
        }
        \new Staff
        {
            e'8
            r8
            r2
        }

    ..  container:: example

        This class can take many optional keyword arguments during its
        creation, besides window_size and step_size. max_steps sets the maximum
        number of steps that the window can advance when the object is called,
        ranging between 1 and the input value (default is also 1).
        repetition_chance sets the chance of a window result repeating itself
        (that is, the window not moving forwards when called). It should range
        from 0.0 to 1.0 (default 0.0, i.e. no repetition). Finally,
        head_position can be used to offset the starting position of the
        looping window. It must be a tuple or an abjad.Duration, and its
        default value is (0, 1) which is the equivalent of a duration of length
        zero.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindow(input_music,
        ...                            window_size=(3, 4),
        ...                            step_size=(5, 8),
        ...                            max_steps=2,
        ...                            repetition_chance=0.25,
        ...                            head_position=(2, 8),
        ...                            )
        >>> looper.window_size
        3/4
        >>> looper.step_size
        5/8
        >>> looper.repetition_chance
        0.25
        >>> looper.max_steps
        2
        >>> looper.head_position
        1/4

        Use the set methods below to change these values after initialisation.

        >>> looper.set_window_size((5, 4))
        >>> looper.set_step_size((1, 4))
        >>> looper.set_max_steps(3)
        >>> looper.set_repetition_chance(0.1)
        >>> looper.set_head_position((0, 1))
        >>> looper.window_size
        5/4
        >>> looper.step_size
        1/4
        >>> looper.max_steps
        3
        >>> looper.repetition_chance
        0.1
        >>> looper.head_position
        0

    ..  container:: example

        To run through the whole process and output it as a single container,
        from  the initial head position until the process outputs the single
        last element, use the method output_all().

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LoopWindow(input_music,
        ...                            window_size=(3, 4),
        ...                            step_size=(1, 4),
        ...                            )
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

    .. container:: example

        To change the size of the looping window after instantiation, use the
        method set_window_size(). In the example below, the initial window is
        of size (4, 4), but changes to (3, 8) after three calls. Notice how the
        very first call attaches a time signature equivalent to the window size
        to the output window; subsequent calls will not have time signatures
        unless the size of the looping window changes.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindow(input_music)
        >>> for _ in range(3):
        ...     notes = looper()
        ...     staff = abjad.Staff(notes)
        ...     abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
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
        \new Staff
        {
            c'8
            d'8
            ~
            d'4.
            e'8
            ~
            e'8
            f'8
        }
        >>> looper.set_window_size((3, 8))
        >>> for _ in range(3):
        ...     notes = looper()
        ...     staff = abjad.Staff(notes)
        ...     abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'16
            d'16
            ~
            d'4
        }
        \new Staff
        {
            d'4.
        }
        \new Staff
        {
            d'4.
        }

    ..  container:: example

        This class can handle tuplets, but this functionality should be
        considered experimental.

        >>> input_music = abjad.Container(r"\times 2/3 {c'8 d'8 e'} d'2.")
        >>> looper = auxjad.LoopWindow(input_music,
        ...                            window_size=(3, 4),
        ...                            step_size=(1, 16))
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
    """

    def __init__(self,
                 container: abjad.Container,
                 *,
                 window_size: tuple = (4, 4),
                 step_size: tuple = (1, 16),
                 max_steps: int = 1,
                 repetition_chance: float = 0.0,
                 head_position: tuple = (0, 1),
                 omit_time_signature: bool = False,
                 ):
        if not isinstance(container, abjad.Container):
            raise TypeError("'container' must be 'abjad.Container' or "
                            "child class")
        if not isinstance(window_size,
                          (int, float, tuple, str, abjad.Meter),
                          ):
            raise TypeError("'window_size' must be 'tuple' or 'abjad.Meter'")
        if not isinstance(step_size,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'step_size' must be a 'tuple' or "
                            "'abjad.Duration'")
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if max_steps < 1:
            raise ValueError("'max_steps' must be greater than zero")
        if not isinstance(repetition_chance, float):
            raise TypeError("'repetition_chance' must be 'float'")
        if repetition_chance < 0.0 or repetition_chance > 1.0:
            raise ValueError("'repetition_chance' must be between 0.0 and 1.0")
        if not isinstance(head_position,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'head_position' must be a number or "
                            "'abjad.Duration'")
        if not isinstance(omit_time_signature, bool):
            raise TypeError("'omit_time_signature' must be 'bool'")

        self._container = copy.deepcopy(container)
        self._container_length = abjad.inspect(container[:]).duration()

        if  abjad.Meter(window_size).duration > self._container_length:
            raise ValueError("'window_size' must be smaller than or equal to "
                             "the duration of 'container'")
        if abjad.Duration(head_position) >= self._container_length:
            raise ValueError("'head_position' must be smaller than "
                             "the duration of 'container'")

        self.head_position = abjad.Duration(head_position)
        self.window_size = abjad.Meter(window_size)
        self.step_size = abjad.Duration(step_size)
        self.repetition_chance = repetition_chance
        self.max_steps = max_steps
        self.omit_time_signature = omit_time_signature
        self._first_window = True
        self._new_time_signature = True

    def __call__(self) -> abjad.Selection:
        self._move_head()
        if self._done():
            raise RuntimeError("'container' has been exhausted")
        self._slice_container()
        return copy.deepcopy(self._current_window)

    def set_head_position(self,
                          head_position: tuple,
                          ):
        if not isinstance(head_position,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'head_position' must be a number or "
                            "'abjad.Duration'")
        if abjad.Duration(head_position) >= self._container_length:
            raise ValueError("'head_position' must be smaller than the "
                             "length of 'container'")
        self.head_position = abjad.Duration(head_position)

    def set_window_size(self,
                        window_size: tuple,
                        ):
        if not isinstance(window_size,
                          (int, float, tuple, str, abjad.Meter),
                          ):
            raise TypeError("'window_size' must be 'tuple' or 'abjad.Meter'")
        if abjad.Meter(window_size).duration >= self._container_length \
                              - self.head_position:
            raise ValueError("'window_size' must be smaller than or equal "
                             "to the length of 'container'")
        if self.window_size.duration != abjad.Meter(window_size).duration:
            self.window_size = abjad.Meter(window_size)
            self._new_time_signature = True

    def set_step_size(self,
                      step_size: tuple,
                      ):
        if not isinstance(step_size,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'step_size' must be a 'tuple' or "
                            "'abjad.Duration'")
        self.step_size = abjad.Duration(step_size)

    def set_max_steps(self,
                      max_steps: int,
                      ):
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if max_steps < 1:
            raise ValueError("'max_steps' must be greater than zero")
        self.max_steps = max_steps

    def set_repetition_chance(self,
                              repetition_chance: float,
                              ):
        if not isinstance(repetition_chance, float):
            raise TypeError("'repetition_chance' must be 'float'")
        if repetition_chance < 0.0 or repetition_chance > 1.0:
            raise ValueError("'repetition_chance' must be between 0.0 and 1.0")
        self.repetition_chance = repetition_chance

    def set_omit_time_signature(self,
                                omit_time_signature: bool,
                                ):
        if not isinstance(omit_time_signature, bool):
            raise TypeError("'omit_time_signature' must be 'bool'")
        self.omit_time_signature = omit_time_signature

    def get_current_window(self) -> abjad.Selection:
        return copy.deepcopy(self._current_window)

    def _done(self):
        return self.head_position >= self._container_length

    def _slice_container(self) -> abjad.Selection:
        head = self.head_position
        window_size = self.window_size
        dummy_container = copy.deepcopy(self._container)
        # splitting leaves at both slicing points
        if head > abjad.Duration(0, 1):
            abjad.mutate(dummy_container[:]).split([head,
                                                    window_size.duration,
                                                    ])
        else:
            abjad.mutate(dummy_container[:]).split([window_size.duration])
        # finding start and end indeces for the window
        for start in range(len(dummy_container)):
            if abjad.inspect(dummy_container[:start + 1]).duration() > head:
                abjad.detach(abjad.Tie(), dummy_container[start - 1])
                break
        for end in range(start + 1, len(dummy_container)):
            if abjad.inspect(dummy_container[start : end]).duration() == \
                    window_size.duration:
                abjad.detach(abjad.Tie(), dummy_container[end - 1])
                break
        else:
            end = len(dummy_container)
        # appending rests if necessary
        container_dur = abjad.inspect(dummy_container[start : end]).duration()
        if container_dur < window_size.duration:
            missing_dur = window_size.duration - container_dur
            rests = abjad.LeafMaker()(None, missing_dur)
            dummy_container.extend(rests)
            end += len(rests)
        # transforming abjad.Selection -> abjad.Container for rewrite_meter
        dummy_container = abjad.Container(
            abjad.mutate(dummy_container[start : end]).copy()
        )
        abjad.mutate(dummy_container[:]).rewrite_meter(window_size)
        if self._new_time_signature:
            abjad.attach(abjad.TimeSignature(window_size),
                         abjad.select(dummy_container).leaves()[0],
                         )
            self._new_time_signature = False
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    def _move_head(self):
        if not self._first_window:  # first window always at initial position
            if self.repetition_chance == 0.0 \
                    or random.random() > self.repetition_chance:
                self.head_position += \
                    self.step_size * random.randint(1, self.max_steps)
        else:
            self._first_window = False

    def output_all(self) -> abjad.Selection:
        dummy_container = abjad.Container()
        while True:
            try:
                dummy_container.append(self.__call__())
            except:
                break
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    def __iter__(self):
        return self

    def __next__(self) -> abjad.Selection:
        self._move_head()
        if self._done():
            raise StopIteration
        self._slice_container()
        return copy.deepcopy(self._current_window)
