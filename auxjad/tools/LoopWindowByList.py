import random


class LoopWindowByList():
    r"""Similar to LoopWindowByList, but instead of taking an
    abjad.Container as input, it takes a list of arbitrary size. It then
    outputs the list elements, whatever they may be. The list elements can be
    abjad.Container's, but they can also be anything else, thus being more
    general. Takes a list as input as well as an integer representing the
    number of elements per looping window, then outputs individual elements
    with according to the looping process. For instance, if the initial
    list had the elements [A, B, C, D, E, F] and the looping window was size
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

        It takes a list and the number of elements of the window as arguments.
        Each call of the object, in this case looper(), will move the window
        forwards and output the result:

        >>> input_list = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
        >>> looper()
        ['A', 'B', 'C']
        >>> looper()
        ['B', 'C', 'D']

        The method get_current_window() will output the current window without
        moving the head forwards.

        >>> looper.get_current_window()
        ['B', 'C', 'D']

    ..  container:: example

        The instances of LoopWindowByList can also be used as an iterator,
        which can then be used in a for loop to exhaust all windows.

        >>> input_list = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> looper = auxjad.LoopWindowByList(input_list,
        ...                                  elements_per_window=3,
        ...                                  )
        >>> for window in looper:
        ...     print(window)
        ['A', 'B', 'C']
        ['B', 'C', 'D']
        ['C', 'D', 'E']
        ['D', 'E', 'F']
        ['E', 'F']
        ['F']

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
        the looping window (default is 0).

        >>> input_list = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> looper = auxjad.LoopWindowByList(input_list,
        ...                                  elements_per_window=3,
        ...                                  step_size=1,
        ...                                  max_steps=2,
        ...                                  repetition_chance=0.25,
        ...                                  initial_head_position=0,
        ...                                  )
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

        >>> input_list = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
        >>> looper.counter
        0
        >>> looper.current_head_position
        0
        >>> for _ in range(4):
        ...     looper()
        ['A', 'B', 'C']
        ['B', 'C', 'D']
        ['C', 'D', 'E']
        ['D', 'E', 'F']
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

        >>> input_list = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
        >>> len(looper)
        6

    ..  container:: example

        To run through the whole process and output it as a single list, from
        the initial head position until the process outputs the single last
        element, use the method output_all().

        >>> input_list = ['A', 'B', 'C', 'D']
        >>> looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
        >>> looper.output_all()
        ['A', 'B', 'C', 'B', 'C', 'D', 'C', 'D', 'D']

    .. container:: example

        To change the size of the window after instantiation, use the method
        set_elements_per_window(). In the example below, the initial window is
        of size 3, and so the first call of the looper object outputs the
        first, second, and third elements of the list. The window size is then
        set to 4, and the looper is called again, moving to the element in the
        next position, thus outputting the second, third, fourth, and fifth
        elements.

        >>> input_list = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
        >>> looper()
        ['A', 'B', 'C']
        >>> looper.set_elements_per_window(4)
        >>> looper()
        ['B', 'C', 'D', 'E']

    .. container:: example

        It should be clear that the list can contain any types of elements:

        >>> input_list = [123, 'foo', (3, 4), 3.14]
        >>> looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
        >>> looper()
        [123, 'foo', (3, 4)]

        This includes Abjad's types, though it is important to remember Abjad's
        exclusive membership requirement; since this class will output a same
        element multiples times, it might be necessary to use copy.deepcopy to
        avoid breaking the membership rule:

        >>> import abjad
        >>> import copy
        >>> input_list = [
        ...     abjad.Container(r"c'4 d'4 e'4 f'4"),
        ...     abjad.Container(r"fs'1"),
        ...     abjad.Container(r"r2 bf2"),
        ...     abjad.Container(r"c''2. r4"),
        ... ]
        >>> looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
        >>> staff = abjad.Staff()
        >>> for element in looper.output_all():
        ...     staff.append(copy.deepcopy(element))
        >>> abjad.f(staff)
        \new Staff
        {
            {
                c'4
                d'4
                e'4
                f'4
            }
            {
                fs'1
            }
            {
                r2
                bf2
            }
            {
                fs'1
            }
            {
                r2
                bf2
            }
            {
                c''2.
                r4
            }
            {
                r2
                bf2
            }
            {
                c''2.
                r4
            }
            {
                c''2.
                r4
            }
        }
    """

    def __init__(self,
                 container: list,
                 *,
                 elements_per_window: int,
                 step_size: int = 1,
                 max_steps: int = 1,
                 repetition_chance: float = 0.0,
                 initial_head_position: int = 0,
                 ):
        if not isinstance(container, list):
            raise TypeError("'container' must be 'list'")
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
        if initial_head_position >= len(container):
            raise ValueError("'initial_head_position' must be smaller than "
                             "the length of 'container'")

        self._container = container[:]
        self.current_head_position = initial_head_position
        self.elements_per_window = elements_per_window
        self.step_size = step_size
        self.repetition_chance = repetition_chance
        self.max_steps = max_steps
        self.counter = 0
        self._slice_container()

    def __call__(self) -> list:
        self._move_head()
        if self._done():
            raise RuntimeError("'container' has been exhausted")
        self._slice_container()
        return self._current_window[:]

    def reset_counter(self):
        self.counter = 0

    def set_head_position(self, new_head_position):
        if new_head_position >= self._container.__len__():
            raise ValueError("'new_head_position' must be smaller than the "
                             "length of 'container'")
        self.current_head_position = new_head_position

    def set_elements_per_window(self, new_elements_per_window):
        self.elements_per_window = new_elements_per_window

    def get_current_window(self) -> list:
        return self._current_window[:]

    def __len__(self):
        return len(self._container)

    def _done(self):
        return self.current_head_position >= self._container.__len__()

    def _slice_container(self) -> list:
        start = self.current_head_position
        end = self.current_head_position + self.elements_per_window
        self._current_window = self._container[start:end]

    def _move_head(self):
        if self.counter > 0:  # 1st time always leave head at initial position
            if self.repetition_chance == 0.0 \
                    or random.random() > self.repetition_chance:
                self.current_head_position += \
                    self.step_size * random.randint(1, self.max_steps)
        self.counter += 1

    def output_all(self) -> list:
        dummy_container = []
        while True:
            try:
                dummy_container.extend(self.__call__())
            except:
                break
        return dummy_container[:]

    def __iter__(self):
        return self

    def __next__(self) -> list:
        self._move_head()
        if self._done():
            raise StopIteration
        self._slice_container()
        return self._current_window[:]
