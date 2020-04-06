import abjad
import random
import copy
from .simplified_time_signature_ratio import simplified_time_signature_ratio


class LoopWindowByElements():
    r"""Takes a container as input as well as an integer representing the
    number of elements per looping window, then outputs a container with
    the elements processed in the looping process. For instance, if the initial
    container had the leaves [A, B, C, D, E, F] and the looping window was size
    three, the output would be: A B C B C D C D E D E F E F F, which can be
    better visualised as:

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
        arguments. Each call of the object, in this case looper(), will move
        the window forwards and output the result. Notice that the time
        signatures in the example below are commented out with %%% because
        abjad only adds them to the score once the leaves are part of a staff:

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=3,
        ...                                      )
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
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }

        The method get_current_window() will output the current window without
        moving the head forwards.

        >>> notes = looper.get_current_window()
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

    ..  container:: example

        The instances of LoopWindowByElements can also be used as an iterator,
        which can then be used in a for loop to exhaust all windows.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=2,
        ...                                      )
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
            \time 3/4
            d'2
            e'4
        }
        \new Staff
        {
            \time 1/4
            e'4
        }

    ..  container:: example

        This class can take many optional keyword arguments during its
        creation. step_size dictates the size of each individual step in
        number of elements (default value is 1). max_steps sets the maximum
        number of steps that the window can advance when the object is called,
        ranging between 1 and the input value (default is also 1).
        repetition_chance sets the chance of a window result repeating itself
        (that is, the window not moving forwards when called). It should range
        from 0.0 to 1.0 (default 0.0, i.e. no repetition). Finally,
        initial_head_position can be used to offset the starting position of
        the looping window. It must be an integer and its default value is 0.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=3,
        ...                                      step_size=1,
        ...                                      max_steps=2,
        ...                                      repetition_chance=0.25,
        ...                                      initial_head_position=0,
        ...                                      )
        >>> looper.elements_per_window
        3
        >>> looper.step_size
        1
        >>> looper.repetition_chance
        0.25
        >>> looper.max_steps
        2
        >>> looper.current_head_position
        0

    ..  container:: example

        This class has an internal counter which counts the number of times it
        has been called. It can be reset with the method reset_counter().
        Resetting the counter will not reset the current_head_position. To
        change the head position, use the method set_head_position(). Notice
        that the counter simply counts the number of calls, while the
        current_head_position only moves forwards after a call (since it may
        not move at all when using repetition_chance). It also stays at 0 after
        the very first call, since that is when the 0-th window is output.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=3,
        ...                                      )
        >>> looper.counter
        0
        >>> looper.current_head_position
        0
        >>> for _ in range(4):
        ...     looper()
        >>> looper.counter
        4
        >>> looper.current_head_position
        3
        >>> looper.reset_counter()
        >>> looper.current_head_position
        4
        >>> looper.counter
        0
        >>> looper.set_head_position(0)
        >>> looper.current_head_position
        0
        >>> looper.counter
        0

    ..  container:: example

        The function len() can be used to get the total number of elements in
        the container.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=3,
        ...                                      )
        >>> len(looper)
        5

    ..  container:: example

        To run through the whole process and output it as a single container,
        from  the initial head position until the process outputs the single
        last element, use the method output_all().

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=2,
        ...                                      )
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

    .. container:: example

        To change the size of the window after instantiation, use the method
        set_elements_per_window(). In the example below, the initial window is
        of size 3, and so the first call of the looper object outputs the
        first, second, and third leaves. The window size is then set to 4, and
        the looper is called again, moving to the leaf in the next position,
        thus outputting the second, third, fourth, and fifth leaves.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=3,
        ...                                      )
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
        >>> looper.set_elements_per_window(4)
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

    ..  container:: example

        This class can handle tuplets, but the output is not ideal and so this
        functionality should be considered experimental. Time signatures will
        be correct when dealing with partial tuplets (thus having non-standard
        values in their denominators), but each individual note of a tuplet
        will have the ratio printed above it.

        >>> input_music = abjad.Container(r"c'4 d'8 \times 2/3 {a4 g2}")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      elements_per_window=2,
        ...                                      )
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
    """

    def __init__(self,
                 container: abjad.Container,
                 *,
                 elements_per_window: int,
                 step_size: int = 1,
                 max_steps: int = 1,
                 repetition_chance: float = 0.0,
                 initial_head_position: int = 0,
                 ):
        if not isinstance(container, abjad.Container):
            raise TypeError("'container' must be 'abjad.Container' or "
                            "child class")
        if not isinstance(elements_per_window, int):
            raise TypeError("'elements_per_window' must be 'int'")
        if not isinstance(step_size, int):
            raise TypeError("'step_size' must be 'int'")
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if not isinstance(repetition_chance, float):
            raise TypeError("'repetition_chance' must be 'float'")
        if repetition_chance < 0.0 or repetition_chance > 1.0:
            raise ValueError("'repetition_chance' must be between 0.0 and 1.0")
        if not isinstance(initial_head_position, int):
            raise TypeError("'initial_head_position' must be 'int'")

        self._container = abjad.select(container).logical_ties()

        if initial_head_position >= self._container.__len__():
            raise ValueError("'initial_head_position' must be smaller than "
                             "the length of 'container'")

        self.current_head_position = initial_head_position
        self.elements_per_window = elements_per_window
        self.step_size = step_size
        self.repetition_chance = repetition_chance
        self.max_steps = max_steps
        self.counter = 0
        self._slice_container()

    def __call__(self) -> abjad.Selection:
        self._move_head()
        if self._done():
            raise RuntimeError("'container' has been exhausted")
        self._slice_container()
        return copy.deepcopy(self._current_window)

    def reset_counter(self):
        self.counter = 0

    def set_head_position(self, new_head_position):
        if new_head_position >= self._container.__len__():
            raise ValueError("'new_head_position' must be smaller than "
                             "the length of 'container'")
        self.current_head_position = new_head_position

    def set_elements_per_window(self, new_elements_per_window):
        self.elements_per_window = new_elements_per_window

    def get_current_window(self) -> abjad.Selection:
        return copy.deepcopy(self._current_window)

    def __len__(self):
        return len(self._container)

    def _done(self):
        return self.current_head_position >= self._container.__len__()

    def _slice_container(self) -> abjad.Selection:
        start = self.current_head_position
        end = self.current_head_position + self.elements_per_window
        logical_ties = self._container[start:end]
        dummy_container = abjad.Container()
        time_signature_duration = 0
        for logical_tie in logical_ties:
            effective_duration = abjad.inspect(logical_tie).duration()
            logical_tie_ = copy.deepcopy(logical_tie)
            dummy_container.append(logical_tie_)
            multiplier = effective_duration / logical_tie_.written_duration
            logical_tie_ = abjad.mutate(logical_tie_).scale(multiplier)
            time_signature_duration += effective_duration
        if len(logical_ties) > 0:
            time_signature = abjad.TimeSignature(time_signature_duration)
            time_signature = simplified_time_signature_ratio(time_signature)
            abjad.attach(time_signature,
                         abjad.select(dummy_container).leaves()[0])
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    def _move_head(self):
        if self.counter > 0:  # 1st time always leave head at initial position
            if self.repetition_chance == 0.0 \
                    or random.random() > self.repetition_chance:
                self.current_head_position += \
                    self.step_size * random.randint(1, self.max_steps)
        self.counter += 1

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

    def __next__(self) -> list:
        self._move_head()
        if self._done():
            raise StopIteration
        self._slice_container()
        return copy.deepcopy(self._current_window)
