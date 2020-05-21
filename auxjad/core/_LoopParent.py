import copy
import random
import abjad
from ..utilities.leaves_are_tieable import leaves_are_tieable


class _LoopParent():
    r"""This is the parent class of all LoopByXxxx classes. It implements all
    common methods and properties, and initialises those using their @setter
    methods.
    """

    ### INITIALISER ###

    def __init__(self,
                 head_position,
                 window_size,
                 step_size,
                 max_steps,
                 repetition_chance,
                 forward_bias,
                 move_window_on_first_call,
                 ):
        if not isinstance(move_window_on_first_call, bool):
            raise TypeError("'move_window_on_first_call' must be 'bool'")
        self.head_position = head_position
        self.window_size = window_size
        self.step_size = step_size
        self.max_steps = max_steps
        self.repetition_chance = repetition_chance
        self.forward_bias = forward_bias
        self._is_first_window = not move_window_on_first_call

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Selection:
        r"""Calls the looping process for one iteration, returning an
        ``abjad.Selection``.
        """
        self._move_head()
        if self._done:
            raise RuntimeError("'contents' has been exhausted")
        self._slice_contents()
        return self.current_window

    def __iter__(self):
        r'Allows instances to be used as iterators.'
        return self

    def __next__(self) -> abjad.Selection:
        r"""Calls the looping process for one iteration, returning an
        ``abjad.Selection``.
        """
        self._move_head()
        if self._done:
            raise StopIteration
        self._slice_contents()
        return self._current_window

    ### PUBLIC METHODS ###

    def output_all(self,
                   *,
                   tie_identical_pitches: bool = False,
                   ) -> abjad.Selection:
        r"""Goes through the whole looping process and outputs a single
        ``abjad.Selection``.
        """
        if not isinstance(tie_identical_pitches, bool):
            raise TypeError("'tie_identical_pitches' must be 'bool'")
        dummy_container = abjad.Container()
        while True:
            try:
                if not tie_identical_pitches or len(dummy_container) == 0:
                    dummy_container.append(self.__call__())
                else:
                    new_window = self.__call__()
                    leaf1 = abjad.select(new_window).leaves()[0]
                    leaf2 = abjad.select(dummy_container).leaves()[-1]
                    if leaves_are_tieable(leaf1, leaf2):
                        abjad.attach(abjad.Tie(), dummy_container[-1])
                    dummy_container.append(new_window)
            except RuntimeError:
                break
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    def output_n(self,
                 n: int,
                 *,
                 tie_identical_pitches: bool = False,
                 ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the looping process and outputs a
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
            if not tie_identical_pitches or len(dummy_container) == 0:
                dummy_container.append(self.__call__())
            else:
                new_window = self.__call__()
                leaf1 = abjad.select(new_window).leaves()[0]
                leaf2 = abjad.select(dummy_container).leaves()[-1]
                if leaves_are_tieable(leaf1, leaf2):
                    abjad.attach(abjad.Tie(), dummy_container[-1])
                dummy_container.append(new_window)
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    ### PRIVATE METHODS ###

    def _move_head(self):
        r"""Moves the head by a certain number of steps of fixed size, either
        forwards or backwards according to the forward bias
        """
        if not self._is_first_window:  # 1st window always at initial position
            if (self._repetition_chance == 0.0
                    or random.random() > self._repetition_chance):
                step = self._step_size * random.randint(1, self._max_steps)
                diretion = self._biased_choice(self._forward_bias)
                self._head_position += step * diretion
        else:
            self._is_first_window = False

    def _slice_contents(self):
        pass

    @staticmethod
    def _biased_choice(bias):
        return random.choices([1, -1], weights=[bias, 1.0-bias])[0]

    @staticmethod
    def _remove_all_time_signatures(contents):
        for leaf in abjad.select(contents).leaves():
            if abjad.inspect(leaf).effective(abjad.TimeSignature):
                abjad.detach(abjad.TimeSignature, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def head_position(self) -> int:
        r'The position of the head at the start of a looping window.'
        return self._head_position

    @head_position.setter
    def head_position(self,
                      head_position: int,
                      ):
        if not isinstance(head_position, int):
            raise TypeError("'head_position' must be 'int'")
        if head_position < 0:
            raise ValueError("'head_position' must be a positive 'int'")
        if head_position >= self._contents.__len__():
            raise ValueError("'head_position' must be smaller than the length "
                             "of 'contents'")
        self._is_first_window = True
        self._head_position = head_position

    @property
    def window_size(self) -> int:
        r'The length of the looping window.'
        return self._window_size

    @window_size.setter
    def window_size(self,
                    window_size: int,
                    ):
        if not isinstance(window_size, int):
            raise TypeError("'window_size' must be 'int'")
        if window_size < 1:
            raise ValueError("'window_size' must be greater than zero")
        if window_size > self._contents.__len__():
            raise ValueError("'window_size' must be smaller than or equal to "
                             "the length of 'contents'")
        self._window_size = window_size

    @property
    def step_size(self) -> int:
        r'The size of each step when moving the head.'
        return self._step_size

    @step_size.setter
    def step_size(self,
                  step_size: int,
                  ):
        if not isinstance(step_size, int):
            raise TypeError("'step_size' must be 'int'")
        if step_size < 1:
            raise ValueError("'step_size' must be greater than zero")
        if step_size >= self._contents.__len__():
            raise ValueError("'step_size' must be smaller than the length of "
                             "'contents'")
        self._step_size = step_size

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
    def repetition_chance(self) -> float:
        r'The chance of the head not moving, thus repeating the output.'
        return self._repetition_chance

    @repetition_chance.setter
    def repetition_chance(self,
                          repetition_chance: float,
                          ):
        if not isinstance(repetition_chance, float):
            raise TypeError("'repetition_chance' must be 'float'")
        if repetition_chance < 0.0 or repetition_chance > 1.0:
            raise ValueError("'repetition_chance' must be between 0.0 and 1.0")
        self._repetition_chance = repetition_chance

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
    def current_window(self) -> (list, abjad.Selection):
        r"""Read-only property, returns the window at the current head
        position.
        """
        return copy.deepcopy(self._current_window)

    ### PRIVATE PROPERTIES ###

    @property
    def _done(self) -> bool:
        r"""Boolean indicating whether the process is done (i.e. whether the
        head position has overtaken the ``contents`` length).
        """
        return (self._head_position >= self._contents.__len__()
            or self._head_position < 0)
